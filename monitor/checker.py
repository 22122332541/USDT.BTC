"""System metrics checker – collects CPU, memory and disk usage."""

import psutil

from monitor.config import CPU_THRESHOLD, MEMORY_THRESHOLD, DISK_THRESHOLD


def get_cpu_usage() -> float:
    """Return current CPU usage percentage (averaged over 1 second)."""
    return psutil.cpu_percent(interval=1)


def get_memory_usage() -> float:
    """Return current memory usage percentage."""
    return psutil.virtual_memory().percent


def get_disk_usage(path: str = "/") -> float:
    """Return disk usage percentage for *path*.

    Note: The default path ``/`` targets Unix-like systems.  On Windows,
    pass an explicit drive such as ``C:\\``.
    """
    return psutil.disk_usage(path).percent


def check_anomalies() -> list[dict]:
    """Check all metrics and return a list of anomalies found.

    Each anomaly is a dict with keys: metric, value, threshold.
    """
    anomalies: list[dict] = []

    cpu = get_cpu_usage()
    if cpu > CPU_THRESHOLD:
        anomalies.append({"metric": "CPU", "value": cpu, "threshold": CPU_THRESHOLD})

    mem = get_memory_usage()
    if mem > MEMORY_THRESHOLD:
        anomalies.append(
            {"metric": "Memory", "value": mem, "threshold": MEMORY_THRESHOLD}
        )

    disk = get_disk_usage()
    if disk > DISK_THRESHOLD:
        anomalies.append(
            {"metric": "Disk", "value": disk, "threshold": DISK_THRESHOLD}
        )

    return anomalies
