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

import sys
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.documents import ProcessedDocument
from models.database import Base, Document
from models.database import DATABASE_NAME, TABLE_NAME_DOCUMENT, TABLE_NAME_EMBEDDING, CHECK_DATABASE_QUERY, CREATE_DATABASE_QUERY
from system.setup import get_config_logger



class DatabaseManager:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.engine = None
        self.vector_store = None

        self.create_database_if_not_exists()

    def create_database_if_not_exists(self):
        query_check_database = text(CHECK_DATABASE_QUERY.strip())
        query_create_database = text(CREATE_DATABASE_QUERY.strip())
        
        need_to_create_database = False
        try:
            # Step 1: Connect to server-level DB (usually 'postgres')
            server_conn_str = self.config['postgresql_conn_str'].replace(DATABASE_NAME, 'postgres')
            server_engine = create_engine(server_conn_str)
            with server_engine.connect() as connection:
                connection = connection.execution_options(isolation_level="AUTOCOMMIT")
                result = connection.execute(query_check_database)
                if not result.scalar():
                    connection.execute(query_create_database)
                    self.logger.info(f"Ensured database '{DATABASE_NAME}' exists.")
                    need_to_create_database = True
            server_engine.dispose()

            # Step 2: Connect to intended DB and create table
            if self.engine is None:
                self.create_connection()
            Base.metadata.create_all(self.engine)
        except Exception as e:
            self.logger.error(f"Failed to create/check the database and its tables: {e}")
        finally:
            self.close_connection()
        return need_to_create_database

    def create_connection(self):
        try:
            self.engine = create_engine(self.config['postgresql_conn_str'])
            self.logger.info("Database connection created successfully.")
        except Exception as e:
            self.logger.error(f"Failed to create database connection: {e}")
            raise
        return self.engine

    def close_connection(self):
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database connection closed successfully.")

    def get_connection(self):
        return self.engine

    def check_connection(self) -> bool:
        valid_connection = False
        try:
            if self.engine is None:
                self.create_connection()
            with self.engine as connection:
                connection.execute(text("SELECT 1"))
                self.logger.info("Database connection checked successfully.")
                valid_connection = True
        except Exception as e:
            self.logger.error(f"Failed to check database connection: {e}")
        finally:
            self.close_connection()
        return valid_connection

    def view_documents(self):
        documents = []
        try:
            if self.engine is None:
                self.create_connection()
            Session = sessionmaker(bind=self.engine)
            session = Session()
            documents = session.query(Document).all()
            session.close()
        except Exception as e:
            self.logger.error(f"Failed to view documents: {e}")
        finally:
            self.close_connection()
        return documents

    def delete_all_documents(self, delete_indices_also=True):
        try:
            if self.engine is None:
                self.create_connection()
            Session = sessionmaker(bind=self.engine)
            session = Session()
            # Delete all records from the documents table using raw SQL
            session.execute(text(f"DELETE FROM {TABLE_NAME_DOCUMENT}"))
            if delete_indices_also:
                # Delete all records from the embeddings table using raw SQL
                session.execute(text(f"DELETE FROM {TABLE_NAME_EMBEDDING}"))
            session.commit()
            session.close()
        except Exception as e:
            self.logger.error(f"Failed to delete all documents: {e}")
        finally:
            self.close_connection()
        return True
    
    def save_processed_document(self, processed_document:ProcessedDocument):
        try:
            if self.engine is None:
                self.create_connection()
            Session = sessionmaker(bind=self.engine)
            session = Session()
            document = Document(
                name=processed_document.file_name,
                path=processed_document.file_path,
                created_at=processed_document.metadata.created_at,
                num_of_nodes=0,
                content_text=processed_document.text_content,
                content_md=processed_document.markdown_content,
            )
            session.add(document)
            session.commit()
            processed_document.doc_id = document.id
            session.close()
            
            return processed_document
        
        except Exception as e:
            self.logger.error(f"Failed to save processed document to database: {e}")
            return None
        