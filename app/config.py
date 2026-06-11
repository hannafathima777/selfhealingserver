import os
from dotenv import load_dotenv

load_dotenv()

# Monitoring
MONITOR_INTERVAL = int(os.getenv("MONITOR_INTERVAL", 10))

# Thresholds
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", 85))
RAM_THRESHOLD = float(os.getenv("RAM_THRESHOLD", 85))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD", 90))

# Docker
DOCKER_SOCKET = os.getenv("DOCKER_SOCKET", "unix://var/run/docker.sock")
TARGET_CONTAINER = os.getenv("TARGET_CONTAINER", "demo_app")





# Paths
LOG_FILE = os.getenv("LOG_FILE", "data/logs.csv")
METRICS_FILE = os.getenv("METRICS_FILE", "data/metrics.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "models/isolation_forest.pkl")