import pytest
from unittest.mock import patch, MagicMock
from app.healer import restart_container, heal


def test_heal_no_action_when_healthy():
    action = heal(health_status="healthy", anomaly_detected=False)
    assert action == "NO_ACTION"


@patch("app.healer.docker.from_env")
def test_restart_container_success(mock_docker):
    mock_client = MagicMock()
    mock_container = MagicMock()
    mock_container.status = "running"
    mock_client.containers.get.return_value = mock_container
    mock_docker.return_value = mock_client

    result = restart_container("demo_app")
    assert result is True
    mock_container.restart.assert_called_once()


@patch("app.healer.docker.from_env")
def test_restart_container_not_found(mock_docker):
    import docker
    mock_client = MagicMock()
    mock_client.containers.get.side_effect = docker.errors.NotFound("not found")
    mock_docker.return_value = mock_client

    result = restart_container("nonexistent_container")
    assert result is False


@patch("app.healer.restart_container", return_value=True)
def test_heal_triggers_restart_on_anomaly(mock_restart):
    action = heal(health_status="healthy", anomaly_detected=True)
    assert action == "RESTART_SUCCESS"
    mock_restart.assert_called_once()


@patch("app.healer.restart_container", return_value=True)
def test_heal_triggers_restart_on_unhealthy(mock_restart):
    action = heal(health_status="container_down", anomaly_detected=False)
    assert action == "RESTART_SUCCESS"