
import sys
from pathlib import Path

import psutil

from alert_rules import is_sustained_high
from reporting import append_snapshot
from service_check import check_http_service


TEST_SERVICE_URL = "http://127.0.0.1:8765/"


def collect_metrics():
    drive = Path.home().anchor

    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(drive).percent,
    }

    return metrics


def main():
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

    # Check the local HTTP test service
    service_available = check_http_service(TEST_SERVICE_URL)

    # Calculate warnings once
    warnings = {
        "cpu": is_sustained_high(cpu_readings),
        "memory": is_sustained_high(memory_readings),
        "disk": metrics["disk_percent"] >= 90,
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
        print("WARNING: Disk utilization is 90% or higher")
    else:
        print("Disk: Below warning threshold")

    if warnings["service"]:
        print("WARNING: Local HTTP service unavailable")
    else:
        print("HTTP Service: Available")

    # Prepare historical monitoring data
    report_data = {
        "cpu_samples_percent": cpu_readings,
        "memory_samples_percent": memory_readings,
        "disk_percent": metrics["disk_percent"],
        "service": {
            "url": TEST_SERVICE_URL,
            "available": service_available,
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
