
import json
from pathlib import Path
from urllib.parse import urlsplit


DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "monitor.json"
)


def validate_config(config):
    if not isinstance(config, dict):
        raise ValueError("Configuration must be a JSON object")

    thresholds = (
        "cpu_warning_percent",
        "memory_warning_percent",
        "disk_warning_percent",
    )

    for setting in thresholds:
        value = config.get(setting)

        if type(value) not in (int, float) or not 1 <= value <= 100:
            raise ValueError(
                f"{setting} must be a number between 1 and 100"
            )

    timeout = config.get("service_timeout_seconds")

    if type(timeout) not in (int, float) or not 0 < timeout <= 30:
        raise ValueError(
            "service_timeout_seconds must be between 0 and 30"
        )

    url = config.get("service_url")

    if not isinstance(url, str):
        raise ValueError("service_url must be a string")

    try:
        parsed_url = urlsplit(url)
        parsed_url.port
    except ValueError as error:
        raise ValueError("service_url is invalid") from error

    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.hostname
        or parsed_url.username is not None
        or parsed_url.password is not None
    ):
        raise ValueError("service_url must be a valid HTTP or HTTPS URL")

    return config


def load_config(path=DEFAULT_CONFIG_PATH):
    with Path(path).open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    return validate_config(config)
