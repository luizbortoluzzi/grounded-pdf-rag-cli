# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-03-23

### Added

- PDF ingestion pipeline (load, split, embed, store in pgvector)
- Interactive chat CLI with grounded QA
- Similarity search with k=10 retrieval
- Configuration validation on startup
- Custom exception hierarchy (ConfigError, IngestionError, SearchError, DatabaseError)
- Logging throughout ingestion and chat
- Complete type hints across all modules
- Unit tests for config, prompts, utils, exceptions
- pyproject.toml with pytest and ruff configuration
- Makefile for common development tasks
- ARCHITECTURE.md documenting the system design
- GitHub Actions CI for tests and linting

### Technical Details

- Chunk size: 1000 characters, overlap: 150
- Embedding model: text-embedding-3-small
- Chat model: gpt-4o-mini
- Fallback answer: "I don't have the necessary information to answer your question."
