
import json
from datetime import datetime
from pathlib import Path


REPORT_PATH = (
    Path(__file__).resolve().parent.parent
    / "reports"
    / "metrics.jsonl"
)


def append_snapshot(data):
    record = {
        "timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        **data,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with REPORT_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")

    return REPORT_PATH
