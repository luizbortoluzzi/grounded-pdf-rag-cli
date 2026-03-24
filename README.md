# Grounded PDF RAG CLI

A CLI-based RAG (Retrieval-Augmented Generation) system that ingests PDFs into PostgreSQL with pgvector and answers questions using only the document content.

## Requirements

- Python 3.10+
- Docker & Docker Compose
- OpenAI API key

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
```

### 2. Ingest the PDF

```bash
python src/ingest.py
```

### 3. Run the chat

```bash
python src/chat.py
```

Example interaction:

```
Ask your question (or type 'exit' to quit):

QUESTION: What was Company X's revenue?
ANSWER: Revenue was 10 million dollars.

QUESTION: How many customers do we have in 2024?
ANSWER: I don't have the necessary information to answer your question.
```

## Project Structure

```
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── document.pdf
├── README.md
└── src/
    ├── ingest.py    # PDF ingestion into pgvector
    ├── search.py    # Similarity search and QA chain
    ├── chat.py      # Interactive CLI
    ├── config.py    # Environment and settings
    ├── prompts.py   # Grounded QA prompt template
    ├── db.py        # pgvector store
    ├── embeddings.py
    ├── llm.py
    └── utils.py
```
