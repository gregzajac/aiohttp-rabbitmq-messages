from pathlib import Path
from yaml import safe_load


BASE_DIR = Path(__file__).parent.parent
config_path = BASE_DIR / "config"


def get_config(path):
    with open(path) as f:
        config = safe_load(f)
    return config


config = {
    "development": get_config(config_path / "api_dev.yaml"),
    "testing": get_config(config_path / "api_test.yaml"),
}
