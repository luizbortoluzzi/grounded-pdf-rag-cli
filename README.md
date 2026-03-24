# Grounded PDF RAG CLI

A CLI-based RAG (Retrieval-Augmented Generation) system that ingests PDFs into PostgreSQL with pgvector and answers questions using only the document content.

## Requirements

- Python 3.10+
- Docker & Docker Compose
- OpenAI API key

## Quick Start

```bash
make setup                    # Create venv
source venv/bin/activate      # Activate (Linux/macOS)
make install                  # Install dependencies
cp .env.example .env          # Configure (set OPENAI_API_KEY)
make docker-up                # Start PostgreSQL
make ingest                   # Ingest document.pdf
make chat                     # Run interactive chat
```

## Setup

1. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # or: venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Copy `.env.example` to `.env` and set:

   - `OPENAI_API_KEY` – your OpenAI API key
   - Database settings (or `DATABASE_URL`) – defaults work with the provided docker-compose

4. **Place `document.pdf` in the project root** (or set `PDF_PATH` in `.env`)

## Execution

### 1. Start the database

```bash
docker compose up -d
# or: make docker-up
```

### 2. Ingest the PDF

```bash
python src/ingest.py
# or: make ingest
```

### 3. Run the chat

```bash
python src/chat.py
# or: make chat
```

Example interaction:

```
Ask your question (or type 'exit' to quit):

QUESTION: What was Company X's revenue?
ANSWER: Revenue was 10 million dollars.

QUESTION: How many customers do we have in 2024?
ANSWER: I don't have the necessary information to answer your question.
```

## Development

```bash
make install-dev    # Install deps + pytest, ruff
make test           # Run tests
make lint           # Run ruff linter
make clean          # Remove cache artifacts
```

## Project Structure

```
├── .github/workflows/ci.yml  # GitHub Actions CI
├── ARCHITECTURE.md           # System design documentation
├── CHANGELOG.md              # Version history
├── Makefile                  # Development commands
├── pyproject.toml            # Tool config (pytest, ruff)
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── document.pdf
├── README.md
└── src/
    ├── __init__.py
    ├── ingest.py       # PDF ingestion entrypoint
    ├── search.py       # Similarity search and QA chain
    ├── chat.py         # Interactive CLI
    ├── config.py       # Environment and validation
    ├── prompts.py      # Grounded QA prompt template
    ├── db.py           # PGVector store
    ├── embeddings.py   # OpenAI embeddings
    ├── llm.py          # ChatOpenAI model
    ├── utils.py        # Helpers
    └── exceptions.py  # Custom exceptions
tests/
    ├── test_config.py
    ├── test_prompts.py
    ├── test_utils.py
    └── test_exceptions.py
```
