from __future__ import annotations

import re
import sys

from PyQt5.QtCore import QLocale, Qt, QRect
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QApplication

from Events.CustomPlainTextEdit import CustomPlainTextEdit
from Events.Event import EventMixin
from Value.constants import *
from Value.data import COMMANDS, Config, app_state
from plugin_loader import PluginLoader
from ui import Ui_MainWindow
from utils.Logger_utils import *
from utils.Utils import in_path
from utils.thread_utils import ThreadUtils

app_state.path = os.path.splitdrive(os.path.abspath(os.sep))[
           0] + '\\' if os.name == 'nt' else os.path.abspath(os.sep)
os.chdir(app_state.path)
app_state.entry = f"{app_state.path}> "


def _is_system_command(command: str) -> bool:
    return in_path(command) or os.path.isfile(os.path.join(app_state.path, command))


class MainForm(QMainWindow, Ui_MainWindow, EventMixin):
    name = Config.name
    version = Config.version
    welcome = f"{name} {version}\n{ \
        LICENSE}\nType 'help' to view help information.\n"

    def __init__(self, parent=None) -> None:
        super(MainForm, self).__init__(parent)
        self.log_file_path = None
        self.args = None
        self.setupUi(self)

        create_config_file()
        LoggerUtils.init_logging(self)
        LoggerUtils.save_log(self, "Huki start")

        self.start_x = None
        self.start_y = None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.thread = ThreadUtils()

        self.text_edit = CustomPlainTextEdit(self.frame)

        self.text_edit.setGeometry(QRect(0, 50, 1521, 671))
        self.text_edit.setStyleSheet("QPlainTextEdit#plainTextEdit"
                                     "{background-color: rgb(12, 12, 12);font: 13pt \"Cascadia Code\";color:rgb(255, "
                                     "255, 255);"
                                     "border-radius:13px;}")
        self.text_edit.setObjectName("plainTextEdit")

        self.text_edit.command_entered.connect(self.process_command)
        self.text_edit.error_occurred.connect(self.error)

        self.print(self.welcome)
        self.print(app_state.entry, end="")

        self.text_edit.selectionChanged.connect(self.on_selection_changed)

        self.plugin_loader = PluginLoader(self)
        self.plugin_loader.load_plugins()

    def closeEvent(self, event) -> None:
        LoggerUtils.save_log(self, "终端关闭")
        event.accept()

    def register_command(self, cmd_name: str, cmd_func) -> None:
        COMMANDS[cmd_name] = cmd_func

    def process_command(self, line_text: str) -> None:
        if not line_text:
            self.print(app_state.entry, end="")
            return

        parts = line_text.split('>')
        command_part = parts[-1].strip()

        if not command_part:
            self.print(app_state.entry, end="")
            return

        command_parts = command_part.split()
        if not command_parts:
            self.print(app_state.entry, end="")
            return

        command = command_parts[0]
        args = command_parts[1:]
        LoggerUtils.save_log(self, f"Command: {line_text}")

        try:
            if command in COMMANDS:
                self._execute_command(command, args)
            elif _is_system_command(command):
                self._execute_system_command(line_text)
            else:
                LoggerUtils.save_log(self, f"Command not found: {command}")
                self.error([CMD_NOT_DEFINED, COLON, command])
        except (KeyboardInterrupt, EOFError):
            self.error(["\n", USET_ABORT])
            sys.exit()
        finally:
            self.print(app_state.entry, end="")

    def _execute_command(self, command: str, args: list[str]) -> None:
        method_name = COMMANDS[command]
        if method_name == "exit":
            sys.exit()

        try:
            if callable(method_name):
                output = method_name(*args)
                if output:
                    self.print(output)
            else:
                method = getattr(self, method_name)
                output = method(*args)
                if output:
                    self.print(output)
        except NameError:
            self.error([CMD_NOT_FOUND, COLON, command])
        except AttributeError:
            self.error([CMD_NOT_FOUND, COLON, command])
        except TypeError as e:
            error_msg = str(e)
            if "positional argument" in error_msg:
                if "missing" in error_msg:
                    self.error([command, COLON, MISS_ARG])
                elif "takes" in error_msg:
                    self.error([command, COLON, LARGE_ARG])
            else:
                self.error([command, COLON, error_msg])
        except Exception as e:
            LoggerUtils.save_log(self, f"Command execution error: {str(e)}")
            self.error([str(e)])

    def _execute_system_command(self, raw_line: str) -> None:
        import subprocess
        try:
            result = subprocess.run(raw_line, shell=True, capture_output=True, text=True)
            output = result.stdout + result.stderr
            if output and output.strip():
                self.print(output.strip())
        except Exception as e:
            self.error([str(e)])

    def mouseReleaseEvent(self, event) -> None:
        self.start_x = None
        self.start_y = None

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            super(MainForm, self).mousePressEvent(event)
            self.start_x = event.x()
            self.start_y = event.y()

    def mouseMoveEvent(self, event) -> None:
        super(MainForm, self).mouseMoveEvent(event)
        dis_x = event.x() - self.start_x
        dis_y = event.y() - self.start_y
        self.move(self.x() + dis_x, self.y() + dis_y)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        frame_margin = 10
        title_bar_height = 51
        frame_w = self.width() - 2 * frame_margin
        frame_h = self.height() - 2 * frame_margin
        self.frame.setGeometry(frame_margin, frame_margin, frame_w, frame_h)
        self.text_edit.setGeometry(0, title_bar_height, frame_w, frame_h - title_bar_height)

    def help(self) -> None:
        info = QCoreApplication.translate("MainWindow", """Welcome to {name} {version}!
Commands:
    echo     Output text to screen - echo <value>
    exit     Exit {name} - exit
    cd       Change directory - cd <dir name |.. |.>
            (alias: chdir)
    mkdir    Create directory - mkdir <dir name>
            (alias: md)
    rm       Remove file - rm <filename>
            (alias: remove, del)
    ls       List directory contents - ls
            (alias: dir)
    help     View this message - help""").format(
            name=self.name,
            version=self.version
        )

        info += self.plugin_loader.get_all_help()
        self.print(info)

    def cd(self, dir_name: str = '.') -> None:
        try:
            if dir_name == '.':
                self.print(app_state.path)
                return
            if os.name == 'nt' and re.match(r'^[A-Za-z]:$', dir_name):
                new_path = f"{dir_name}\\"
                if not os.path.exists(new_path):
                    self.error(DIR_NOT_FOUND)
                    return
                os.chdir(new_path)
                app_state.path = new_path
                app_state.entry = f"{app_state.path}> "
                return

            if dir_name == '..':
                new_path = os.path.dirname(app_state.path)
            else:
                new_path = os.path.abspath(os.path.join(app_state.path, dir_name))

            if not os.path.exists(new_path):
                self.error(DIR_NOT_FOUND)
                return

            os.chdir(new_path)
            app_state.path = new_path
            app_state.entry = f"{app_state.path}> "

        except PermissionError:
            self.error(READONLY_FILE)
        except Exception as e:
            self.error(str(e))

    def mkdir(self, dir_name: str) -> None:
        try:
            full_path = os.path.join(app_state.path, dir_name)
            if os.path.exists(full_path):
                self.error("目录已存在")
                return
            os.mkdir(full_path)
        except PermissionError:
            self.error(READONLY_FILE)
        except OSError as e:
            if e.errno == 30:
                self.error(READONLY_FILE)
            elif e.errno == 2:
                self.error("路径无效")
            elif e.errno == 13:
                self.error(READONLY_FILE)
            else:
                self.error(f"创建目录失败: {str(e)}")
        except Exception as e:
            self.error(str(e))

    def echo(self, *string: str) -> None:
        self.print(string, sep=" ")

    def remove(self, filename: str) -> None:
        try:
            filepath = os.path.join(app_state.path, filename)
            if not os.path.exists(filepath):
                raise FileNotFoundError

            if os.path.isfile(filepath):
                os.remove(filepath)
            else:
                os.rmdir(filepath)
        except FileNotFoundError:
            self.error(FILE_NOT_FOUND)
        except PermissionError:
            self.error(READONLY_FILE)
        except Exception as e:
            self.error(str(e))

    def ls(self) -> None:
        self.print(os.listdir(app_state.path), sep=" ")

    def on_selection_changed(self) -> None:
        if self.text_edit.textCursor().hasSelection():
            self.text_edit.setReadOnly(True)
        else:
            self.text_edit.setReadOnly(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MainForm()
    myWin.show()
    sys.exit(app.exec_())