
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

from src import service_check


TEST_URL = "http://127.0.0.1:8765/"


class TestHTTPService(unittest.TestCase):

    def test_http_success(self):
        with patch("src.service_check.urlopen") as mock_open:
            mock_open.return_value.__enter__.return_value.status = 200

            result = service_check.check_http_service(TEST_URL)

            self.assertTrue(result)
            mock_open.assert_called_once_with(TEST_URL, timeout=2)

    def test_http_server_error(self):
        error = HTTPError(
            TEST_URL, 503, "Service Unavailable", None, None
        )

        try:
            with patch(
                "src.service_check.urlopen",
                side_effect=error
            ):
                result = service_check.check_http_service(TEST_URL)

            self.assertFalse(result)

        finally:
            error.close()

    def test_connection_failure(self):
        with patch(
            "src.service_check.urlopen",
            side_effect=URLError("Connection refused")
        ):
            result = service_check.check_http_service(TEST_URL)

        self.assertFalse(result)

    def test_timeout(self):
        with patch(
            "src.service_check.urlopen",
            side_effect=TimeoutError("Connection timed out")
        ):
            result = service_check.check_http_service(TEST_URL)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
