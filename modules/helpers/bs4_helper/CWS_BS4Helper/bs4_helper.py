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
        from CWS_Logger import logger
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

    @staticmethod
    def get_soup(url):
        """
        Fetches the HTML content from a specified URL and returns a
        BeautifulSoup object for parsing.

        Args:
            url (str): The URL from which to fetch the HTML content.

        Returns:
            BeautifulSoup: A BeautifulSoup object initialized with the fetched
            HTML content.
        """
        log.fine("BS4Helper.get_soup")
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

    @staticmethod
    def find_div_with_class_name(self, class_name):
        """
        Finds and returns the first <div> element with the specified class name
        in the parsed HTML.

        Args:
            class_name (str): The class attribute of the <div> element to find.

        Returns:
            bs4.element.Tag: The first <div> element with the specified class
            name, or None if no such element is found.
        """
        log.fine("BS4Helper.find_div_with_class_name")
        return self.soup.find("div", class_=class_name)
