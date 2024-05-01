import os
import logging
from logging import handlers


class Logger:
    """Initializes logger."""

    @staticmethod
    def initialize_logger(export_dir: str) -> None:
        """Initializes INFO logger with handler for output in logs file."""
        logging.basicConfig(level=logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s "
        )
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        log_dir = os.path.join(export_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, "logs.log"), maxBytes=1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)
