
import sys
from pathlib import Path

import psutil

from alert_rules import is_sustained_high
from config import load_config
from reporting import append_snapshot
from service_check import check_http_service


def collect_metrics():
    drive = Path.home().anchor

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(drive).percent,
    }


def main():
    # Validate configuration before collecting data.
    try:
        config = load_config()

    except (OSError, ValueError) as error:
        print(
            f"ERROR: Invalid or unavailable configuration: {error}",
            file=sys.stderr,
        )
        return 2

    cpu_readings = []
    memory_readings = []

    print("=== Infrastructure Health Monitor ===")

    for sample_number in range(1, 4):
        metrics = collect_metrics()

        cpu_readings.append(metrics["cpu_percent"])
        memory_readings.append(metrics["memory_percent"])

        print(
            f"Sample {sample_number}: "
            f"CPU {metrics['cpu_percent']:.1f}% | "
            f"RAM {metrics['memory_percent']:.1f}% | "
            f"Disk {metrics['disk_percent']:.1f}%"
        )

    service_available = check_http_service(
        config["service_url"],
        timeout=config["service_timeout_seconds"],
    )

    warnings = {
        "cpu": is_sustained_high(
            cpu_readings,
            threshold=config["cpu_warning_percent"],
        ),
        "memory": is_sustained_high(
            memory_readings,
            threshold=config["memory_warning_percent"],
        ),
        "disk": (
            metrics["disk_percent"]
            >= config["disk_warning_percent"]
        ),
        "service": not service_available,
    }

    print("\n=== Alert Evaluation ===")

    if warnings["cpu"]:
        print("WARNING: Sustained high CPU utilization")
    else:
        print("CPU: No sustained high utilization detected")

    if warnings["memory"]:
        print("WARNING: Sustained high memory utilization")
    else:
        print("Memory: No sustained high utilization detected")

    if warnings["disk"]:
        print("WARNING: High disk utilization")
    else:
        print("Disk: Below warning threshold")

    if warnings["service"]:
        print("WARNING: Local HTTP service unavailable")
    else:
        print("HTTP Service: Available")

    report_data = {
        "cpu_samples_percent": cpu_readings,
        "memory_samples_percent": memory_readings,
        "disk_percent": metrics["disk_percent"],
        "service": {
            "url": config["service_url"],
            "available": service_available,
        },
        "thresholds": {
            "cpu_percent": config["cpu_warning_percent"],
            "memory_percent": config["memory_warning_percent"],
            "disk_percent": config["disk_warning_percent"],
        },
        "warnings": warnings,
    }

    try:
        report_path = append_snapshot(report_data)

    except OSError as error:
        print(
            f"ERROR: Monitoring completed, "
            f"but the report could not be saved: {error}",
            file=sys.stderr,
        )
        return 1

    print(f"\nReport saved: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
