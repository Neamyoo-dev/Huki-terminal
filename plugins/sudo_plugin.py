from __future__ import annotations

import ctypes
import os
import subprocess
import tempfile
import threading
from ctypes import wintypes


class SudoPlugin:
    _SEE_MASK_NOCLOSEPROCESS = 0x00000040
    _SEE_MASK_NO_CONSOLE = 0x00008000
    _SW_HIDE = 0

    def __init__(self, main_form=None) -> None:
        self.main_form = main_form

    def get_commands(self) -> dict[str, str]:
        return {"sudo": "cmd_sudo"}

    def get_help(self) -> str:
        return "sudo <command>: Run command with administrator privileges"

    @staticmethod
    def is_admin() -> bool:
        try:
            return bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            return False

    class SHELLEXECUTEINFO(ctypes.Structure):
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("fMask", ctypes.c_ulong),
            ("hwnd", wintypes.HANDLE),
            ("lpVerb", wintypes.LPCWSTR),
            ("lpFile", wintypes.LPCWSTR),
            ("lpParameters", wintypes.LPCWSTR),
            ("lpDirectory", wintypes.LPCWSTR),
            ("nShow", ctypes.c_int),
            ("hInstApp", wintypes.HINSTANCE),
            ("lpIDList", wintypes.LPVOID),
            ("lpClass", wintypes.LPCWSTR),
            ("hKeyClass", wintypes.HKEY),
            ("dwHotKey", wintypes.DWORD),
            ("hIconOrMonitor", wintypes.HANDLE),
            ("hProcess", wintypes.HANDLE),
        ]

    def _run_elevated_await(self, exe: str, args: str, timeout_ms: int = 30000) -> bool:
        sei = self.SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(sei)
        sei.fMask = self._SEE_MASK_NOCLOSEPROCESS | self._SEE_MASK_NO_CONSOLE
        sei.lpVerb = "runas"
        sei.lpFile = exe
        sei.lpParameters = args
        sei.nShow = self._SW_HIDE

        ret = ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei))
        if not ret:
            return False

        h_process = sei.hProcess
        ctypes.windll.kernel32.WaitForSingleObject(h_process, timeout_ms)
        ctypes.windll.kernel32.CloseHandle(h_process)
        return True

    def cmd_sudo(self, *args: str) -> str:
        if not args:
            return "Usage: sudo <command>"

        command = ' '.join(args)

        try:
            if self.is_admin():
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                output = (result.stdout or result.stderr).strip()
                return output if output else "(command completed with no output)"

            tag = f"huki_sudo_{os.getpid()}_{threading.get_ident()}"
            result_file = os.path.join(tempfile.gettempdir(), f"{tag}.txt")
            helper_file = os.path.join(tempfile.gettempdir(), f"{tag}.bat")

            try:
                with open(helper_file, "w", encoding="utf-8") as f:
                    f.write(
                        f'@echo off\r\n'
                        f'cd /d "%~dp0"\r\n'
                        f'>{result_file} 2>&1 (\r\n'
                        f'  {command}\r\n'
                        f')\r\n'
                    )

                self._run_elevated_await("cmd.exe", f'/c "{helper_file}"')

                if os.path.exists(result_file):
                    with open(result_file, "r", encoding="utf-8", errors="replace") as f:
                        output = f.read().strip()
                    return output if output else "(command completed with no output)"

                return "Sudo: 提权命令已执行，但未收到输出"

            finally:
                for f in [helper_file, result_file]:
                    try:
                        if os.path.exists(f):
                            os.remove(f)
                    except Exception:
                        pass

        except subprocess.TimeoutExpired:
            return "Sudo: 命令执行超时（30秒）"
        except Exception as e:
            return f"Error executing command: {str(e)}"
