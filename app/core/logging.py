"""Centralised logging configuration."""
import logging
import sys


def setup_logging() -> None:
    """Configure root logger with a timestamped, levelled format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


logger = logging.getLogger("finance_backend")
