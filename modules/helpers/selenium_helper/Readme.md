# SeleniumHelper Class Documentation

The `SeleniumHelper` class is a utility for automating browser tasks using Selenium, PyAutoGUI, and psutil. It provides methods for opening Chrome in different modes, navigating to URLs, logging mouse coordinates, and more.

## Requirements

This package depends on a custom Logger. To install the Logger package, run the
following command:

```terminal
pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger
```

Note: You will receive an error if you try to run the SeleniumHelper without first
installing the Logger package.

## Installation

Install the package directly from GitHub:

```terminal
pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/helpers/selenium_helper
```

## Methods

### `start_coordinate_logging()`
---
This method logs the current mouse coordinates at specified intervals for a given duration.

- **Parameters:**
  - `logging_interval` (float, optional): The time interval (in seconds) between
    each log of the mouse coordinates. **Defaults to 0.5 seconds**.
  - `duration` (int, optional): The total duration (in seconds) for which the
    mouse coordinates will be logged. **Defaults to 30 seconds**.
- **Returns:** None

### `open_chrome_in_debug()`
---
This method opens a new Chrome window in incognito mode in debug mode.

- **Parameters:** None
- **Returns:** None

### `open_chrome()`
---
This method opens a new Chrome window in incognito mode.

- **Parameters:** None
- **Returns:** None

### `open_url_in_new_chrome_incognito_window()`
---
This method opens the specified URL in a new Chrome incognito window with optional debug mode, zoom level, window size, and window position.

- **Parameters:**
  - `url` (str): The URL to be opened.
  - `zoom` (int, optional): The zoom level for the browser window, expressed as a percentage. Defaults to 100.
  - `debug` (bool, optional): If True, opens the browser in debug mode. Defaults to False.
  - `window_size` (tuple[int, int], optional): The size of the browser window as a tuple (width, height). Defaults to (1300, 2100).
  - `window_position` (tuple[int, int], optional): The position of the browser window as a tuple (x, y). Defaults to (100, 0).
- **Returns:** A tuple containing the WebDriver instance and the WebDriverWait instance for the opened browser window.

### `close_browser()`
---
This method closes the current browser window.

- **Parameters:** None
- **Returns:** None

### `close_chrome()`
---
This method closes the main Chrome process.

- **Parameters:** None
- **Returns:** None

### `take_screenshot()`
---
This method takes a screenshot of the current state of the browser and saves it to the specified file path.

- **Parameters:**
  - `file_path` (str): The path to save the screenshot file. The '.png' extension should be added at the source as it is not added in this method.
- **Returns:** None

### `capture_html(filename=None)`
---
This method captures the HTML of the current page in the browser. If a filename is provided, it saves the HTML to that file.

- **Parameters:**
  - `filename` (str, optional): The name of the file where the HTML will be saved. If not provided, the HTML is not saved to a file.
- **Returns:** The HTML of the current page.

## Usage

```python
from CWS_SeleniumHelper.selenium_helper import SeleniumHelper

sh = SeleniumHelper()
sh.open_chrome_in_new_chrome_incognito_window(
    url="https://www.google.com",
    zoom=100,
    debug=False,
    window_size=(1300, 2100),
    window_position=(100, 0)
)
```
