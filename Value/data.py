from dataclasses import dataclass, field
import os


@dataclass
class Config:
    color: str = "white"
    name: str = "Huki terminal"
    version: float = 1.0
    logging_enabled: bool = True
    log_file_max_size: int = 10240
    log_file_max_age: int = 30
    log_file_max_count: int = 10


@dataclass
class AppState:
    path: str = ""
    entry: str = ""


app_state = AppState()

COMMANDS = {
        "exit": "exit",
        "echo": "echo",
        "cd": "cd",
        "chdir": "cd",
        "mkdir": "mkdir",
        "md": "mkdir",
        "rm": "remove",
        "remove": "remove",
        "del": "remove",
        "ls": "ls",
        "dir": "ls",
        "help": "help",
}