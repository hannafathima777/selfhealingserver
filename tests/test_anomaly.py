import pytest
from app.anomaly_detector import (
    generate_synthetic_training_data,
    train_model,
    is_anomaly,
    load_model
)


@pytest.fixture(scope="module")
def trained_model():
    data = generate_synthetic_training_data(300)
    return train_model(data)


def test_synthetic_data_shape():
    data = generate_synthetic_training_data(100)
    assert len(data) == 100
    assert all(len(row) == 3 for row in data)


def test_train_model_returns_model(trained_model):
    assert trained_model is not None


def test_normal_metrics_not_anomaly(trained_model):
    # These are within normal operating ranges
    result = is_anomaly(40.0, 50.0, 60.0, trained_model)
    assert result is False


def test_extreme_metrics_are_anomaly(trained_model):
    # Extreme values should be flagged
    result = is_anomaly(99.9, 99.9, 99.9, trained_model)
    assert result is True


def test_no_model_uses_threshold_normal():
    result = is_anomaly(30.0, 40.0, 50.0, model=None)
    assert result is False


def test_no_model_uses_threshold_anomaly():
    result = is_anomaly(95.0, 95.0, 95.0, model=None)
    assert result is True