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

from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from pydantic import BaseModel

from llama_index.core import Document

class ProcessedDocumentMetadata(BaseModel):
    original_file: str
    processed_successfully: bool
    has_content: bool
    created_at: datetime

    def to_dict(self):
        return {
            'original_file': self.original_file,
            'processed_successfully': self.processed_successfully,
            'has_content': self.has_content,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else self.created_at,
        }

class ProcessedDocument(BaseModel):
    doc_id: str
    file_name: str
    file_path: str
    title: str
    markdown_content: str
    text_content: str
    sections: list
    metadata: ProcessedDocumentMetadata

    def to_dict(self):
        return {
            'doc_id': self.doc_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'title': self.title,
            'markdown_content': self.markdown_content,
            'text_content': self.text_content,
            'sections': self.sections,
            'metadata': self.metadata.to_dict() if hasattr(self.metadata, 'to_dict') else self.metadata,
        }

    @classmethod
    def create_from_dict(cls, data: Dict[str, Any]) -> 'ProcessedDocument':
        metadata = ProcessedDocumentMetadata(**data['metadata'])
        return cls(
            doc_id=data.get('doc_id', ''),
            file_name=data['file_name'],
            file_path=data['file_path'],
            title=data['title'],
            markdown_content=data['markdown_content'],
            text_content=data['text_content'],
            sections=data['sections'],
            metadata=metadata
        )

    @classmethod
    def create_from_document(cls, file_path:Path, document:Document, txt_exported, md_exported, title, sections) -> 'ProcessedDocument':
        return cls(
            doc_id='',
            file_name=file_path.name,
            file_path=str(file_path),
            title=title,
            markdown_content=md_exported,
            text_content=txt_exported,
            sections=sections,
            metadata=ProcessedDocumentMetadata(
                original_file=document.name,
                processed_successfully=True,
                has_content=len(txt_exported.strip()) > 0,
                created_at=datetime.now(),
            ),
        )
            
