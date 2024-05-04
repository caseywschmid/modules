from bs4 import BeautifulSoup
import requests


class BS4Helper:
    """
    A helper class for fetching and parsing HTML content using BeautifulSoup.

    This class provides methods to fetch HTML from a URL and to find specific
    elements within the HTML.
    """

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
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")

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
        return self.soup.find("div", class_=class_name)
