import csv
import os
from datetime import datetime
from app.config import LOG_FILE, METRICS_FILE


def _ensure_file(filepath: str, headers: list):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)


def log_metrics(cpu: float, ram: float, disk: float, health: str, anomaly: bool):
    """Save collected metrics to CSV."""
    headers = ["timestamp", "cpu", "ram", "disk", "health_status", "anomaly"]
    _ensure_file(METRICS_FILE, headers)
    with open(METRICS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(), cpu, ram, disk, health, anomaly
        ])


def log_event(event_type: str, message: str, action: str = "None"):
    """Save a monitoring event/action to logs CSV."""
    headers = ["timestamp", "event_type", "message", "action"]
    _ensure_file(LOG_FILE, headers)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(), event_type, message, action
        ])
    print(f"[{datetime.now().strftime('%H:%M:%S')}] [{event_type}] {message} | Action: {action}")