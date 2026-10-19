
from pathlib import Path
import psutil


def collect_metrics():
    drive = Path.home().anchor

    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage(drive).percent,
    }

    return metrics


def main():
    metrics = collect_metrics()

    print("=== Infrastructure Health Monitor ===")
    print(f"CPU Usage: {metrics['cpu_percent']:.1f}%")
    print(f"Memory Usage: {metrics['memory_percent']:.1f}%")
    print(f"Home Drive Usage: {metrics['disk_percent']:.1f}%")


if __name__ == "__main__":
    main()
