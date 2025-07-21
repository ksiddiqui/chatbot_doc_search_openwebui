# =============================================================================
# © 2025 Kashif Ali Siddiqui, Pakistan
# Developed by: Kashif Ali Siddiqui 
#
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
import yaml
from dotenv import load_dotenv

from models.database import CONNECTION_STRING

CONFIG_FILE_PATH = "../../config.yaml"

CONFIG_MAP = [
    # Logging settings
    {'conf_name': 'log_level', 'env_name': 'LOG_LEVEL', 'default_value': 'INFO', 'is_required': False},
    {'conf_name': 'log_format', 'env_name': 'LOG_FORMAT', 'default_value': '%(levelname)s - %(message)s', 'is_required': False},
    {'conf_name': 'log_file_path', 'env_name': 'LOG_FILE_PATH', 'default_value': 'app.log', 'is_required': False},
    {'conf_name': 'log_important_file_path', 'env_name': 'LOG_IMPORTANT_FILE_PATH', 'default_value': 'warnings.log', 'is_required': False},
    {'conf_name': 'log_testing', 'env_name': 'LOG_TESTING', 'default_value': False, 'is_required': False},
    # FastAPI settings
    {'conf_name': 'fastapi_host', 'env_name': 'FASTAPI_HOST', 'default_value': 'localhost', 'is_required': True},
    {'conf_name': 'fastapi_port', 'env_name': 'FASTAPI_PORT', 'default_value': 8000, 'is_required': True},
    {'conf_name': 'fastapi_debug', 'env_name': 'FASTAPI_DEBUG', 'default_value': True, 'is_required': True},
    {'conf_name': 'fastapi_reload', 'env_name': 'FASTAPI_RELOAD', 'default_value': True, 'is_required': True},
    {'conf_name': 'restapi_prefix', 'env_name': 'RESTAPI_PREFIX', 'default_value': '/api/v1', 'is_required': True},
    {'conf_name': 'web_prefix', 'env_name': 'WEB_PREFIX', 'default_value': None, 'is_required': False},
    
    # Document files settings
    {'conf_name': 'data_folder_raw', 'env_name': 'DATA_FOLDER_RAW', 'default_value': 'data/raw', 'is_required': True},
    {'conf_name': 'data_folder_processed', 'env_name': 'DATA_FOLDER_PROCESSED', 'default_value': 'data/processed', 'is_required': True},
    
    # PostgreSQL settings
    {'conf_name': 'postgresql_host', 'env_name': 'POSTGRES_HOST', 'default_value': 'localhost', 'is_required': True},
    {'conf_name': 'postgresql_port', 'env_name': 'POSTGRES_PORT', 'default_value': 5432, 'is_required': True},
    {'conf_name': 'postgresql_db', 'env_name': 'POSTGRES_DB', 'default_value': None, 'is_required': False},
    {'conf_name': 'postgresql_user', 'env_name': 'POSTGRES_USER', 'default_value': None, 'is_required': False},
    {'conf_name': 'postgresql_pass', 'env_name': 'POSTGRES_PASSWORD', 'default_value': None, 'is_required': False},
    {'conf_name': 'postgresql_conn_str', 'env_name': None, 'default_value': None, 'is_required': False},

    # # Database tables settings
    # {'conf_name': 'db_table_files', 'env_name': 'DB_TABLE_FILES', 'default_value': 'documents_meta', 'is_required': True},
    # {'conf_name': 'db_table_embeddings', 'env_name': 'DB_TABLE_EMBEDDINGS', 'default_value': 'documents_embeddings', 'is_required': True},

    # Indexing settings
    {'conf_name': 'model_embedding', 'env_name': 'EMBEDDING_MODEL', 'default_value': 'BAAI/bge-large-en', 'is_required': True},

    {'conf_name': 'chunk_size', 'env_name': 'CHUNK_SIZE', 'default_value': 1000, 'is_required': True},
    {'conf_name': 'chunk_overlap', 'env_name': 'CHUNK_OVERLAP', 'default_value': 200, 'is_required': True},
    {'conf_name': 'top_k_retrieval', 'env_name': 'TOP_K_RETRIEVAL', 'default_value': 10, 'is_required': True},
    {'conf_name': 'top_k_rerank', 'env_name': 'TOP_K_RERANK', 'default_value': 3, 'is_required': True},

]

class ConfigLoader:    
    def __init__(self, load_from_config=True, load_from_env=True) -> None:
        self.my_config = {}

        if load_from_config:
            self._load_from_config_file()

        if load_from_env:
            self._load_from_environment()

        self._validate_config()
        if not self.my_config.get('postgresql_conn_str'):
            connection_string = CONNECTION_STRING.replace("[USER]", self.my_config['postgresql_user'])\
                                .replace("[PASS]", self.my_config['postgresql_pass'])\
                                .replace("[HOST]", self.my_config['postgresql_host'])\
                                .replace("[PORT]", str(self.my_config['postgresql_port']))
            self.my_config['postgresql_conn_str'] = connection_string


    def _validate_config(self):
        for config in CONFIG_MAP:
            if config['is_required'] and config['conf_name'] not in self.my_config:
                raise ValueError(f"Configuration key '{config['conf_name']}' is required but not found in the configuration.")

    def _load_from_config_file(self):
        new_config = {}
        with open(os.path.join(os.path.dirname(__file__), CONFIG_FILE_PATH), 'r') as f:
            new_config = yaml.safe_load(f)
        
        new_config = new_config.get('config', {})
        for config in CONFIG_MAP:
            if config['conf_name'] in new_config:
                self.my_config[config['conf_name']] = new_config[config['conf_name']]

    def _load_from_environment(self):
        for config in CONFIG_MAP:
            env_var_name = config['env_name']
            if env_var_name is None or env_var_name not in os.environ:
                continue
            new_config_value = os.getenv(env_var_name, config['default_value'])
            if new_config_value:
                self.my_config[config['conf_name']] = new_config_value

    def get_config(self):
        return self.my_config
