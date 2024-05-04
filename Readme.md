# Documentation

## Usage

Install the package directly from GitHub:

`pip install git+https://github.com/caseywschmid/modules.git`

## Modules

### Helpers

#### BS4Helper Class

The `BS4Helper` class is a utility for fetching and parsing HTML content using
BeautifulSoup. It provides methods to easily retrieve HTML from a URL and to
perform searches within the HTML content.

##### Methods

###### `get_soup(url)`

Fetches the HTML content from a specified URL and returns a `BeautifulSoup`
object for parsing.

- **Parameters:**
  - `url` (str): The URL from which to fetch the HTML content.
- **Returns:**
  - `BeautifulSoup`: A BeautifulSoup object initialized with the fetched HTML
    content.

###### `find_div_with_class_name(class_name)`

Finds and returns the first `<div>` element with the specified class name in the
parsed HTML.

- **Parameters:**
  - `class_name` (str): The class attribute of the `<div>` element to find.
- **Returns:**
  - `bs4.element.Tag`: The first `<div>` element with the specified class name,
    or `None` if no such element is found.

### Logger

#### Features

- **Custom Log Levels**: Includes custom log levels such as `FINE` and
  `MILESTONE` to provide more granularity than the standard logging levels.
- **Color-Coded Console Output**: Uses color coding in the console output to
  distinguish between different log levels.
- **Optional Detailed Output**: Can toggle detailed output in the console that
  includes timestamps, logger names, and file locations.
- **File Logging**: Supports file logging with rotation, keeping backups of log
  files.

#### Custom Log Levels

- `FINE`: A log level between `DEBUG` and `INFO`, with a value of 15.
- `MILESTONE`: A log level between `INFO` and `WARNING`, with a numeric of 25.

#### Configuration

The logging configuration is set up when the module is imported, but can be
reconfigured dynamically if needed.

##### Default Configuration

By default, the logger is configured to:

- Set the log level to `FINE` (15).
- Output logs to the console with color formatting.
- Optionally output detailed logs to files (commented out by default).

##### Console Output Formatting

The console output is color-coded based on the log level:

- `DEBUG`:      Grey;        Level - 10
- `FINE`:       Blue;        Level - 15
- `INFO`:       Green;       Level - 20
- `MILESTONE`:  Purple;      Level - 25
- `WARNING`:    Yellow;      Level - 30
- `ERROR`:      Red;         Level - 40
- `CRITICAL`:   Bold Red;    Level - 50

##### File Output Formatting

File logging is set up to rotate logs when they reach 5MB and keep up to 3
backups. The detailed format includes timestamps, logger names, log levels, and
file locations. This feature is disabled by default. You can enable it for a
particular file by running `configure_logging(keep_files=True)`.

#### Usage

Best practice is to set some kind of constant in your main file to set the log
level. This way you can easily change the log level for all files by changing
the constant in one place. To use the configured logger in your Python files: 

```python
python
from constants import LOG_LEVEL
import logging
from modules.logs.logger import configure_logging

log = logging.getLogger(__name__)
configure_logging(log_level=LOG_LEVEL, keep_logs=False)

log.debug("This is a debug message")
log.fine("This is a fine message")
log.info("This is an info message")
log.milestone("This is a milestone message")
log.warning("This is a warning message")
log.error("This is an error message")
log.critical("This is a critical message")
```
