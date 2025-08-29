"""
DevTools - A Python utility library for development tasks
"""

__version__ = "0.1.0"
__author__ = "Robin Magnussen"
__email__ = "your.email@example.com"

# Import main modules for easy access
from .logger import get_logger, setup_logging
from .file_utils import FileUtils
from .data_utils import DataUtils
from .api_utils import APIUtils

__all__ = [
    "get_logger",
    "setup_logging", 
    "FileUtils",
    "DataUtils",
    "APIUtils",
]
