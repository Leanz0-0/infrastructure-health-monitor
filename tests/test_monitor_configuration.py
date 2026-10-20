
import io
import sys
import unittest

from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

import monitor


class TestMonitorConfiguration(unittest.TestCase):

    def test_custom_configuration(self):
        config = {
            "cpu_warning_percent": 85,
            "memory_warning_percent": 95,
            "disk_warning_percent": 90,
            "service_url": "http://127.0.0.1:9999/",
            "service_timeout_seconds": 5,
        }

        fake_metrics = {
            "cpu_percent": 20.0,
            "memory_percent": 91.0,
            "disk_percent": 55.0,
        }

        with (
            patch.object(
                monitor, "load_config",
                return_value=config
            ),
            patch.object(
                monitor, "collect_metrics",
                return_value=fake_metrics
            ),
            patch.object(
                monitor, "check_http_service",
                return_value=True
            ) as mock_service,
            patch.object(
                monitor, "append_snapshot",
                return_value=Path("simulated.jsonl")
            ) as mock_report,
            redirect_stdout(io.StringIO()),
        ):
            exit_code = monitor.main()

        self.assertEqual(exit_code, 0)

        mock_service.assert_called_once_with(
            "http://127.0.0.1:9999/",
            timeout=5
        )

        report = mock_report.call_args.args[0]

        self.assertEqual(
            report["thresholds"]["memory_percent"], 95
        )
        self.assertFalse(report["warnings"]["memory"])

    def test_invalid_config_stops_monitoring(self):
        errors = io.StringIO()

        with (
            patch.object(
                monitor, "load_config",
                side_effect=ValueError("Invalid threshold")
            ),
            patch.object(
                monitor, "collect_metrics"
            ) as mock_collect,
            patch.object(
                monitor, "append_snapshot"
            ) as mock_report,
            redirect_stderr(errors),
        ):
            exit_code = monitor.main()

        self.assertEqual(exit_code, 2)
        mock_collect.assert_not_called()
        mock_report.assert_not_called()

        self.assertIn(
            "Invalid or unavailable configuration",
            errors.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
