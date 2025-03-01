import logging
import sys
from pathlib import Path

from loguru import logger


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging messages and redirect them to loguru.
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging(log_level="INFO"):
    """
    Configure loguru logger with console and file sinks.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        loguru.logger instance
    """
    # Remove any existing handlers
    logger.remove()
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Define log format
    console_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan> - <level>{message}</level>"
    )
    
    # Add console handler
    logger.add(
        sys.stdout,
        format=console_format,
        level=log_level,
        colorize=True,
    )
    
    # Add file handler
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} - {message}",
        level=log_level,
        rotation="10 MB", 
        retention="1 week",
        compression="gz",
    )
    
    # Configure logging to intercept standard library logs
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "asyncio",
        "starlette",
    ]
    
    # Intercept logs from other libraries
    handler = InterceptHandler()
    for logger_name in loggers:
        _logger = logging.getLogger(logger_name)
        _logger.handlers = [handler]
        _logger.propagate = False
        # Ensure the log level is low enough to capture all messages
        _logger.setLevel(logging.DEBUG)
    
    return logger
