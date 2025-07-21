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

import warnings
warnings.filterwarnings("ignore", message=".*pin_memory.*")

from typing import Optional, List, Dict, Any
from pathlib import Path
import json

from docling.document_converter import DocumentConverter

from system.setup import get_config_logger
from models.documents import ProcessedDocument
from services.database import DatabaseManager
from services.vectorstore import VectorStoreManager
from services.rag import RAGManager

class DocumentIndexingManager:
    def __init__(self):
        self.config, self.logger = get_config_logger()
        self.input_dir_path = Path(self.config['data_folder_raw'])
        self.output_dir_path = Path(self.config['data_folder_processed'])

        self.db_manager = DatabaseManager()
        self.vector_store_manager = VectorStoreManager()
        self.rag_manager = RAGManager()

        self.document_converter = DocumentConverter()
        self._check_directories()

    def _check_directories(self):
        if not self.input_dir_path.exists():
            self.logger.error(f"Input directory does not exist: {self.input_dir_path}")
            self.input_dir_path.mkdir(parents=True, exist_ok=True)
        if not self.output_dir_path.exists():
            self.logger.error(f"Output directory does not exist: {self.output_dir_path}")
            self.output_dir_path.mkdir(parents=True, exist_ok=True)

    def _get_input_files(self):
        input_files = list(self.input_dir_path.glob("*.*"))
        self.logger.info(f"Found {len(input_files)} files in the input directory '{self.input_dir_path}'")
        for file in input_files:
            self.logger.info(f"  - {file.name}")    
        return input_files


    def _do_convert_any_to_pdf(self, document_path:Path):
        # get externsion of the file
        ext = document_path.name.split(".")[-1]
        if not ext or len(ext) == 0:
            return None
        ext = ext.lower()

        if ext == "pdf":
            return document_path        
        if ext == "docx":
            return self._do_convert_docx_to_pdf(document_path)

        return None

    def _do_convert_docx_to_pdf(self, document_path:str):
        return None

    def _do_load_processed_document(self, document:Path):
        # get the document name only
        document_name = document.name
        document_name = document_name.split(".")[0]
        processed_file_json = Path(self.output_dir_path / f"{document_name}_processed.json")
        processed_file_md = Path(self.output_dir_path / f"{document_name}.md")

        if processed_file_json.exists() and processed_file_md.exists():
            with open(processed_file_json, "r", encoding="utf-8") as f:
                processed_data = json.load(f)
            return ProcessedDocument.create_from_dict(processed_data)

        return None

    def _do_convert_pdf_to_md(self, file_path:Path):
        processed_data = None
        file_name_without_ext = file_path.stem
        try:
            self.logger.info(f"Processing file: {file_path.name} using Docling")

            result = self.document_converter.convert(str(file_path))
            if not result or not result.document:
                self.logger.error(f"Failed to convert PDF: {file_path}")
                return None

            document = result.document
            txt_exported = document.export_to_text()
            md_exported = document.export_to_markdown()
            title = self._md_content_extract_title(txt_exported, file_name_without_ext)
            sections = self._md_content_extract_sections(md_exported)
            processed_data = ProcessedDocument.create_from_document(file_path, document, txt_exported, md_exported, title, sections)

            # Save to output folder
            output_file = self.output_dir_path / f"{file_name_without_ext}_processed.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(processed_data.to_dict(), f, indent=2, ensure_ascii=False)

            # save markdown file here
            markdown_file = self.output_dir_path / f"{file_name_without_ext}.md"
            with open(markdown_file, "w", encoding="utf-8") as f:
                f.write(md_exported)

            self.logger.info(f"Processed {file_path.name} -> {output_file.name}")
        
        except Exception as e:
            self.logger.error(f"Error processing {file_path.name}: {e}")
            processed_data = ProcessedDocument.create_from_dict({
                "file_name": file_path.name,
                "file_path": str(file_path),
                "title": file_name_without_ext,
                "markdown_content": "",
                "text_content": "",
                "sections": [],
                "metadata": {
                    "original_file": file_path.name,
                    "processed_successfully": False,
                    "error": str(e),
                },
            })
        
        return processed_data
    
    def _md_content_extract_title(self, document_text, default_title: str) -> str:
        try:
            lines = document_text.split("\n")

            for line in lines[:10]:
                line = line.strip()
                if line and len(line) > 3:
                    return line

            return default_title
        except:
            return default_title

    def _md_content_extract_sections(self, markdown_content: str) -> List[Dict[str, Any]]:
        sections = []
        lines = markdown_content.split("\n")
        current_section = None

        for line in lines:
            if line.startswith("#"):
                if current_section:
                    sections.append(current_section)
                header_level = len(line) - len(line.lstrip("#"))
                title = line.lstrip("#").strip()
                current_section = {"title": title, "level": header_level, "content": []}
            elif current_section and line.strip():
                current_section["content"].append(line)

        if current_section:
            sections.append(current_section)

        if not sections and markdown_content.strip():
            sections.append(
                {
                    "title": "Main Content",
                    "level": 1,
                    "content": markdown_content.split("\n"),
                }
            )

        return sections

    def _save_processed_documents_to_database(self, processed_document:ProcessedDocument):
        try:
            processed_document = self.db_manager.save_processed_document(processed_document)
            return processed_document
        except Exception as e:
            self.logger.error(f"Failed to save processed document to database. Exception occurred: {e}")
            return None
        
    def _index_processed_documents_to_vector_store(self, processed_document_list:list[ProcessedDocument]):
        try:
            self.rag_manager.ingest_processed_documents(processed_document_list)
        except Exception as e:
            self.logger.error(f"Failed to index processed document to vector store. Exception occurred: {e}")

    def start_indexing_from_directory(self):
        # Step 1: Get all the files ...
        input_files = self._get_input_files()

        converted_files = []
        # Step 2: Convert all the files to PDF ...
        for input_file in input_files:
            converted_file = self._do_convert_any_to_pdf(input_file)
            if converted_file:
                converted_files.append(converted_file)
        
        input_files = converted_files
        processed_documents = []        
        # Step 3: Process each PDF file 
        for input_file in input_files:
            processed_document = self._do_load_processed_document(input_file)
            if not processed_document:
                processed_document = self._do_convert_pdf_to_md(input_file)
            if processed_document:
                processed_documents.append(processed_document)

        # Step 4: Save processed documents to database
        for processed_document in processed_documents:
            upd_processed_document = self._save_processed_documents_to_database(processed_document)
            if upd_processed_document:
                processed_document.doc_id = upd_processed_document.doc_id

        # Step 5: Index processed documents to vector store
        self._index_processed_documents_to_vector_store(processed_documents)

        return processed_documents