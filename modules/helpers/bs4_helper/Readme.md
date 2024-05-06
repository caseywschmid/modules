# Documentation

## Requirements

This package depends on a custom Logger. To install the Logger package, run the
following command:

`pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger`

Note: You will receive an error if you try to run the BS4Helper without first
installing the Logger package.

## Installation

Install the package directly from GitHub:

`pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/helpers/bs4_helper`

## BS4Helper Class

The `BS4Helper` class is a utility for fetching and parsing HTML content using
BeautifulSoup. It provides methods to easily retrieve HTML from a URL and to
perform searches within the HTML content.

### Methods

#### `get_soup(url)`

Fetches the HTML content from a specified URL and returns a `BeautifulSoup`
object for parsing.

- **Parameters:**
  - `url` (str): The URL from which to fetch the HTML content.
- **Returns:**
  - `BeautifulSoup`: A BeautifulSoup object initialized with the fetched HTML
    content.

#### `find_div_with_class_name(class_name)`

Finds and returns the first `<div>` element with the specified class name in the
parsed HTML.

- **Parameters:**
  - `class_name` (str): The class attribute of the `<div>` element to find.
- **Returns:**
  - `bs4.element.Tag`: The first `<div>` element with the specified class name,
    or `None` if no such element is found.

### Usage

```python
from CWS_BS4Helper.bs4_helper import BS4Helper

bs4_helper = BS4Helper()
soup = bs4_helper.get_soup("https://www.google.com")
print(soup.prettify())
```
