# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
# Github: https://github.com/ksiddiqui
# LinkedIn: https://www.linkedin.com/in/ksiddiqui
# Email: kashif.ali.siddiqui@gmail.com
# Dated: July, 2025 
# -----------------------------------------------------------------------------
# This source code is the property of Kashif Ali Siddiqui and is confidential.
# Unauthorized copying or distribution of this file, via any medium, is strictly prohibited.
# =============================================================================

from typing import List, Tuple, Dict, Any

from llama_index.core import Settings, QueryBundle, get_response_synthesizer, StorageContext, Document, VectorStoreIndex
from llama_index.core.schema import NodeWithScore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
import numpy as np

from system.setup import get_config_logger
from services.vectorstore import VectorStoreManager
from models.documents import ProcessedDocument

from services.observability import observability_set_contexts

# === Open Source Embedding model constants ===
EMBEDDING_MODEL_NOMIC = "nomic-embed-text"
EMBEDDING_MODEL_HF_BGE_SMALL = "BAAI/bge-small-en"
EMBEDDING_MODEL_HF_BGE_LARGE = "BAAI/bge-large-en"
EMBEDDING_MODEL_HF_E5_LARGE_V2 = "intfloat/e5-large-v2"
EMBEDDING_MODEL_HF_ALL_MPNET_BASE_V2 = "sentence-transformers/all-mpnet-base-v2"


class RAGManager:
    is_llamaindex_setup = False
    embed_model = None

    def __init__(self):
        self.config, self.logger = get_config_logger()
     
        self._setup_llamaindex()
        
        self.vector_store_manager = VectorStoreManager()
        self.vs_engine = self.vector_store_manager.create_vector_store()
        self.vs_index = self.vector_store_manager.load_index()

    def _setup_llamaindex(self):
        if RAGManager.is_llamaindex_setup:
            return

        RAGManager.embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_HF_BGE_LARGE)

        Settings.embed_model = RAGManager.embed_model
        Settings.chunk_size = int(self.config['chunk_size'])
        Settings.chunk_overlap = int(self.config['chunk_overlap'])

        RAGManager.is_llamaindex_setup = True
    
    def _create_document_from_processed(self, processed_document:ProcessedDocument) -> Document:
        document = None
        
        try:
            # Use markdown content if available, otherwise fallback to text
            content = processed_document.markdown_content
            
            if not content:
                # self.logger.error(f"No content found for document: {processed_document.get('file_name', 'Unknown')}")
                return None
                
            # Create Document with metadata
            document = Document(
                text=content,
                metadata={
                    "source": processed_document.file_path,
                    "filename": processed_document.file_name,
                    "title": processed_document.title,
                    "doc_id": processed_document.doc_id,
                    "sections_count": len(processed_document.sections)
                }
            )
                
            # self.logger.info(f"Successfully created document: {processed_document.get('file_name', 'Unknown')}")
                
        except Exception as e:
            # self.logger.error(f"Error creating document from {processed_document.get('file_name', 'Unknown')}. Exception occurred: {e}")
            pass
        
        return document

    def _index_document(self, file_name:str, document: Document):
        is_sucess = False

        storage_context = StorageContext.from_defaults(vector_store=self.vs_engine)
        parser = SentenceSplitter(
            chunk_size=int(self.config['chunk_size']),
            chunk_overlap=int(self.config['chunk_overlap']),
            separator=" "
        )
        
        nodes = parser.get_nodes_from_documents([document])
        
        chunk_id = 1
        for node in nodes:
            node.metadata.update({                
                "chunk_id": str(chunk_id)
            })
            chunk_id += 1
        
        # self.logger.info(f"Created {len(nodes)} nodes from document {document.get('file_name', 'Unknown')}.")
        
        try:
            self.index = VectorStoreIndex(
                nodes=nodes,
                storage_context=storage_context,
                show_progress=True
            )
            is_sucess = True    
        except Exception as e:
            self.logger.error(f"Error creating index from document {file_name}. Exception occurred: {e}")
            
        return is_sucess

    def ingest_processed_documents(self, list_of_processed_documents: list[ProcessedDocument]):
        self.logger.info(f"Ingesting {len(list_of_processed_documents)} processed documents.")
        self.logger.info("-------------------------------------------------------")

        success_count = 0
        for processed_document in list_of_processed_documents:
            file_name = processed_document.file_name
            self.logger.info(f" > Processing document: {file_name}")
            document = self._create_document_from_processed(processed_document)

            if not document:
                self.logger.error(f" > Failed to create document from {file_name}")
                continue

            if self._index_document(file_name, document):
                success_count += 1
            else:
                self.logger.error(f" > Failed to index document {file_name}")

        self.logger.info("-------------------------------------------------------")
        self.logger.info(f"Ingestion completed successfully with {success_count} document(s).")



    def _retrieve_nodes(self, query: str, top_k: int) -> List[NodeWithScore]:

        retriever = VectorIndexRetriever(index=self.vs_index, similarity_top_k=top_k)
        retrieved_nodes = retriever.retrieve(QueryBundle(query_str=query))
        return retrieved_nodes

    def _rerank_results(self, query: str, nodes: List[NodeWithScore], top_k: int) -> List[NodeWithScore]:

        query_emb = np.array(RAGManager.embed_model.get_text_embedding(query))
        node_texts = [node.node.text for node in nodes]
        node_embs = np.array([RAGManager.embed_model.get_text_embedding(node_text) for node_text in node_texts])
        # node_embs = np.array(RAGManager.embed_model.get_text_embeddings(node_texts))

        # Normalize embeddings
        query_emb_norm = query_emb / np.linalg.norm(query_emb)
        node_embs_norm = node_embs / np.linalg.norm(node_embs, axis=1, keepdims=True)

        # Cosine similarities
        similarities = np.dot(node_embs_norm, query_emb_norm)

        # Attach similarity as score, sort, return top_k
        for node, sim in zip(nodes, similarities):
            node.score = float(sim)
        reranked_nodes = sorted(nodes, key=lambda x: x.score or 0, reverse=True)[:top_k]
        return reranked_nodes

    def query_context_retrieval(self, query: str, retrieve_top_k:int=None, rerank_top_k:int=None) -> Tuple[str, List[Dict[str, Any]], List[str], List[Any]]:
        if not retrieve_top_k or retrieve_top_k == 0:
            retrieve_top_k = self.config['top_k_retrieval']
        if not rerank_top_k or rerank_top_k == 0:
            rerank_top_k = self.config['top_k_rerank']

        retrieved_nodes = self._retrieve_nodes(query, top_k=retrieve_top_k)
        reranked_nodes = self._rerank_results(query, retrieved_nodes, top_k=rerank_top_k)

        observability_set_contexts(reranked_nodes)

        context_parts, sources, context_used = [], [], []
        for i, node in enumerate(reranked_nodes):
            context_parts.append(
                f"[Source {i + 1} - {node.node.metadata.get('filename', 'Unknown')}]"
            )
            context_parts.append(f"Section: {node.node.metadata.get('title', 'N/A')}")
            context_parts.append(node.node.text)
            context_parts.append("")

            sources.append(
                {
                    "file_name": node.node.metadata.get("filename"),
                    "section": node.node.metadata.get("title"),
                    "score": node.score,
                    "text": node.node.text,
                }
            )
            context_used.append(node.node.text)

        return "\\n".join(context_parts), sources, context_used, retrieved_nodes