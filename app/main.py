import time
import schedule
from app.config import MONITOR_INTERVAL, TARGET_CONTAINER
from app.monitor import collect_metrics
from app.health_check import get_health_status
from app.anomaly_detector import is_anomaly, load_model, train_model, generate_synthetic_training_data
from app.healer import heal

from app.logger import log_metrics, log_event


def initialize_model():
    """Load existing model or train a new one with synthetic data."""
    model = load_model()
    if model is None:
        log_event("INIT", "Training a new model with synthetic data...")
        training_data = generate_synthetic_training_data(500)
        model = train_model(training_data)
    return model


def monitor_cycle(model):
    """One complete monitoring, detection, and healing cycle."""
    # 1. Collect metrics
    metrics = collect_metrics()
    cpu, ram, disk = metrics["cpu"], metrics["ram"], metrics["disk"]
    log_event("MONITOR", f"CPU:{cpu:.1f}% | RAM:{ram:.1f}% | DISK:{disk:.1f}%")

    # 2. Health check
    health = get_health_status(TARGET_CONTAINER)

    # 3. Anomaly detection
    anomaly = is_anomaly(cpu, ram, disk, model)

    # 4. Log metrics
    log_metrics(cpu, ram, disk, health, anomaly)

    # 5. Heal if needed
    action = "NO_ACTION"
    if health != "healthy" or anomaly:
        reason = f"Health: {health} | Anomaly: {anomaly} | CPU:{cpu:.1f} RAM:{ram:.1f} DISK:{disk:.1f}"
        log_event("ALERT", reason, "TRIGGERING_HEAL")
        
        action = heal(health, anomaly, TARGET_CONTAINER)
        

    log_event("CYCLE", f"Cycle complete. Action: {action}")
    return action


def run():
    """Start the self-healing monitoring loop."""
    print("=" * 55)
    print("  🛡️  Self-Healing Server — Monitoring Started")
    print("=" * 55)
    log_event("INIT", "Self-Healing Server started.")
    model = initialize_model()

    # Run immediately on start, then on schedule
    monitor_cycle(model)
    schedule.every(MONITOR_INTERVAL).seconds.do(monitor_cycle, model)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run()