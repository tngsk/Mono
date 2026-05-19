.PHONY: setup test run

setup:
	npm ci
	uv run playwright install

test:
	uv run pytest

run:
	uv run python src/main.py
