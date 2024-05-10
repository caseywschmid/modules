import os
import requests

# Use importlib.metadata for Python 3.8 and above
from importlib.metadata import version
from bs4 import BeautifulSoup

# ------ CONFIGURE LOGGING ------
import logging

try:
    # if running the code from the package itself
    if os.getenv("BS4_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
        from modules.logs.logger.CWS_Logger import logger
    else:
        # if running the code as an imported package in another project
        from CWS_Logger import logger  # type: ignore
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "The necessary 'Logger' module is not installed. Please install it by running \n'pip install git+https://github.com/caseywschmid/modules.git#subdirectory=modules/logs/logger'"
    )

logger.configure_logging(__name__)
log = logging.getLogger(__name__)

if os.getenv("BS4_HELPER_PACKAGE_TEST", "False").lower() in ("true", "1", "t"):
    log.info("Running in test mode.")


BS4_VERSION = "4.12.3"


class BS4Helper:
    """
    A helper class for fetching and parsing HTML content using BeautifulSoup.

    This class provides methods to fetch HTML from a URL and to find specific
    elements within the HTML.
    """

    def __init__(self):
        self.check_dependency_versions()
        self.soup = None

    def check_dependency_versions(self):
        current_bs4_version = version("beautifulsoup4")
        # Check if the warning should be muted
        mute_warning = os.getenv("MUTE_BS4_HELPER_WARNING", "False").lower() in (
            "true",
            "1",
            "t",
        )

        if not mute_warning and current_bs4_version != BS4_VERSION:
            log.info(
                "This warning can be muted by setting the MUTE_BS4_HELPER_WARNING environment variable to 'True'."
            )
            log.warning(
                f"The 'BS4Helper' tool was created using Beautiful Soup version {BS4_VERSION}. The version you have installed in this project ({current_bs4_version}) may not be compatible with this tool. If you encounter any issues, either downgrade your BeautifulSoup version to 4.12.3 or email the creator at caseywschmid@gmail.com to have the package updated."
            )

    def get_soup(self, url, timeout=5):
        """
        Fetches the HTML content from a specified URL and returns a
        BeautifulSoup object for parsing.

        Args:
            url (str): The URL from which to fetch the HTML content.
            timeout (int, optional): The number of seconds to wait for the server to send data
            before giving up. Defaults to 5.

        Returns:
            BeautifulSoup: A BeautifulSoup object initialized with the fetched
            HTML content.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
            requests.exceptions.RequestException: If there was an ambiguous exception that occurred while handling your request.
            Exception: If an unexpected exception occurred.
        """
        log.fine("BS4Helper.get_soup")
        # Some websites may block requests without a User-Agent header.
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.text, "html.parser")
            return self.soup
        except requests.exceptions.HTTPError as e:
            raise requests.exceptions.HTTPError(f"HTTP Error: {e}")
        except requests.exceptions.Timeout:
            raise requests.exceptions.Timeout(
                "The request timed out. The default timeout is 5 seconds. You can increase the timeout by passing a different value to the 'timeout' parameter of the `get_soup()` method."
            )
        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f"Error: {e}")
        except Exception as e:
            raise Exception(str(e))

    def find_div_with_class_name(self, class_name):
        """
        Finds and returns the first <div> element with the specified class name
        in the parsed HTML.

        Args:
            class_name (str): The class attribute of the <div> element to find.

        Returns:
            bs4.element.Tag: The first <div> element with the specified class
            name, or None if no such element is found.

        Raises:
            AttributeError: If the soup object is None or not initialized.
        """
        log.fine("BS4Helper.find_div_with_class_name")
        if self.soup is None:
            raise AttributeError(
                "The BeautifulSoup object is not initialized. Please ensure you have fetched the HTML content with `get_soup()` method before calling this method."
            )
        try:
            return self.soup.find("div", class_=class_name)
        except AttributeError as e:
            raise AttributeError(
                "An error occurred while finding the div with the specified class name. Please ensure the class name is correct."
            ) from e

    def find_element_with_id(self, element_id):
        """
        Finds and returns the element with the specified ID in the parsed HTML.

        Args:
            element_id (str): The ID attribute of the element to find.

        Returns:
            bs4.element.Tag: The element with the specified ID, or None if no such element is found.

        Raises:
            AttributeError: If the soup object is None or not initialized.
        """
        log.fine("BS4Helper.find_element_with_id")
        if self.soup is None:
            raise AttributeError(
                "The BeautifulSoup object is not initialized. Please ensure you have fetched the HTML content with `get_soup()` method before calling this method."
            )
        try:
            return self.soup.find(id=element_id)
        except AttributeError as e:
            raise AttributeError(
                "An error occurred while finding the element with the specified ID. Please ensure the ID is correct."
            ) from e