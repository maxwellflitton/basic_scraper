from unittest import TestCase, main
from unittest.mock import patch, MagicMock


from basic_scaper.basic_thread import BasicImageThread


class TestBasicImageThread(TestCase):

    @patch("basic_scaper.basic_thread.Thread.__init__")
    def test__init__(self, mock_super_init):
        mock_super_init.return_value = None
        test = BasicImageThread(url="test url")

        self.assertEqual("test url", test.url)
        self.assertEqual(None, test.result)

    @patch("basic_scaper.basic_thread.requests")
    @patch("basic_scaper.basic_thread.BasicImageThread.__init__")
    def test_run(self, mock_init, mock_requests):
        mock_init.return_value = None
        test = BasicImageThread(url="test url")
        test.url = MagicMock()

        test.run()

        mock_requests.get.assert_called_once_with(test.url, stream=True)
        self.assertEqual(mock_requests.get.return_value.content, test.result)


if __name__ == "__main__":
    main()