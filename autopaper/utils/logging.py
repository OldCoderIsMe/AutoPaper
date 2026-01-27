"""Logging configuration for AutoPaper."""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    name: str = "autopaper",
    log_file: Optional[str] = None,
    log_level: int = logging.INFO,
    console_level: int = logging.WARNING
) -> logging.Logger:
    """Configure logging for AutoPaper.

    Args:
        name: Logger name
        log_file: Path to log file (default: data/autopaper.log)
        log_level: Logging level for file (default: INFO)
        console_level: Logging level for console (default: WARNING)

    Returns:
        Configured logger instance

    Examples:
        >>> logger = setup_logging()
        >>> logger.info("Article added successfully")

        >>> logger = setup_logging(log_level=logging.DEBUG)
        >>> logger.debug("Debug information")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels, handlers filter

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter(
        '%(levelname)s - %(message)s'
    )

    # File handler
    if log_file is None:
        # Default to data/autopaper.log
        log_dir = Path("data")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "autopaper.log"

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)

    # Console handler (only warnings and errors)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(console_level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = "autopaper") -> logging.Logger:
    """Get or create a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)

    # Setup logging if not already configured
    if not logger.handlers:
        setup_logging(name)

    return logger


# Module-level logger for convenience
logger = get_logger(__name__)
