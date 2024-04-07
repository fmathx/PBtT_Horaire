from pathlib import Path


def get_repo_dir():
    return Path(__file__).parent


def get_definitions_file() -> Path:
    return get_repo_dir() / "events_definitions.json"
