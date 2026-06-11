import psutil
from datetime import datetime


def get_cpu_usage() -> float:
    """Return current CPU usage percentage."""
    return psutil.cpu_percent(interval=1)


def get_ram_usage() -> float:
    """Return current RAM usage percentage."""
    mem = psutil.virtual_memory()
    return mem.percent


def get_disk_usage() -> float:
    """Return disk usage percentage for root partition."""
    disk = psutil.disk_usage("/")
    return disk.percent


def collect_metrics() -> dict:
    """Collect all system metrics and return as a dictionary."""
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu": get_cpu_usage(),
        "ram": get_ram_usage(),
        "disk": get_disk_usage(),
    }