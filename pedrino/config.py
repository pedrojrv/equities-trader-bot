import yaml

from pathlib import Path


def get_database_path() -> Path:
    config = yaml.load("config.yaml")
    database_path = config['DATABASE_PATH']
    return Path(database_path)
