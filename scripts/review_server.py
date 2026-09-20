#!/usr/bin/env python3
"""Read the book in a browser and annotate it in the margin, live, with other people.

Run it with ``make review``. It serves the chapters named in ``book/README.md`` — the same table
of contents the build reads, so the review and the book can never disagree about what is in it —
renders each one to HTML, and lets a reader select a passage and attach a comment to it.

Two things make an annotation useful to the agent that has to act on it:

* it carries the **source** position, ``book/`` path and line number, not a position in rendered
  HTML, because the agent edits markdown; and
* it carries the **quoted text**, so the anchor survives the line moving underneath it.

Annotations are an append-only event log in ``review/annotations.jsonl`` — create, resolve, reopen
and delete are all appends, never rewrites, which is what makes concurrent writers safe without a
database and a migration path (cards/standing-defaults.md). ``review/REVIEW.md`` is regenerated
from that log on every change, and is the file an agent should read: it is the review as a task
list, in reading order.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from markdown_it import MarkdownIt

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_book as bb  # noqa: E402  — the table of contents contract lives there, not here

ROOT = bb.ROOT
BOOK = bb.BOOK
REVIEW = ROOT / "review"
EVENTS = REVIEW / "annotations.jsonl"
DIGEST = REVIEW / "REVIEW.md"
APP_HTML = Path(__file__).resolve().parent / "review_app.html"
BOOK_CSS = Path(__file__).resolve().parent / "book.css"


# ---------------------------------------------------------------------------------- the chapters


def chapters() -> list[dict]:
    """Every chapter in the table of contents that exists on disk, in reading order."""
    parts = bb.parse_toc(bb.TOC_FILE.read_text(encoding="utf-8"))
    out = []
    for part in parts:
        for chapter in part.chapters:
            if chapter.file.is_file():
                out.append({"path": chapter.path, "title": chapter.title, "part": part.title})
    return out


def chapter_paths() -> set[str]:
    return {c["path"] for c in chapters()}


# ----------------------------------------------------------------------------------- rendering

#: Tables and strikethrough are used in the book; the rest of CommonMark is the default.
MD = MarkdownIt("commonmark", {"breaks": False, "linkify": False}).enable(["table", "strikethrough"])


def _mermaid_fence(self, tokens, idx, options, env):
    """A mermaid block is a diagram, not a code sample: hand it to mermaid.js in the browser."""
    token = tokens[idx]
    line = token.map[0] + 1 if token.map else 0
    if token.info.strip() == "mermaid":
        return f'<pre class="mermaid" data-line="{line}">{token.content}</pre>\n'
    info = token.info.strip().split(" ")[0]
    cls = f' class="language-{info}"' if info else ""
    escaped = (token.content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return f'<pre data-line="{line}"><code{cls}>{escaped}</code></pre>\n'


MD.add_render_rule("fence", _mermaid_fence)


def render(markdown: str) -> str:
    """Render one chapter, tagging every block with the source line it started on.

    ``token.map`` is markdown-it's own record of where a block came from, which is the whole
    reason this renders the book rather than reading the built HTML: pandoc produces a far better
    page and throws that mapping away, and without it an annotation cannot say which line it is
    about.
    """
    tokens = MD.parse(markdown)
    for token in tokens:
        if token.block and token.map and token.nesting >= 0 and token.type != "fence":
            token.attrSet("data-line", str(token.map[0] + 1))
    return MD.renderer.render(tokens, MD.options, {})


# -------------------------------------------------------------------------------------- the store


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    """The append-only event log, folded into the annotations it implies.

    Every change is one JSON object on one line. Nothing is ever rewritten, so two writers cannot
    lose each other's work, an accidental deletion is recoverable from the log, and the file stays
    something a person or an agent can read with ``cat``.
    """

    def __init__(self, path: Path = EVENTS) -> None:
        self.path = path
        self.lock = asyncio.Lock()

    def events(self) -> list[dict]:
        if not self.path.is_file():
            return []
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # a half-written line is not worth losing the rest of the log over
        return out

    def state(self) -> dict[str, dict]:
        """Fold the log: the current annotations, by id, in the order they were created."""
        live: dict[str, dict] = {}
        for event in self.events():
            op, ident = event.get("op"), event.get("id")
            if not ident:
                continue
            if op == "create":
                live[ident] = {k: v for k, v in event.items() if k != "op"} | {"status": "open"}
            elif ident in live:
                if op == "delete":
                    live.pop(ident, None)
                elif op in ("resolve", "reopen"):
                    live[ident]["status"] = "resolved" if op == "resolve" else "open"
                    live[ident]["updated"] = event.get("ts", "")
        return live

    async def append(self, event: dict) -> dict[str, dict]:
        async with self.lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(event, ensure_ascii=False) + "\n")
            state = self.state()
            write_digest(state)
            return state


# ------------------------------------------------------------------------------------- the digest


def write_digest(state: dict[str, dict]) -> None:
    """Regenerate `review/REVIEW.md`: the review as a task list, in the book's own order.

    This is the file to hand an agent. It is generated, never edited — an edit would be overwritten
    by the next annotation — and it says so at the top.
    """
    order = {c["path"]: i for i, c in enumerate(chapters())}
    titles = {c["path"]: c["title"] for c in chapters()}
    items = sorted(
        state.values(),
        key=lambda a: (order.get(a.get("file", ""), 10**6), a.get("line", 0), a.get("ts", "")),
    )
    open_items = [a for a in items if a.get("status") == "open"]

    lines = [
        "# Review",
        "",
        "Annotations left on the book in the review server, newest state, in reading order.",
        "**Generated by `scripts/review_server.py` from `review/annotations.jsonl` — edit the",
        "book, not this file.** Resolving an annotation in the browser removes it from the open",
        "list below; the event log keeps it either way.",
        "",
        f"{len(open_items)} open, {len(items) - len(open_items)} resolved, "
        f"as of {_now()}.",
        "",
    ]
    if not open_items:
        lines += ["Nothing open.", ""]

    current = None
    for item in open_items:
        path = item.get("file", "")
        if path != current:
            current = path
            lines += [f"## {titles.get(path, path)}", "", f"`book/{path}`", ""]
        line_no = item.get("line", 0)
        lines.append(f"- **`book/{path}:{line_no}`** — {item.get('comment', '').strip()}")
        quote = " ".join((item.get("quote") or "").split())
        if quote:
            if len(quote) > 240:
                quote = quote[:237] + "…"
            lines.append(f"  > {quote}")
        lines.append("")

    DIGEST.parent.mkdir(parents=True, exist_ok=True)
    DIGEST.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------------- the live wire


class Hub:
    """Everyone currently looking at the book, so a comment appears in every window at once."""

    def __init__(self) -> None:
        self.clients: set[WebSocket] = set()

    async def join(self, socket: WebSocket) -> None:
        await socket.accept()
        self.clients.add(socket)

    def leave(self, socket: WebSocket) -> None:
        self.clients.discard(socket)

    async def broadcast(self, message: dict) -> None:
        dead = []
        for client in list(self.clients):
            try:
                await client.send_json(message)
            except Exception:
                dead.append(client)
        for client in dead:
            self.leave(client)


store = Store()
hub = Hub()
app = FastAPI(title="The Agentic Playbook — review")


#: The page and its stylesheet are edited while the server is running, and a browser that caches
#: them will serve yesterday's build back with no sign that it has. This is a local review tool;
#: correctness on reload is worth more than a cached kilobyte.
NO_CACHE = {"Cache-Control": "no-store, must-revalidate"}


@app.get("/", response_class=HTMLResponse)
def index() -> FileResponse:
    return FileResponse(APP_HTML, headers=NO_CACHE)


@app.get("/book.css")
def book_css() -> FileResponse:
    return FileResponse(BOOK_CSS, media_type="text/css", headers=NO_CACHE)


@app.get("/api/toc")
def api_toc() -> JSONResponse:
    return JSONResponse(chapters())


@app.get("/api/chapter/{path:path}")
def api_chapter(path: str) -> JSONResponse:
    if path not in chapter_paths():
        raise HTTPException(404, f"{path} is not in the table of contents")
    source = (BOOK / path).read_text(encoding="utf-8")
    return JSONResponse({"path": path, "html": render(source), "lines": len(source.splitlines())})


@app.get("/api/annotations")
def api_annotations() -> JSONResponse:
    return JSONResponse(list(store.state().values()))


@app.get("/review.md", response_class=PlainTextResponse)
def review_md() -> str:
    return DIGEST.read_text(encoding="utf-8") if DIGEST.is_file() else "# Review\n\nNothing yet.\n"


@app.websocket("/ws")
async def ws(socket: WebSocket) -> None:
    await hub.join(socket)
    try:
        await socket.send_json({"type": "snapshot",
                                "annotations": list(store.state().values()),
                                "readers": len(hub.clients)})
        await hub.broadcast({"type": "readers", "readers": len(hub.clients)})
        while True:
            message = await socket.receive_json()
            kind = message.get("type")
            if kind == "create":
                comment = (message.get("comment") or "").strip()
                path = message.get("file") or ""
                if not comment or path not in chapter_paths():
                    continue
                event = {
                    "op": "create",
                    "id": uuid.uuid4().hex[:12],
                    "ts": _now(),
                    "file": path,
                    "line": int(message.get("line") or 0),
                    "quote": (message.get("quote") or "")[:2000],
                    "comment": comment[:4000],
                    "author": (message.get("author") or "anonymous")[:80],
                }
            elif kind in ("resolve", "reopen", "delete") and message.get("id"):
                event = {"op": kind, "id": message["id"], "ts": _now()}
            else:
                continue
            state = await store.append(event)
            await hub.broadcast({"type": "annotations",
                                 "annotations": list(state.values()),
                                 "readers": len(hub.clients)})
    except WebSocketDisconnect:
        pass
    finally:
        hub.leave(socket)
        await hub.broadcast({"type": "readers", "readers": len(hub.clients)})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--host", default="127.0.0.1", help="default: 127.0.0.1, localhost only")
    parser.add_argument("--port", type=int, default=8777)
    args = parser.parse_args(argv)

    import uvicorn

    write_digest(store.state())  # so review/REVIEW.md exists before anyone annotates anything
    print(f"The Agentic Playbook — review server on http://{args.host}:{args.port}")
    print(f"  annotations  {EVENTS.relative_to(ROOT)}")
    print(f"  digest       {DIGEST.relative_to(ROOT)}")
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
