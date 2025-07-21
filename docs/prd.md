# ✅ Task List: Interactive Chatbot with Contextual RAG Pipeline

## 🧩 Phase 1: Project Setup
- Initialize Git repository and folder structure
- Set up local Python environment (venv or Conda)
- Install core dependencies
  - llama-index, pgvector, psycopg2, crewai, ollama, arize-phoenix, ragas, etc.

## 📄 Phase 2: Document Ingestion Pipeline
- Install and configure Docling
- Parse the provided documents
- Extract and clean relevant text content
- Store cleaned documents in a temporary data structure (e.g., JSON or pandas)

## 🗃️ Phase 3: Embedding Storage Setup
- Set up PostgreSQL and PGVector extension
- Create schema and tables for vector storage
- Generate embeddings from cleaned text using Ollama-supported model
- Store embeddings into PGVector

## 🔍 Phase 4: Indexing & Retrieval with LlamaIndex
- Integrate LlamaIndex with PGVector
- Build document index from stored vectors
- Test retrieval queries for accuracy and relevance

## 🧠 Phase 5: Contextual RAG Implementation
- Configure local LLM using Ollama
- Implement retrieval-augmented generation logic
- Add Anthropic-style contextualization (multi-pass, semantic expansion)
- Integrate re-ranking logic to improve response quality

## 🤖 Phase 6: Agentic Framework with Crew.AI
- Define agent roles and prompt chains
- Set up Crew.AI to manage prompt orchestration
- Integrate Crew.AI output with RAG pipeline

## 🧪 Phase 7: Prompt Evaluation and Debugging
- Connect Arize Phoenix Prompt Playground
- Log prompt/response data for inspection
- Set up RAGAs tracing and scoring
- Review logs and tune prompts based on insights

## 💬 Phase 8: Chatbot Interface Integration
- Set up Arize Phoenix Chatbot interface
- Integrate backend RAG pipeline with chat UI
- Deploy UI through Open WebUI
- Test chat interactions end-to-end

## 📚 Phase 9: Final Documentation & Packaging
- Write setup and installation instructions
- Add usage documentation (architecture, commands, flow)
- Prepare local deployment guide
- Push everything to GitHub (or prepare ZIP)

## 📦 Phase 10: Final Submission
- ✅ Ensure all deliverables are working and documented
- ✅ Submit the code/repo link and docs before Friday 4:30 PM
- ✅ Prepare short demo/walkthrough for client meeting