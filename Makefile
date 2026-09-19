# The Agentic Playbook — build targets.
#
# The book is markdown and stays readable without any of this. These targets exist to collect it
# into one file for review, and to render that file. Everything lands in build/, which is not
# committed.

PYTHON ?= python3
BUILD  ?= build
NAME   ?= agentic-playbook
SCRIPT := scripts/build_book.py
STYLE  := scripts/check_style.py
ARGS   ?=
# Extra flags for the style checker alone, so that ARGS keeps carrying build flags. Not
# named LINT: make has a built-in variable of that name, and it is already set to `lint`.
STYLEARGS ?=

OUT    := --out-dir $(BUILD) --name $(NAME)

# Links that leave the book — a research brief, PLAN.md — are relative in the markdown, which is
# what makes them work when the book is read on GitHub. Collected into one file they would
# resolve against wherever that file happens to sit, so the build rewrites them to point at the
# repository. A release pins them to its own tag instead of main, so the PDF keeps citing the
# sources as they read when it was published.
REPO     ?= https://github.com/epatel/agentic-playbook
REPO_URL ?= $(REPO)/blob/main
LINKS    := --repo-url $(REPO_URL)
PDF    := $(BUILD)/$(NAME).pdf
HTML   := $(BUILD)/$(NAME).html

# A release is a dated snapshot of a book, not a version of a program: there is no API to break
# and no semantics a number could carry, so the timestamp is the version. Local time, to the
# minute, so two releases on one day sort correctly and never collide. Expanded once with := —
# with ?= the date would be re-read on every use, and a release started at 13:59:59 would tag
# one minute and upload a file named the other.
RELEASE_VERSION := $(shell date +v%Y.%m.%d-%H%M)
VERSION ?= $(RELEASE_VERSION)
RELEASE_PDF := $(BUILD)/$(NAME)-$(VERSION).pdf

# Whatever hands a file to the desktop: macOS has open, most Linux desktops have xdg-open.
OPENER ?= $(shell command -v open 2>/dev/null || command -v xdg-open 2>/dev/null)

.DEFAULT_GOAL := help
.PHONY: help pdf md html open open-html check lint release clean

help: ## Show this help
	@echo "The Agentic Playbook"
	@echo
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-10s %s\n", $$1, $$2}'
	@echo
	@echo "  Pass extra flags with ARGS, e.g. make pdf ARGS='--pdf-engine typst --strict'"

pdf: ## Collect the book and render build/agentic-playbook.pdf (needs pandoc + a PDF engine)
	$(PYTHON) $(SCRIPT) --format pdf $(OUT) $(LINKS) $(ARGS)

md: ## Collect the book into build/agentic-playbook.md (no external tools needed)
	$(PYTHON) $(SCRIPT) --format md $(OUT) $(LINKS) $(ARGS)

html: ## Collect the book into one self-contained build/agentic-playbook.html (needs pandoc)
	$(PYTHON) $(SCRIPT) --format html $(OUT) $(LINKS) $(ARGS)

open: pdf ## Build the PDF and open it in the default viewer
	@test -f "$(PDF)" || { echo "make open: $(PDF) was not rendered — see the build output above"; exit 1; }
	@test -n "$(OPENER)" || { echo "make open: no 'open' or 'xdg-open' on PATH; the PDF is at $(PDF)"; exit 1; }
	$(OPENER) "$(PDF)"

open-html: html ## Build the HTML book and open it in the default browser
	@test -f "$(HTML)" || { echo "make open-html: $(HTML) was not rendered — see the build output above"; exit 1; }
	@test -n "$(OPENER)" || { echo "make open-html: no 'open' or 'xdg-open' on PATH; the book is at $(HTML)"; exit 1; }
	$(OPENER) "$(HTML)"

# Both halves always run: fixing a missing chapter and fixing a 104-column line are different
# jobs, and stopping at the first one hides the second until the next invocation.
check: ## Report structural problems and style defects; write nothing, fail if either does
	@$(PYTHON) $(SCRIPT) --check --strict $(ARGS); structure=$$?; \
	$(PYTHON) $(STYLE) --strict $(STYLEARGS); style=$$?; \
	test $$structure -eq 0 -a $$style -eq 0

lint: ## Report style defects only: 100 columns, whitespace, fences, the outright bans
	$(PYTHON) $(STYLE) --strict $(STYLEARGS)

# Publishing is irreversible in the way that matters — a tag other people have fetched cannot be
# moved honestly — so everything that can be checked is checked before anything is pushed.
release: ## Build the PDF and publish it as a GitHub release tagged with the date and time
	@command -v gh >/dev/null 2>&1 || { echo "make release: needs the GitHub CLI; brew install gh"; exit 1; }
	@gh auth status >/dev/null 2>&1 || { echo "make release: gh is not logged in; run 'gh auth login'"; exit 1; }
	@test -z "$$(git status --porcelain)" || { echo "make release: working tree is dirty — commit or stash first"; exit 1; }
	@git rev-parse -q --verify "refs/tags/$(VERSION)" >/dev/null \
		&& { echo "make release: tag $(VERSION) already exists — wait a minute or pass VERSION="; exit 1; } || true
	@git fetch --quiet origin
	@test "$$(git rev-parse HEAD)" = "$$(git rev-parse '@{u}')" \
		|| { echo "make release: HEAD differs from its upstream — push first, so the tag names public history"; exit 1; }
	@$(MAKE) --no-print-directory check
	$(PYTHON) $(SCRIPT) --format pdf --out-dir $(BUILD) --name $(NAME)-$(VERSION) \
		--repo-url $(REPO)/blob/$(VERSION) $(ARGS)
	@test -f "$(RELEASE_PDF)" || { echo "make release: $(RELEASE_PDF) was not rendered — see the build output above"; exit 1; }
	git tag -a "$(VERSION)" -m "The Agentic Playbook $(VERSION)"
	git push --quiet origin "$(VERSION)"
	gh release create "$(VERSION)" "$(RELEASE_PDF)" \
		--title "The Agentic Playbook $(VERSION)" --generate-notes

clean: ## Remove build output
	rm -rf $(BUILD)
