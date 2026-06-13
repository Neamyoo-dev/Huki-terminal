from __future__ import annotations

import ctypes
import subprocess


class SudoPlugin:
    def __init__(self, main_form=None) -> None:
        self.main_form = main_form

    def get_commands(self) -> dict[str, str]:
        return {"sudo": "cmd_sudo"}

    def get_help(self) -> str:
        return "sudo <command>: Run command with administrator privileges"

    def is_admin(self) -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    def cmd_sudo(self, *args: str) -> str:
        if not args:
            return "Usage: sudo <command>"

        command = ' '.join(args)

        try:
            if self.is_admin():
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.stdout if result.stdout else result.stderr
            else:
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,
                    "runas",
                    "cmd.exe",
                    f"/c {command}",
                    None,
                    1
                )
                if result <= 32:
                    return "Failed to execute command with elevated privileges"
                return "Command executed with elevated privileges"

        except Exception as e:
            return f"Error executing command: {str(e)}"
