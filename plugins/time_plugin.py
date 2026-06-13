from __future__ import annotations

from datetime import datetime


class TimePlugin:
    def get_commands(self) -> dict[str, str]:
        return {"time": "cmd_time", "now": "cmd_time"}

    def get_help(self) -> str:
        return "time/now: 显示当前时间 - time"

    def cmd_time(self, *args: str) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
