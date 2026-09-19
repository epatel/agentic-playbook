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
PDF    := $(BUILD)/$(NAME).pdf
HTML   := $(BUILD)/$(NAME).html

# Whatever hands a file to the desktop: macOS has open, most Linux desktops have xdg-open.
OPENER ?= $(shell command -v open 2>/dev/null || command -v xdg-open 2>/dev/null)

.DEFAULT_GOAL := help
.PHONY: help pdf md html open open-html check lint clean

help: ## Show this help
	@echo "The Agentic Playbook"
	@echo
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-10s %s\n", $$1, $$2}'
	@echo
	@echo "  Pass extra flags with ARGS, e.g. make pdf ARGS='--pdf-engine typst --strict'"

pdf: ## Collect the book and render build/agentic-playbook.pdf (needs pandoc + a PDF engine)
	$(PYTHON) $(SCRIPT) --format pdf $(OUT) $(ARGS)

md: ## Collect the book into build/agentic-playbook.md (no external tools needed)
	$(PYTHON) $(SCRIPT) --format md $(OUT) $(ARGS)

html: ## Collect the book into one self-contained build/agentic-playbook.html (needs pandoc)
	$(PYTHON) $(SCRIPT) --format html $(OUT) $(ARGS)

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

clean: ## Remove build output
	rm -rf $(BUILD)
