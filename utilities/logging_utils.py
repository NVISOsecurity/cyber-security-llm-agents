""" Logging utility functions """

import logging as _logging
import sys
import datetime
import json

from utilities import config_utils

from crewai.telemetry import Telemetry


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

    # Create a logger
    logger = _logging.getLogger("cyber-security-llm-agents")
    logger.setLevel(_logging_level)
    logger.propagate = (
        False  # This prevents double logging by not propagating to root logger
    )

    # Create a handler with the desired settings
    handler = _logging.StreamHandler(sys.stdout)
    handler.setLevel(_logging_level)
    formatter = _logging.Formatter(
        "%(asctime)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Set the logging level for the "httpx" logger to WARNING
    _logging.getLogger("httpx").setLevel(_logging.WARNING)

    # Make sure we don't duplicate log messages by removing any default handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Add the new handler to the logger
    logger.addHandler(handler)

    return logger


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


def noop(*args, **kwargs):
    # with open("./logfile.txt", "a") as f:
    #     f.write("Telemetry method called and noop'd\n")
    pass


# Disable telemetry calls in crewai
for attr in dir(Telemetry):
    if callable(getattr(Telemetry, attr)) and not attr.startswith("__"):
        setattr(Telemetry, attr, noop)


logger = setup_logging()
