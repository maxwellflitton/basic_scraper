from unittest import TestCase, main
from unittest.mock import patch, MagicMock


from basic_scaper.worker import BasicWorker


class TestWorker(TestCase):

    @patch("basic_scaper.worker.BasicWorker.__init__")
    def setUp(self, mock_init):
        mock_init.return_value = None
        self.test = BasicWorker(url="test url")
        self.test.url = "test url"
        self.test.raw_data = None
        self.test.parsed_data = None

    def test___init__(self):
        test = BasicWorker(url="test url")
        self.assertEqual("test url", test.url)

    def test_process_url(self):
        self.assertEqual("http://test.com",
                         BasicWorker.process_url(url_string="http://www.test.com"))
        self.assertEqual("http://test.com",
                         BasicWorker.process_url(url_string="www.test.com"))
        self.assertEqual("http://test.com",
                         BasicWorker.process_url(url_string="//test.com"))
        self.assertEqual("https://test.com",
                         BasicWorker.process_url(url_string="https://test.com"))
        self.assertEqual("http://test.com",
                         BasicWorker.process_url(url_string="test.com"))

    @patch("basic_scaper.worker.requests")
    def test_get_raw_data(self, mock_requests):
        self.test.get_raw_data()
        self.assertEqual(mock_requests.get.return_value.content, self.test.raw_data)
        mock_requests.get.assert_called_once_with(self.test.url)

    @patch("basic_scaper.worker.BeautifulSoup")
    @patch("basic_scaper.worker.BasicWorker.get_raw_data")
    def test_parse_html(self, mock_get_data, mock_soup):
        self.test.parse_html()
        mock_get_data.assert_called_once_with()
        mock_soup.assert_called_once_with(self.test.raw_data, 'html.parser')
        self.assertEqual(self.test.parsed_data, mock_soup.return_value)

        self.test.raw_data = True
        mock_soup.reset_mock()
        self.test.parse_html()
        mock_soup.assert_called_once_with(self.test.raw_data, 'html.parser')
        self.assertEqual(self.test.parsed_data, mock_soup.return_value)
        mock_get_data.assert_called_once_with()

    def test_word_filter(self):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        self.test.parsed_data = MagicMock()
        self.test.parsed_data.findAll.return_value = [one, two, three]

        self.assertEqual([one.contents[0], two.contents[0], three.contents[0]],
                         self.test.word_filter(tag_type="test tag", class_name="test name"))
        self.test.parsed_data.findAll.assert_called_once_with("test tag", {"class": "test name"})

    @patch("basic_scaper.worker.BasicWorker.process_url")
    @patch("basic_scaper.worker.requests")
    def test_image_filter(self, mock_requests, mock_process_url):
        one = {"src": "one"}
        two = {"src": "two"}
        three = {"src": "three"}
        self.test.parsed_data = MagicMock()
        self.test.parsed_data.findAll.return_value = [one, two, three]

        out_come = self.test.image_filter(tag_type="test tag", class_name="test name")
        self.assertEqual(3, len(mock_requests.get.call_args_list))
        self.assertEqual(3, len(mock_process_url.call_args_list))
        self.assertEqual([mock_requests.get.return_value.content,
                          mock_requests.get.return_value.content,
                          mock_requests.get.return_value.content], out_come)

    @patch("basic_scaper.worker.BasicImageThread")
    @patch("basic_scaper.worker.BasicWorker.process_url")
    def test_threaded_image_filter(self, mock_process_url, mock_thread):
        one = {"src": "one"}
        two = {"src": "two"}
        three = {"src": "three"}
        self.test.parsed_data = MagicMock()
        self.test.parsed_data.findAll.return_value = [one, two, three]

        out_come = self.test.threaded_image_filter(tag_type="test tag", class_name="test name")
        self.assertEqual(3, len(mock_process_url.call_args_list))
        self.assertEqual(3, len(mock_thread.call_args_list))
        self.assertEqual(3, len(mock_thread.return_value.start.call_args_list))
        self.assertEqual(3, len(mock_thread.return_value.join.call_args_list))

        result = mock_thread.return_value.result
        self.assertEqual([result, result, result], out_come)


if __name__ == "__main__":
    main()
