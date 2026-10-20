
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


class TestMonitorErrorHandling(unittest.TestCase):

    def test_report_write_failure(self):
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
                side_effect=OSError("Simulated write failure")
            ),
            redirect_stdout(output),
            redirect_stderr(errors),
        ):
            exit_code = monitor.main()

        self.assertEqual(exit_code, 1)

        self.assertIn(
            "WARNING: Sustained high memory utilization",
            output.getvalue()
        )

        self.assertIn(
            "WARNING: Local HTTP service unavailable",
            output.getvalue()
        )

        self.assertIn(
            "report could not be saved",
            errors.getvalue()
        )

        self.assertNotIn(
            "Report saved:",
            output.getvalue()
        )


if __name__ == "__main__":
    unittest.main()
