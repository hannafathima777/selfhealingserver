import pytest
from app.monitor import get_cpu_usage, get_ram_usage, get_disk_usage, collect_metrics


def test_cpu_usage_range():
    cpu = get_cpu_usage()
    assert 0 <= cpu <= 100, f"CPU usage out of range: {cpu}"


def test_ram_usage_range():
    ram = get_ram_usage()
    assert 0 <= ram <= 100, f"RAM usage out of range: {ram}"


def test_disk_usage_range():
    disk = get_disk_usage()
    assert 0 <= disk <= 100, f"Disk usage out of range: {disk}"


def test_collect_metrics_keys():
    metrics = collect_metrics()
    assert "cpu" in metrics
    assert "ram" in metrics
    assert "disk" in metrics
    assert "timestamp" in metrics


def test_collect_metrics_types():
    metrics = collect_metrics()
    assert isinstance(metrics["cpu"], float)
    assert isinstance(metrics["ram"], float)
    assert isinstance(metrics["disk"], float)