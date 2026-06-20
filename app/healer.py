import time
import docker
from app.config import TARGET_CONTAINER
from app.logger import log_event

# ---------- GLOBAL SETTINGS ----------
client = docker.from_env()

MAX_RESTARTS = 10
restart_count = 0

last_restart_time = 0
COOLDOWN_SECONDS = 30


# ---------- RESTART ----------
def restart_container(container_name: str = TARGET_CONTAINER) -> bool:
    try:
        container = client.containers.get(container_name)

        log_event("HEALER", f"Restarting container '{container_name}'...", "RESTART")

        container.restart(timeout=10)
        time.sleep(5)
        container.reload()

        if container.status == "running":
            log_event("HEALER", f"Container '{container_name}' restarted successfully.", "SUCCESS")
            return True
        else:
            log_event("HEALER", f"Container '{container_name}' failed to restart.", "FAILED")
            return False

    except docker.errors.NotFound:
        log_event("HEALER", f"Container '{container_name}' not found.", "ERROR")
        return False

    except Exception as e:
        log_event("HEALER", f"Restart failed: {e}", "ERROR")
        return False


# ---------- STOP ----------
def stop_container(container_name: str = TARGET_CONTAINER) -> bool:
    try:
        container = client.containers.get(container_name)
        container.stop(timeout=10)
        log_event("HEALER", f"Container '{container_name}' stopped.", "STOPPED")
        return True
    except Exception as e:
        log_event("HEALER", f"Stop failed: {e}", "ERROR")
        return False


# ---------- HEAL LOGIC ----------
def heal(health_status: str, anomaly_detected: bool, container_name: str = TARGET_CONTAINER) -> str:
    global restart_count, last_restart_time

    current_time = time.time()

    # RESET when system is healthy
    if health_status == "healthy" and not anomaly_detected:
        restart_count = 0

    # COOLDOWN
    if current_time - last_restart_time < COOLDOWN_SECONDS:
        print("[HEALER] Cooldown active. Skipping restart.")
        return "COOLDOWN_ACTIVE"

    # LIMIT CHECK
    print(f"[HEALER] restart_count={restart_count}, MAX_RESTARTS={MAX_RESTARTS}")
    if restart_count >= MAX_RESTARTS:
        print("[HEALER] MAX RESTART LIMIT reached")
        return "RESTART_BLOCKED"

    # TRIGGER CONDITION
    if health_status in ("container_down", "app_unresponsive") or anomaly_detected:

        print(f"[HEALER] Restart triggered for {container_name}")

        success = restart_container(container_name)

        if success:
            restart_count += 1
            last_restart_time = current_time

            try:
                with open("data/restart_count.txt", "r") as f:
                    count = int(f.read().strip())

                with open("data/restart_count.txt", "w") as f:
                    f.write(str(count + 1))

            except Exception as e:
                print(f"[HEALER] Restart count update failed: {e}")

        return "RESTART_SUCCESS" if success else "RESTART_FAILED"

    return "NO_ACTION"