import logging
from logging.handlers import RotatingFileHandler


# Flag to toggle detailed console output
DETAILED_CONSOLE_OUTPUT = False  # Set to False to disable detailed logs in the console


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
#              Define the MILESTONE level
# ------------------------------------------------------
"""
MILESTONE is a custom log level that is between INFO and WARNING
"""
MILESTONE_LEVEL = 25
logging.addLevelName(MILESTONE_LEVEL, "MILESTONE")


def milestone(self, message, *args, **kwargs):
    if self.isEnabledFor(MILESTONE_LEVEL):
        self._log(MILESTONE_LEVEL, message, args, **kwargs)


logging.Logger.milestone = milestone


# ------------------------------------------------------
#         Define custom log format for terminal
# ------------------------------------------------------
class ColorLevelFormatter(logging.Formatter):
    level_formats = {
        logging.DEBUG: "\x1b[38;21mDEBUG\x1b[0m:\t  %(message)s",  # Grey Level
        FINE_LEVEL: "\x1b[34mFINE\x1b[0m:\t  %(message)s",  # Blue Level
        logging.INFO: "\x1b[32mINFO\x1b[0m:\t  %(message)s",  # Green Level
        MILESTONE_LEVEL: "\x1b[35mMILESTONE\x1b[0m:\t  \x1b[35m%(message)s\x1b[0m",  # Purple Level and Message
        logging.WARNING: "\x1b[33mWARNING\x1b[0m:  %(message)s",  # Yellow Level
        logging.ERROR: "\x1b[31mERROR\x1b[0m:\t  %(message)s",  # Red Level
        logging.CRITICAL: "\x1b[31;1mCRITICAL\x1b[0m: %(message)s",  # Bold Red Level
    }

    def format(self, record):
        log_fmt = self.level_formats.get(record.levelno, "%(levelname)s: %(message)s")
        if DETAILED_CONSOLE_OUTPUT:
            log_fmt += "\t%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


# ------------------------------------------------------
#              Define detailed log format
# ------------------------------------------------------
class DetailedFormatter(logging.Formatter):
    detail_format = (
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s (%(filename)s:%(lineno)d)"
    )

    def __init__(self, fmt=detail_format, datefmt="%Y-%m-%d %H:%M:%S"):
        super().__init__(fmt=fmt, datefmt=datefmt)

    def format(self, record):
        return super().format(record)


# =======================================================
# Logging
# --------------
# DEBUG: 10
# FINE: 15
# INFO: 20
# MILESTONE: 25
# WARNING: 30
# ERROR: 40
# CRITICAL: 50
# =======================================================
LOG_LEVEL = 15


# Function to configure logging
def configure_logging(logger_name="root", log_level=LOG_LEVEL, keep_logs=False):
    # print(f"Configuring Logging: {logger_name}")
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    # Check if handlers already exist to prevent duplication
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(ColorLevelFormatter())
        logger.addHandler(console_handler)

        if keep_logs:
            # File Handler with detailed messages
            file_handler = RotatingFileHandler(
                "logs/logs.log", maxBytes=5 * 1024 * 1024, backupCount=3
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(DetailedFormatter())
            logger.addHandler(file_handler)

    # Prevent logging from propagating to the root logger
    logger.propagate = False
