
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src import reporting


class TestReporting(unittest.TestCase):

    def test_records_are_appended(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "reports" / "metrics.jsonl"

            with patch.object(reporting, "REPORT_PATH", test_file):
                reporting.append_snapshot({"cpu_percent": 20})
                reporting.append_snapshot({"cpu_percent": 40})

            lines = test_file.read_text(
                encoding="utf-8"
            ).splitlines()

            records = [json.loads(line) for line in lines]

            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["cpu_percent"], 20)
            self.assertEqual(records[1]["cpu_percent"], 40)
            self.assertIn("timestamp", records[0])

    def test_write_failure_raises_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            blocker = Path(temp_dir) / "reports"
            blocker.write_text("This is a file", encoding="utf-8")

            test_file = blocker / "metrics.jsonl"

            with patch.object(reporting, "REPORT_PATH", test_file):
                with self.assertRaises(OSError):
                    reporting.append_snapshot({"cpu_percent": 20})


if __name__ == "__main__":
    unittest.main()
