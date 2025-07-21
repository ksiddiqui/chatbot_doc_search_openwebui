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

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

DATABASE_NAME = "document_search"

TABLE_NAME_DOCUMENT = "document"
TABLE_NAME_EMBEDDING = "data_embedding"

CONNECTION_STRING = f"postgresql://[USER]:[PASS]@[HOST]:[PORT]/{DATABASE_NAME}"

CHECK_DATABASE_QUERY = f"""
SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}';
"""

CREATE_DATABASE_QUERY = f"""
CREATE DATABASE {DATABASE_NAME};
"""


Base = declarative_base()

class Document(Base):
    # __tablename__ = f"{DATABASE_NAME}.{TABLE_NAME_DOCUMENT}"
    __tablename__ = f"{TABLE_NAME_DOCUMENT}"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    path = Column(String(512), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    num_of_nodes = Column(Integer, nullable=False)
    content_text = Column(Text)
    content_md = Column(Text)
