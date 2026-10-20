
import unittest

from src.config import load_config, validate_config


class TestConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = {
            "cpu_warning_percent": 85,
            "memory_warning_percent": 85,
            "disk_warning_percent": 90,
            "service_url": "http://127.0.0.1:8765/",
            "service_timeout_seconds": 2,
        }

    def test_valid_configuration(self):
        result = validate_config(self.config)
        self.assertEqual(result, self.config)

    def test_invalid_cpu_threshold(self):
        self.config["cpu_warning_percent"] = 150

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_excessive_timeout(self):
        self.config["service_timeout_seconds"] = 200

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_invalid_url_scheme(self):
        self.config["service_url"] = "ftp://example.com"

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_missing_required_setting(self):
        del self.config["memory_warning_percent"]

        with self.assertRaises(ValueError):
            validate_config(self.config)

    def test_load_actual_configuration(self):
        config = load_config()

        self.assertEqual(config["cpu_warning_percent"], 85)
        self.assertEqual(config["service_timeout_seconds"], 2)


if __name__ == "__main__":
    unittest.main()
