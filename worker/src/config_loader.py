import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "config", "config.yaml")


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_worker_config():
    cfg = load_config()
    return cfg["worker"], cfg["sensors"], cfg["student_id"]
