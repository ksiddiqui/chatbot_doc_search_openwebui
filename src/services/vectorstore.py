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

from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext

from system.setup import get_config_logger
from models.database import TABLE_NAME_EMBEDDING

class VectorStoreManager:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.vector_store = None
        self.index = None

    def create_vector_store(self):
        self.vector_store = None
        try:
            self.vector_store = PGVectorStore.from_params(
                database=self.config['postgresql_db'],
                host=self.config['postgresql_host'],
                password=self.config['postgresql_pass'],
                port=int(self.config['postgresql_port']),
                user=self.config['postgresql_user'],
                table_name=TABLE_NAME_EMBEDDING,
                # embed_dim=1536, 
                embed_dim=1024,
                hnsw_kwargs={
                    "hnsw_m": 16, # The number of bi-directional connections created for each node in the graph
                    "hnsw_ef_construction": 64, # how many neighbors are considered when inserting a new node.
                    "hnsw_ef_search": 40, # how many candidates are considered in the graph during a query
                }
            )
            self.logger.info("Vector store created successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create vector store: {e}")
        return self.vector_store

    def load_index(self):
        if not self.vector_store:
            self.create_vector_store()

        try:
            self.index = VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
            self.logger.info("Index loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load index: {e}")

        return self.index

    def check_connection(self):
        return DatabaseManager().check_connection()

    def reset_vector_store(self):
        return DatabaseManager().delete_all_documents(delete_indices_also=True)