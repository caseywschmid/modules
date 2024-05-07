import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()


# Flag to toggle detailed console output
DETAILED_CONSOLE_OUTPUT = bool(os.getenv("DETAILED_CONSOLE_OUTPUT", False))

# ------------------------------------------------------
#                 Define the FINE level
# ------------------------------------------------------
"""
FINE is a custom log level that is between DEBUG and INFO
"""
FINE_LEVEL = 15
logging.addLevelName(FINE_LEVEL, "FINE")


def fine(self, message, *args, **kwargs):
    if self.isEnabledFor(FINE_LEVEL):
        self._log(FINE_LEVEL, message, args, **kwargs)


logging.Logger.fine = fine


# ------------------------------------------------------
#              Define the STEP level
# ------------------------------------------------------
"""
STEP is a custom log level that is between INFO and WARNING
"""
STEP_LEVEL = 25
logging.addLevelName(STEP_LEVEL, "STEP")


def step(self, message, *args, **kwargs):
    if self.isEnabledFor(STEP_LEVEL):
        self._log(STEP_LEVEL, message, args, **kwargs)


logging.Logger.step = step


# ------------------------------------------------------
#         Define custom log format for terminal
# ------------------------------------------------------
class ConsoleFormatter(logging.Formatter):
    level_formats = {
        logging.DEBUG: "\x1b[38;21mDEBUG\x1b[0m:\t  %(message)s",  # Grey Level
        FINE_LEVEL: "\x1b[34mFINE\x1b[0m:\t  %(message)s",  # Blue Level
        logging.INFO: "\x1b[32mINFO\x1b[0m:\t  %(message)s",  # Green Level
        STEP_LEVEL: "\x1b[35mSTEP\x1b[0m:\t  \x1b[35m%(message)s\x1b[0m",  # Purple Level and Message
        logging.WARNING: "\x1b[33mWARNING\x1b[0m:  %(message)s",  # Yellow Level
        logging.ERROR: "\x1b[31mERROR\x1b[0m:\t  %(message)s",  # Red Level
        logging.CRITICAL: "\x1b[31;1mCRITICAL\x1b[0m: %(message)s",  # Bold Red Level
    }

    def format(self, record):
        log_fmt = self.level_formats.get(record.levelno, "%(levelname)s: %(message)s")
        if DETAILED_CONSOLE_OUTPUT:
            log_fmt += "\t(%(filename)s:%(lineno)d)\t%(asctime)s"
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# ------------------------------------------------------
#              Define detailed log format
# ------------------------------------------------------
class LogFileFormatter(logging.Formatter):
    detail_format = (
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)"
    )

    def __init__(self, fmt=detail_format, datefmt="%Y-%m-%d %H:%M:%S"):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        return super().format(record)


# ===============
# Logging
# --------------
# DEBUG: 10
# FINE: 15
# INFO: 20
# STEP: 25
# WARNING: 30
# ERROR: 40
# CRITICAL: 50
# ===============

# Function to configure logging
def configure_logging(logger_name="root", keep_logs=False):
    """
    Configures the logging for the application.

    Args:
        logger_name (str, optional): The name of the logger to be configured.
        Defaults to "root".
        log_level (int, optional): The level of logging to be used. Defaults to
        LOG_LEVEL.
        keep_logs (bool, optional): If set to True, logs will be kept in a file.
        Defaults to False.

    """
    # Dynamically read the environment variable
    default_log_level = 15  # Default level if LOG_LEVEL is not set
    log_level = int(os.getenv("LOG_LEVEL", default_log_level))
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    # Check if handlers already exist to prevent duplication
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(ConsoleFormatter())
        logger.addHandler(console_handler)

        if keep_logs:
            # File Handler with detailed messages
            file_handler = RotatingFileHandler(
                "logs/logs.log", maxBytes=5 * 1024 * 1024, backupCount=3
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(LogFileFormatter())
            logger.addHandler(file_handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False
