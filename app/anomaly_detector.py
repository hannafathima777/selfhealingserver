import numpy as np
import joblib
import os
from sklearn.ensemble import IsolationForest
from app.config import MODEL_PATH
from app.logger import log_event


def train_model(training_data: list) -> IsolationForest:
    """
    Train an Isolation Forest model on historical metrics.
    training_data: list of [cpu, ram, disk] samples.
    """
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    X = np.array(training_data)
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    log_event("MODEL", f"Isolation Forest trained on {len(X)} samples and saved.")
    return model


def load_model() -> IsolationForest | None:
    """Load a previously saved model. Returns None if not found."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    log_event("MODEL", "No pre-trained model found. Will use threshold-based detection.", "WARN")
    return None


def is_anomaly(cpu: float, ram: float, disk: float, model: IsolationForest = None) -> bool:
    """
    Detect if the current metrics represent an anomaly.
    Falls back to simple threshold checks if no model is loaded.
    """
    if model:
        sample = np.array([[cpu, ram, disk]])
        prediction = model.predict(sample)
        # IsolationForest: -1 = anomaly, 1 = normal
        result = prediction[0] == -1
        log_event("ANOMALY", f"ML Detection — CPU:{cpu} RAM:{ram} DISK:{disk} → {'ANOMALY' if result else 'Normal'}")
        return result
    else:
        # Fallback: simple threshold check
        from app.config import CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD
        result = cpu > CPU_THRESHOLD or ram > RAM_THRESHOLD or disk > DISK_THRESHOLD
        log_event("ANOMALY", f"Threshold Detection — CPU:{cpu} RAM:{ram} DISK:{disk} → {'ANOMALY' if result else 'Normal'}")
        return result


def generate_synthetic_training_data(n_samples: int = 500) -> list:
    """Generate synthetic normal metric data for initial model training."""
    np.random.seed(42)
    data = []
    for _ in range(n_samples):
        cpu = np.random.uniform(10, 70)
        ram = np.random.uniform(20, 75)
        disk = np.random.uniform(30, 80)
        data.append([cpu, ram, disk])
    return data