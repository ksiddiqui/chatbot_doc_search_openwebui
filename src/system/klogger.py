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
import logging

from rich.logging import RichHandler
from rich.console import Console
from rich.text import Text


# Define a new level
DEV_TRACE_LEVEL = 14
DEV_DEBUG_LEVEL = 15

DEFAULT_LOG_FORMAT_MSG = "%(message)s"
DEFAULT_LOG_FORMAT_LEVEL_MSG = '%(levelname)s - %(message)s'
DEFAULT_LOG_FORMAT_LEVEL_TIME_MSG = '%(levelname)s - %(asctime)s - %(message)s'

console = Console()   # Create a custom console with no background colors

class MyCustomLogRenderer(RichHandler):     
    def render_message(self, record: logging.LogRecord, message: str) -> Text:
        text = Text(message)
        
        if record.levelno == logging.DEBUG:
            text.stylize("bright_black")
        elif record.levelno == DEV_TRACE_LEVEL:
            text.stylize("bright_black") 
        elif record.levelno == DEV_DEBUG_LEVEL:
            text.stylize("blue") 
        elif record.levelno == logging.INFO:
            text.stylize("bright_blue")
        elif record.levelno == logging.WARNING:
            text.stylize("yellow")
        elif record.levelno == logging.ERROR:
            # text.stylize("bold red on white")  # Red text on white background
            text.stylize("red")  # Red text on white background
        elif record.levelno == logging.CRITICAL:
            text.stylize("bold red")       
        else:
            text.stylize("")  # Just white background for other levels
            
        return text
    

def logger_dev_trace(self, message, *args, **kwargs):
    if self.isEnabledFor(DEV_TRACE_LEVEL):
        self._log(DEV_TRACE_LEVEL, message, args, **kwargs)

def logger_dev_debug(self, message, *args, **kwargs):
    if self.isEnabledFor(DEV_DEBUG_LEVEL):
        self._log(DEV_DEBUG_LEVEL, message, args, **kwargs)

def setup_klogger(
    log_name:str, log_level: int = DEV_DEBUG_LEVEL, log_format:str=None, 
    enable_console_logging:bool=False, enable_file_logging:bool=False, log_file_path:str=None,
    enable_important_file_logging:bool=False, important_log_file_path:str=None,
    log_testing:bool=False):
    
    if log_format is None:
        log_format = DEFAULT_LOG_FORMAT_LEVEL_MSG
    log_formatter = logging.Formatter(log_format)
    
    logging.addLevelName(DEV_TRACE_LEVEL, "DTRACE") 
    logging.Logger.dev_trace = logger_dev_trace
    logging.addLevelName(DEV_DEBUG_LEVEL, "DDEBUG")  
    logging.Logger.dev_debug = logger_dev_debug
    
    logging.basicConfig(
        level=log_level,     # Set logging level to DEBUG or any other level
        force=True,                   # To force immediate flush of log messages from buffer
        format=log_format,         # Customize the log message format
        # datefmt="[%X]",
        handlers=[MyCustomLogRenderer(
            console=console,
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_level=True,
            show_path=False,                        
        )]  # Use RichHandler to enable rich text logging
    )
    logger = logging.getLogger(log_name)
    
    if enable_console_logging and not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(log_formatter)
        logger.addHandler(console_handler)

    if enable_file_logging:
        if log_file_path is None:
            log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app.log'))
        try:
            file_handler = logging.FileHandler(log_file_path)
            file_handler.setLevel(log_level)
            file_handler.setFormatter(log_formatter)
            logger.addHandler(file_handler)
            logger.info(f"File logging enabled at: {log_file_path}")
        except Exception as e:
            logger.error(f"Failed to create log file handler at {log_file_path}: {e}")
            
    # Add a separate file handler for WARNING and above log levels
    if enable_important_file_logging:
        if important_log_file_path is None:
            important_log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'warnings.log'))
        try:
            important_file_handler = logging.FileHandler(important_log_file_path)
            important_file_handler.setLevel(logging.WARNING)  # Only log WARNING and above
            important_file_handler.setFormatter(log_formatter)
            logger.addHandler(important_file_handler)
            logger.info(f"Important-level file logging enabled at: {important_log_file_path}")
        except Exception as e:
            logger.error(f"Failed to create important log file handler at {important_log_file_path}: {e}")
    
    if log_testing:
        logger.info("***** Testing logs *****")
        logger.debug("testing debug log")
        logger.dev_trace("testing dev_trace (custom) log")
        logger.dev_debug("testing dev_debug (custom) log")
        logger.info("testing info log")
        logger.warning("testing warning log")
        logger.error("testing error log")
        logger.critical("testing critical log")
        logger.info("************************")
    
    return logger

