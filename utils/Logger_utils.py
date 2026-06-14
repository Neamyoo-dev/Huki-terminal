from __future__ import annotations

import json
import os
import time

from Value.data import Config


def _get_config_paths() -> tuple[str, str, str]:
    user_folder = os.path.expanduser("~")
    config_folder = os.path.join(user_folder, ".huki")
    config_file = os.path.join(config_folder, "config.json")
    return user_folder, config_folder, config_file


def create_config_file() -> None:
    _, config_folder, config_file = _get_config_paths()

    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    if not os.path.exists(config_file):
        config_data = {"logging_enabled": True,
                       "log_file_max_size": 10240,
                       "log_file_max_age": 30,
                       "log_file_max_count": 10}
    else:
        with open(config_file, "r") as f:
            config_data = json.load(f)

    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=4)


def load_logging_settings() -> None:
    _, _, config_file = _get_config_paths()

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config_data = json.load(f)

        Config.logging_enabled = config_data.get("logging_enabled", True)
        Config.log_file_max_size = config_data.get("log_file_max_size", 10240)
        Config.log_file_max_age = config_data.get("log_file_max_age", 30)
        Config.log_file_max_count = config_data.get("log_file_max_count", 10)


def save_logging_settings() -> None:
    _, _, config_file = _get_config_paths()

    config_data = {
        "logging_enabled": Config.logging_enabled,
        "log_file_max_size": Config.log_file_max_size,
        "log_file_max_age": Config.log_file_max_age,
        "log_file_max_count": Config.log_file_max_count
    }

    with open(config_file, "w") as f:
        json.dump(config_data, f, indent=4)


def _cleanup_logs_file(log_file_path: str) -> None:
    if not log_file_path or not os.path.exists(log_file_path):
        return

    log_folder = os.path.dirname(log_file_path)
    log_files = [f for f in os.listdir(log_folder) if f.startswith("huki_log")]
    if len(log_files) <= Config.log_file_max_count:
        return

    log_files.sort(key=lambda f: os.path.getmtime(os.path.join(log_folder, f)))
    while len(log_files) > Config.log_file_max_count:
        os.remove(os.path.join(log_folder, log_files.pop(0)))


def _archive_log_file(log_file_path: str) -> str | None:
    if not log_file_path:
        return None

    log_folder = os.path.dirname(log_file_path)
    log_file_base = os.path.basename(log_file_path)
    log_file_name, log_file_ext = os.path.splitext(log_file_base)
    archive_file_name = f"{log_file_name}_{time.strftime('%Y%m%d%H%M%S')}{log_file_ext}"
    archive_file_path = os.path.join(log_folder, archive_file_name)

    os.rename(log_file_path, archive_file_path)
    return archive_file_path


class LoggerUtils:
    def __init__(self) -> None:
        self.log_file_path: str | None = None

    def init_logging(self) -> None:
        _, config_folder, config_file = _get_config_paths()

        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        if not os.path.exists(config_file):
            create_config_file()

        load_logging_settings()

        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")
        self.log_file_path = os.path.join(config_folder, f"huki_log_{timestamp}.txt")
        if not os.path.exists(self.log_file_path):
            with open(self.log_file_path, "w") as f:
                pass

    def save_log(self, message: str) -> None:
        if not Config.logging_enabled:
            return

        log_file_path = getattr(self, 'log_file_path', None)
        if not log_file_path:
            self.init_logging()

        log_file_path = getattr(self, 'log_file_path', None)
        if not log_file_path:
            return

        if os.path.getsize(log_file_path) > Config.log_file_max_size:
            _archive_log_file(log_file_path)
            self.init_logging()
            log_file_path = getattr(self, 'log_file_path', None)
            if not log_file_path:
                return

        with open(log_file_path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

        _cleanup_logs_file(log_file_path)

    def archive_log(self) -> None:
        _archive_log_file(self.log_file_path)
        self.log_file_path = None