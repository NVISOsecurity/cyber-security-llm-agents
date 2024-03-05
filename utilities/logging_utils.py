""" Logging utility functions """

import logging as _logging
import sys

from utilities import config_utils


def setup_logging():
    """Setup logging with INFO level."""

    # Get the logging level based on on the configuration we set
    if config_utils.LOGGING_LEVEL == "DEBUG":
        _logging_level = _logging.DEBUG
    elif config_utils.LOGGING_LEVEL == "INFO":
        _logging_level = _logging.INFO
    elif config_utils.LOGGING_LEVEL == "WARNING":
        _logging_level = _logging.WARNING
    elif config_utils.LOGGING_LEVEL == "ERROR":
        _logging_level = _logging.ERROR
    elif config_utils.LOGGING_LEVEL == "CRITICAL":
        _logging_level = _logging.CRITICAL
    else:
        _logging_level = _logging.INFO

    _logging.basicConfig(
        level=_logging_level,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    _logging.getLogger("httpx").setLevel(_logging.WARNING)
    return _logging.getLogger("CALDERA GPT")


def print_banner(title):
    """Print a banner to the console"""
    logger.info("=" * len(title))
    logger.info(title)
    logger.info("=" * len(title))


def print_section(title):
    """Print a section to the console"""
    logger.info("")
    logger.info(title)
    logger.info("-" * len(title))


logger = setup_logging()
