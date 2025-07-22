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

import os
import time
import functools
import inspect
from pathlib import Path
import shutil
from docx2pdf import convert


class BogusDecorator:
    def __call__(self, func):
        return func
    def __getattr__(self, name):
        return self


class FnTraceLogger:
    def __init__(self, log_func=None, custom_text=None, line_enter_pattern='-' * 80, line_exit_pattern='-' * 80):
        self.custom_text = f"{custom_text} " if custom_text else ""
        self.log_func = log_func if log_func else print
        self.line_enter = line_enter_pattern
        self.line_exit = line_exit_pattern
        
    def _log_entry(self, func, args, kwargs):
        arg_lines = []
        for a in args:
            arg_lines.append(f"    {repr(a)}")
        for k, v in kwargs.items():
            arg_lines.append(f"    {k}={v!r}")
        formatted_args =  "\n".join(arg_lines) if arg_lines else ""
        
        text = f"/ ENTR {self.custom_text}{func.__name__} /"
        self.log_func('')
        self.log_func(self.line_enter[:3] + text + self.line_enter[3+len(text):])
        self.log_func(formatted_args)
        
    def _log_exit(self, func, result):
        text = f"/ EXIT {self.custom_text}{func.__name__} /"
        self.log_func(self.line_exit[:3] + text + self.line_exit[3+len(text):])
        self.log_func(f"{result!r}")
        self.log_func('')

    def __call__(self, func):
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            self._log_entry(func, args, kwargs)
            result = func(*args, **kwargs)
            self._log_exit(func, result)
            return result
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            self._log_entry(func, args, kwargs)
            result = await func(*args, **kwargs)
            self._log_exit(func, result)
            return result
        
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


class Timer:
    def __init__(self, task_name=None, logger=None):
        self.task_name = task_name
        self.logger = logger
        self.start = None
        self.end = None
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
        message = f"[Timer] {self.task_name or 'Elapsed time'}: {self.elapsed:.4f} seconds"
        if self.logger:
            self.logger.info(message)
        else:
            print(message)


def convert_docx_to_pdf(file_path: str, delete_original: bool=False):
    # Ensure the file exists and is a DOCX file
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if file_path.suffix.lower() != '.docx':
        raise ValueError(f"File is not a DOCX file: {file_path}")
    
    # Create the output PDF path with the same name but .pdf extension
    pdf_path = file_path.with_suffix('.pdf')
    
    try:
        # Convert DOCX to PDF using docx2pdf
        convert(file_path, pdf_path)
        
        # Check if the PDF was created successfully
        if pdf_path.exists():
            # Delete the original file if requested
            if delete_original:
                os.remove(file_path)
            
            return str(pdf_path), 'application/pdf'
        else:
            return None, None
    except Exception as e:
        print(f"Error converting DOCX to PDF: {e}")
        return None, None


def zip_directory(target_directory: str, zip_file_path: str, ignore_if_zip_file_present: bool=True) -> bool:
        
    try:
        # Make sure the output directory exists
        if not os.path.exists(target_directory):
            return False
        
        if os.path.exists(zip_file_path):
            if ignore_if_zip_file_present:
                return True
            os.remove(zip_file_path)
        
        # Create parent directories for zip_file_path if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(zip_file_path)), exist_ok=True)
        
        # Create the zip file
        shutil.make_archive(
            base_name=os.path.splitext(zip_file_path)[0],   # Base name (without extension)
            format='zip',                                   # Format
            root_dir=target_directory                       # Root directory to zip
        )
        
        return True
        
    except Exception:
        return False