"""
Logging utilities for development projects
"""

import logging
import sys
from datetime import datetime
from typing import Optional
from colorama import Fore, Style, init

# Initialize colorama for Windows support
init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""
    
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, '')
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)


def setup_logging(
    level: str = "INFO",
    format_str: Optional[str] = None,
    colored: bool = True,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging with optional colors and file output
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format_str: Custom format string
        colored: Whether to use colored output
        log_file: Optional file to write logs to
        
    Returns:
        Configured logger instance
    """
    if format_str is None:
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logger = logging.getLogger("devtools")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if colored:
        console_handler.setFormatter(ColoredFormatter(format_str))
    else:
        console_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(console_handler)
    
    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(format_str))
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "devtools", level: str = "INFO") -> logging.Logger:
    """
    Get a logger instance with default configuration
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        setup_logging(level)
    return logger


class DevLogger:
    """
    A simple wrapper for common development logging patterns
    """
    
    def __init__(self, name: str = "devtools"):
        self.logger = get_logger(name)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
    
    def success(self, message: str):
        """Log success message (as info with green color)"""
        self.logger.info(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")
    
    def step(self, message: str):
        """Log step message (as info with blue color)"""
        self.logger.info(f"{Fore.BLUE}🔄 {message}{Style.RESET_ALL}")
    
    def timestamp(self, message: str):
        """Log message with timestamp"""
        now = datetime.now().strftime("%H:%M:%S")
        self.logger.info(f"[{now}] {message}")
