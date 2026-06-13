import os
import stat
import time


def in_path(program_name):
    path_env = os.environ.get('PATH', '')
    directories = path_env.split(os.pathsep)

    for directory in directories:
        if not directory:
            continue
        program_path = os.path.join(directory, program_name)
        if os.path.isfile(program_path):
            if os.name == 'nt':
                return True
            if os.access(program_path, os.X_OK):
                return True
        if os.name == 'nt':
            for ext in ['.exe', '.bat', '.cmd']:
                full_path = program_path + ext
                if os.path.isfile(full_path):
                    return True
    return False


def log(log_type: str, module: str, message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [Huki/{log_type}] [{module}] {message}")


class Utils:
    def __init__(self):
        pass
