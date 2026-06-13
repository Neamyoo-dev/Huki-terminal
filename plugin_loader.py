import os
import importlib.util
import Value.data as data
from utils.Utils import log


class PluginLoader:
    def __init__(self, terminal, plugin_dir="plugins"):
        self.terminal = terminal
        self.main_form = terminal
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.plugin_dir = os.path.join(current_dir, plugin_dir)
        self.plugins = {}

    def load_plugins(self):
        log("INFO", "PluginLoader", "开始加载插件...")
        log("INFO", "PluginLoader", f"正在从 {self.plugin_dir} 加载插件...")
        log("INFO", "PluginLoader", f"插件目录的绝对路径: {os.path.abspath(self.plugin_dir)}")

        if not os.path.exists(self.plugin_dir):
            os.makedirs(self.plugin_dir)
            log("INFO", "PluginLoader", f"创建插件目录: {self.plugin_dir}")
            return

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('.py'):
                plugin_path = os.path.join(self.plugin_dir, filename)
                plugin = self._load_plugin(plugin_path)
                if plugin:
                    self._register_commands(plugin)

        log("INFO", "PluginLoader", f"已注册的命令: {data.COMMANDS}")

    def _load_plugin(self, plugin_file):
        plugin_name = None
        try:
            plugin_name = os.path.splitext(os.path.basename(plugin_file))[0]

            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and attr.__module__ == module.__name__:
                    plugin_class = attr
                    break

            if plugin_class is None:
                log("ERROR", "PluginLoader", f"加载插件失败 {plugin_name}: 未找到插件类")
                return None

            plugin_instance = plugin_class()

            plugin_instance.plugin_loader = self
            plugin_instance.main_form = self.main_form

            self.plugins[plugin_name] = plugin_instance

            return plugin_instance
        except Exception as e:
            log("ERROR", "PluginLoader", f"加载插件失败 {plugin_name}: {str(e)}")
            return None

    def get_loaded_plugins(self):
        return list(self.plugins.keys())

    def _register_commands(self, plugin):
        try:
            commands = plugin.get_commands()
            for cmd_name, cmd_func in commands.items():
                if isinstance(cmd_func, str):
                    self.terminal.register_command(cmd_name, getattr(plugin, cmd_func))
                else:
                    self.terminal.register_command(cmd_name, cmd_func)
        except Exception as e:
            log("ERROR", "PluginLoader", f"注册命令失败: {str(e)}")

    def get_plugins(self):
        return self.plugins

    def get_all_help(self) -> str:
        help_text = "\n插件命令："
        for plugin_name, plugin in self.plugins.items():
            try:
                if hasattr(plugin, 'get_help'):
                    help_text += "\n" + plugin.get_help()
            except Exception as e:
                log("ERROR", "PluginLoader", f"获取插件 {plugin_name} 的帮助信息失败: {str(e)}")
        return help_text

