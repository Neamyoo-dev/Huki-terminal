from __future__ import annotations


class ShowPlugins:
    def __init__(self) -> None:
        self.plugin_loader = None

    def get_commands(self) -> dict[str, str]:
        return {"plugins": "cmd_plugins", "pl": "cmd_plugins"}

    def get_help(self) -> str:
        return "plugins/pl: 显示所有已加载的插件"

    def cmd_plugins(self, *args: str) -> str:
        plugins = self.plugin_loader.get_loaded_plugins()
        if plugins:
            result = "已加载的插件:\n"
            for plugin in plugins:
                result += f"- {plugin}\n"
            return result.strip()
        return "没有已加载的插件"
