
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


class TestMonitorIntegration(unittest.TestCase):

    def test_unavailable_service_with_successful_reporting(self):
        fake_metrics = {
            "cpu_percent": 20.0,
            "memory_percent": 90.0,
            "disk_percent": 55.0,
        }

        output = io.StringIO()
        errors = io.StringIO()

        with (
            patch.object(
                monitor,
                "collect_metrics",
                return_value=fake_metrics
            ),
            patch.object(
                monitor,
                "check_http_service",
                return_value=False
            ),
            patch.object(
                monitor,
                "append_snapshot",
                return_value=Path("simulated.jsonl")
            ) as mock_report,
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            exit_code = monitor.main()

        # The monitoring application succeeded.
        self.assertEqual(exit_code, 0)

        # The unavailable service was detected.
        self.assertIn(
            "WARNING: Local HTTP service unavailable",
            output.getvalue()
        )

        # Reporting was successful.
        self.assertIn("Report saved:", output.getvalue())
        self.assertEqual(errors.getvalue(), "")

        # Verify the report contains the correct status.
        mock_report.assert_called_once()
        report_data = mock_report.call_args.args[0]

        self.assertFalse(report_data["service"]["available"])
        self.assertTrue(report_data["warnings"]["service"])
        self.assertTrue(report_data["warnings"]["memory"])


if __name__ == "__main__":
    unittest.main()
