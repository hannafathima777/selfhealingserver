import time
import docker
from app.config import TARGET_CONTAINER
from app.logger import log_event


def restart_container(container_name: str = TARGET_CONTAINER) -> bool:
    """Restart the specified Docker container."""
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        log_event("HEALER", f"Restarting container '{container_name}'...", "RESTART")
        container.restart(timeout=10)
        time.sleep(5)  # Wait for the container to come back up
        container.reload()
        if container.status == "running":
            log_event("HEALER", f"Container '{container_name}' restarted successfully.", "SUCCESS")
            return True
        else:
            log_event("HEALER", f"Container '{container_name}' failed to restart.", "FAILED")
            return False
    except docker.errors.NotFound:
        log_event("HEALER", f"Container '{container_name}' not found. Cannot restart.", "ERROR")
        return False
    except Exception as e:
        log_event("HEALER", f"Restart failed: {e}", "ERROR")
        return False


def stop_container(container_name: str = TARGET_CONTAINER) -> bool:
    """Stop the specified Docker container."""
    try:
        client = docker.from_env()
        container = client.containers.get(container_name)
        container.stop(timeout=10)
        log_event("HEALER", f"Container '{container_name}' stopped.", "STOPPED")
        return True
    except Exception as e:
        log_event("HEALER", f"Stop failed: {e}", "ERROR")
        return False


def heal(health_status: str, anomaly_detected: bool, container_name: str = TARGET_CONTAINER) -> str:
    """
    Decide and perform the appropriate healing action.
    Returns the action taken as a string.
    """
    if health_status in ("container_down", "app_unresponsive") or anomaly_detected:
        success = restart_container(container_name)
        return "RESTART_SUCCESS" if success else "RESTART_FAILED"
    return "NO_ACTION"