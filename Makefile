# The Agentic Playbook — build targets.
#
# The book is markdown and stays readable without any of this. These targets exist to collect it
# into one file for review, and to render that file. Everything lands in build/, which is not
# committed.

PYTHON ?= python3
BUILD  ?= build
SCRIPT := scripts/build_book.py
ARGS   ?=

.DEFAULT_GOAL := help
.PHONY: help pdf md html check clean

help: ## Show this help
	@echo "The Agentic Playbook"
	@echo
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  make %-8s %s\n", $$1, $$2}'
	@echo
	@echo "  Pass extra flags with ARGS, e.g. make pdf ARGS='--pdf-engine typst --strict'"

pdf: ## Collect the book and render build/agentic-playbook.pdf (needs pandoc + a PDF engine)
	$(PYTHON) $(SCRIPT) --format pdf $(ARGS)

md: ## Collect the book into build/agentic-playbook.md (no external tools needed)
	$(PYTHON) $(SCRIPT) --format md $(ARGS)

html: ## Collect the book and render build/agentic-playbook.html (needs pandoc)
	$(PYTHON) $(SCRIPT) --format html $(ARGS)

check: ## Report chapters missing from disk and files missing from the table of contents
	$(PYTHON) $(SCRIPT) --check --strict $(ARGS)

clean: ## Remove build output
	rm -rf $(BUILD)
