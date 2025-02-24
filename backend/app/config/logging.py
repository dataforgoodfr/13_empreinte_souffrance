import datetime
import json
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }

        if hasattr(record, "request_id"):
            log_obj["request_id"] = record.request_id

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


def setup_logging(log_level=logging.INFO):
    # Create main logger
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    # Avoiding handler duplication
    if logger.handlers:
        return logger

    # Configuration of the console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # Configuration of the file handler
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / "app.log", maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)

    return logger
