from bs4 import BeautifulSoup
from typing import Union, List
import requests

from .basic_thread import BasicImageThread


class BasicWorker:
    """
    This is a class for getting basic image and word data if accessed directly under html class.

    Attributes:
        url (str): url to website to be scraped
        raw_data (str) raw data from the website
        parsed_data (str) raw data that has been passed through Beautiful Soup Parser
    """
    def __init__(self, url: str):
        """
        The constructor for the BasicWorker class.

        :param url: (str) url to website to be scraped
        """
        self.url = url
        self.raw_data = None
        self.parsed_data = None

    @staticmethod
    def process_url(url_string: str) -> str:
        """
        Cleans the prefix of the url string to "http://" (static).

        :param url_string: (str) url to be cleaned
        :return: (str) cleaned url
        """
        if url_string.startswith('http://www.'):
            return 'http://' + url_string[len('http://www.'):]
        if url_string.startswith('www.'):
            return 'http://' + url_string[len('www.'):]
        if url_string.startswith("//"):
            return 'http:' + url_string
        if url_string.startswith("https://"):
            return url_string
        if not url_string.startswith('http://'):
            return 'http://' + url_string
        return url_string

    def get_raw_data(self) -> None:
        """
        Gets raw HTML data from self.url to populate self.raw_data.

        :return: None
        """
        self.raw_data = requests.get(self.url).content

    def parse_html(self) -> None:
        """
        Parses the self.raw_data using beautiful soup to self.parsed_data.

        :return: None
        """
        if self.raw_data is None:
            self.get_raw_data()
        self.parsed_data = BeautifulSoup(self.raw_data, 'html.parser')

    def word_filter(self, tag_type: str, class_name: str) -> List[Union[str, int, float]]:
        """
        Filters self.parsed_data based on the tag and class name.

        :param tag_type: (str) tag identified such as 'div', 'span' etc
        :param class_name: (str) name of the class for the filter to act on
        :return: (list) list of contents (WARNING: response has to have .contents)
        """
        if self.parsed_data is None:
            self.parse_html()
        return [i.contents[0] for i in self.parsed_data.findAll(tag_type, {"class": class_name})]

    def image_filter(self, tag_type: str, class_name: str) -> List[bytes]:
        """
        Gets raw image data based on tag and class name.

        :param tag_type: (str) tag identified such as 'div', 'span' etc
        :param class_name: (str) name of the class for the filter to act on
        :return: (list[bytes]) image data from the filter
        """
        results = []
        if self.parsed_data is None:
            self.parse_html()

        urls = [i.get("src") for i in self.parsed_data.findAll(tag_type, {"class": class_name})]
        for url in urls:
            if url is None:
                results.append(None)
            image_url = self.process_url(url_string=url)
            result = requests.get(image_url, stream=True)
            results.append(result.content)
        return results

    def threaded_image_filter(self, tag_type: str, class_name: str) -> List[bytes]:
        """
        Gets raw image data based on tag and class name (multi-threaded).

        :param tag_type: (str) tag identified such as 'div', 'span' etc
        :param class_name: (str) name of the class for the filter to act on
        :return: (list[bytes]) image data from the filter
        """
        if self.parsed_data is None:
            self.parse_html()

        urls = [i.get("src") for i in self.parsed_data.findAll(tag_type, {"class": class_name})]
        threads = []
        for url in urls:
            url = self.process_url(url_string=url)
            temp_thread = BasicImageThread(url=url)
            temp_thread.start()
            threads.append(temp_thread)

        for thread in threads:
            thread.join()

        return [i.result for i in threads]
