from flask import Flask, Response
from prometheus_client import Gauge, generate_latest
import psutil

app = Flask(__name__)

cpu_gauge = Gauge("cpu_usage", "CPU usage")
ram_gauge = Gauge("ram_usage", "RAM usage")
disk_gauge = Gauge("disk_usage", "Disk usage")


def collect_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    cpu_gauge.set(cpu)
    ram_gauge.set(ram)
    disk_gauge.set(disk)


@app.route("/metrics")
def metrics():
    collect_metrics()
    return Response(generate_latest(), mimetype="text/plain")


@app.route("/health")
def health():
    return {"status": "ok"}


def run_metrics_server():
    print("Metrics server running on port 8000")
    app.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    run_metrics_server()