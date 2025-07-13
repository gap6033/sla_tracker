import yaml
import threading
from pathlib import Path
from typing import Dict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging
logger = logging.getLogger(__name__)

CONFIG_PATH = Path.cwd() / "config" / "sla_config.yaml"

# Thread-safe shared config
_sla_config_lock = threading.Lock()
_sla_config_data: Dict = {}

def _load_yaml_config() -> Dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def _set_config(new_config: Dict):
    global _sla_config_data
    with _sla_config_lock:
        _sla_config_data = new_config

def get_sla_config() -> Dict:
    with _sla_config_lock:
        return _sla_config_data.copy()

def get_sla_target(customer_tier: str, clock_type: str) -> int:
    config = get_sla_config()
    tier = config["customer_tier"].get(customer_tier.lower())
    if not tier:
        raise ValueError(f"Unknown customer tier: {customer_tier}")
    raw = tier.get(f"{clock_type}_sla")
    if not raw:
        raise ValueError(f"SLA not defined for {clock_type} in {customer_tier}")
    
    if raw.endswith("h"):
        return int(raw[:-1]) * 3600
    elif raw.endswith("m"):
        return int(raw[:-1]) * 60
    elif raw.endswith("s"):
        return int(raw[:-1])
    else:
        raise ValueError(f"Unsupported SLA format: {raw}")

# ----- Watchdog integration -----

class SLAConfigChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("sla_config.yaml"):
            try:
                updated = _load_yaml_config()
                _set_config(updated)
                logger.info("SLA config reloaded.")
            except Exception as e:
                logger.info(f"Failed to reload SLA config: {e}")

def start_sla_config_watcher():
    observer = Observer()
    handler = SLAConfigChangeHandler()
    observer.schedule(handler, path=CONFIG_PATH.parent.as_posix(), recursive=False)
    observer.start()
