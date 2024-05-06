# Documentation

## Usage

Install the package directly from GitHub:

`pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger`

## Logger

### Features

- **Custom Log Levels**: Includes custom log levels such as `FINE` and
  `MILESTONE` to provide more granularity than the standard logging levels.
- **Color-Coded Console Output**: Uses color coding in the console output to
  distinguish between different log levels.
- **Optional Detailed Output**: Can toggle detailed output in the console that
  includes timestamps, logger names, and file locations.
- **File Logging**: Supports file logging with rotation, keeping backups of log
  files.

### Custom Log Levels

- `FINE`: A log level between `DEBUG` and `INFO`, with a value of 15.
- `MILESTONE`: A log level between `INFO` and `WARNING`, with a numeric of 25.

### Configuration

The logging configuration is set up when the module is imported, but can be
reconfigured dynamically if needed.

### Default Configuration

By default, the logger is configured to:

- Set the log level to `FINE` (15).
- Output logs to the console with color formatting.
- Optionally output detailed logs to files (commented out by default).

### Console Output Formatting

The console output is color-coded based on the log level:

- `DEBUG`: Grey; Level - 10
- `FINE`: Blue; Level - 15
- `INFO`: Green; Level - 20
- `MILESTONE`: Purple; Level - 25
- `WARNING`: Yellow; Level - 30
- `ERROR`: Red; Level - 40
- `CRITICAL`: Bold Red; Level - 50

### File Output Formatting

File logging is set up to rotate logs when they reach 5MB and keep up to 3
backups. The detailed format includes timestamps, logger names, log levels, and
file locations. This feature is disabled by default. You can enable it for a
particular file by running `configure_logging(keep_files=True)`.

## Usage

Best practice is to set some kind of constant in your main file to set the log
level. This way you can easily change the log level for all files by changing
the constant in one place. Files though can be set to a custom log level if you
choose. To use the configured logger in your Python files:

```python
from constants import LOG_LEVEL
# setup logging
import logging
from modules.logs import logger

logger.configure_logging(__name__, log_level=LOG_LEVEL)
log = logging.getLogger(__name__)

log.debug("This is a debug message")
log.fine("This is a fine message")
log.info("This is an info message")
log.milestone("This is a milestone message")
log.warning("This is a warning message")
log.error("This is an error message")
log.critical("This is a critical message")
```