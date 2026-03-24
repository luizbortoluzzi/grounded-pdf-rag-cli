.PHONY: help setup install ingest chat test lint clean docker-up docker-down

help:
	@echo "Grounded PDF RAG CLI - Available commands:"
	@echo "  make setup      - Create venv, install deps, show next steps"
	@echo "  make install    - Install dependencies"
	@echo "  make install-dev - Install deps + dev tools (pytest, ruff)"
	@echo "  make ingest     - Run PDF ingestion"
	@echo "  make chat       - Run interactive chat"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run ruff linter"
	@echo "  make clean      - Remove cache and build artifacts"
	@echo "  make docker-up  - Start PostgreSQL with pgvector"
	@echo "  make docker-down - Stop PostgreSQL"

setup:
	@echo "Creating virtual environment..."
	python3 -m venv venv
	@echo "Activate with: source venv/bin/activate (Linux/macOS) or venv\\Scripts\\activate (Windows)"
	@echo "Then run: make install"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

ingest:
	python3 src/ingest.py

chat:
	python3 src/chat.py

test:
	pytest

lint:
	ruff check src tests

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

docker-up:
	docker compose up -d

docker-down:
	docker compose down
