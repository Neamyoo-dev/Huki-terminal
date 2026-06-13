import ctypes
import subprocess
from typing import Dict


class Sudoplugin:
    def __init__(self, main_form=None):
        self.main_form = main_form

    def get_commands(self) -> Dict[str, str]:
        return {
            "sudo": "cmd_sudo"
        }

    def get_help(self) -> str:
        return "sudo <command>: Run command with administrator privileges"

    def is_admin(self) -> bool:
        """检查当前程序是否以管理员权限运行"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def cmd_sudo(self, *args) -> str:
        """处理 sudo 命令"""
        if not args:
            return "Usage: sudo <command>"

        command = ' '.join(args)

        try:
            if self.is_admin():
                # 已经是管理员权限，直接执行命令
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                return result.stdout if result.stdout else result.stderr
            else:
                # 请求提升权限
                result = ctypes.windll.shell32.ShellExecuteW(
                    None,  # handle to parent window
                    "runas",  # operation to perform
                    "cmd.exe",  # executable
                    f"/c {command}",  # parameters
                    None,  # directory
                    1  # show window
                )
                if result <= 32:  # ShellExecute 返回值小于等于32表示错误
                    return "Failed to execute command with elevated privileges"
                return "Command executed with elevated privileges"

        except Exception as e:
            return f"Error executing command: {str(e)}"
