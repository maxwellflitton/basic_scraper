from threading import Thread
import requests


class BasicImageThread(Thread):
    """
    This is a class for managing the threading of downloading image data.

    Attributes:
        url (str): url of the image to be scraped
        result (bytes): image data
    """
    def __init__(self, url: str):
        """
        The constructor for the BasicImageThread class.

        :param url: (str) url of the image to be scraped
        """
        super().__init__()
        self.url = url
        self.result = None

    def run(self) -> None:
        """
        Fires when the thread starts.

        :return: None
        """
        if self.url is None:
            self.result = None
        else:
            result = requests.get(self.url, stream=True)
            self.result = result.content
