import logging
import os
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.INFO)

    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "client.log")

    formatter = logging.Formatter(
        fmt="[%Y-%m-%d %H:%M:%S] CLIENT %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger
