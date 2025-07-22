# ChatBot Doc Search – Contextual RAG Pipeline

## Overview

This project is an interactive chatbot platform leveraging a contextual Retrieval-Augmented Generation (RAG) pipeline. It enables users to query and interact with document collections using advanced LLMs, semantic search, and agent orchestration. The system is modular, extensible, and designed for both experimentation and production deployment.

---

## Tech Stack

- **Python 3.10+**
- **LlamaIndex** (indexing & retrieval)
- **PGVector** (vector storage in PostgreSQL)
- **psycopg2** (PostgreSQL adapter)
- **CrewAI** (agent orchestration)
- **Ollama** (local LLM serving)
- **Arize Phoenix** (prompt playground & chatbot UI)
- **RAGAs** (retrieval evaluation & tracing)
- **Docling** (document parsing)
- **Open WebUI** (frontend interface)
- **PostgreSQL** (database)
- **Batch scripts** (`run.bat` for automation)
- **Other**: pandas, JSON, etc.

---

## Prototype Requirements

The following phases summarize the prototype requirements (see [`docs/prd.md`](docs/prd.md) for full details):

1. **Project Setup**: Git repo, Python environment, core dependencies.
2. **Document Ingestion**: Parse and clean documents using Docling.
3. **Embedding Storage**: PostgreSQL with PGVector, embeddings via Ollama.
4. **Indexing & Retrieval**: LlamaIndex integration, vector-based retrieval.
5. **Contextual RAG**: Retrieval-augmented generation, multi-pass contextualization, re-ranking.
6. **Agentic Framework**: Crew.AI for agent roles and orchestration.
7. **Prompt Evaluation**: Arize Phoenix, prompt logging, RAGAs scoring.
8. **Chatbot Interface**: Integration with Arize Phoenix UI, backend connection, Open WebUI deployment.
9. **Documentation & Packaging**: Setup guides, usage docs, deployment instructions.
10. **Final Submission**: Ensure deliverables, submit code/docs, and prepare for demo.

---

## Installation

To set up the project and install all dependencies, simply run:

```bash
run.bat
```

This script will:
- Set up your Python environment (virtualenv/conda)
- Install all required Python packages
- Prepare the database and other services as needed

> _Note: Ensure you have Python 3.10+ and PostgreSQL installed on your system._

---

## Running the Software

### 1. Run the UI

To launch the Open WebUI interface:
```bash
# From the project root
run.bat ui
```
Or, open the Open WebUI executable directly if available.

### 2. Run the Server

To start the backend server (RAG pipeline, LLM, etc.):
```bash
run.bat server
```
This will launch the main server process, connecting to the database and LLM.

### 3. Admin Utility

For administrative tasks (database management, ingestion, etc.):
```bash
run.bat admin
```
Follow the prompts or consult the documentation for available admin commands.

---

## Usage

1. **Ingest Documents**: Use the admin utility to parse and load documents into the system.
2. **Query via UI**: Access the chatbot via Open WebUI, ask questions, and receive context-rich answers.
3. **Monitor & Evaluate**: Use the Arize Phoenix playground for prompt evaluation and debugging.

---

## Contributing

Pull requests and issues are welcome! Please see CONTRIBUTING.md (if available) for guidelines.
