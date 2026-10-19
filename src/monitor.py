
from pathlib import Path
import psutil
from alert_rules import is_sustained_high


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

    print("\n=== Alert Evaluation ===")

    if is_sustained_high(cpu_readings):
        print("WARNING: Sustained high CPU utilization")
    else:
        print("CPU: No sustained high utilization detected")

    if is_sustained_high(memory_readings):
        print("WARNING: Sustained high memory utilization")
    else:
        print("Memory: No sustained high utilization detected")

    if metrics["disk_percent"] >= 90:
        print("WARNING: Disk utilization is 90% or higher")
    else:
        print("Disk: Below warning threshold")

if __name__ == "__main__":
    main()
