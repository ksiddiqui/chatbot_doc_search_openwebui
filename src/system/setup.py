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

# import sys
import os

from dotenv import load_dotenv

from system.config import ConfigLoader
from system.klogger import setup_klogger
from system.utils import FnTraceLogger

config_loader: ConfigLoader = None
config = None
logger = None
http_call_tracer = None

def do_setup():
    global config_loader, config, logger, http_call_tracer

    load_dotenv()

    config_loader = ConfigLoader(load_from_config=True, load_from_env=False)
    config = config_loader.get_config()

    logger = setup_klogger(
        log_name="percepta", 
        log_level=config['log_level'], 
        log_format=config['log_format'], 
        
        enable_console_logging=False, 
        enable_file_logging=False, 
        log_file_path=None, 
        enable_important_file_logging=True,
        important_log_file_path=config['log_important_file_path'],
        log_testing=config['log_testing'],
    )
    logger.info(f"Current working directory: {os.getcwd()}")

    # http_call_tracer = FnTraceLogger(log_func=logger.info, custom_text="<HTTP>")

    return config, logger


def get_config_logger():
    return config, logger

def get_config():
    return config   

def get_logger():
    return logger

def get_http_call_tracer():
    global http_call_tracer
    
    if http_call_tracer is None:
        http_call_tracer = FnTraceLogger(log_func=logger.info, custom_text="<HTTP>")
    return http_call_tracer

