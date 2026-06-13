from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt

from Value.data import app_state


class CustomPlainTextEdit(QtWidgets.QPlainTextEdit):
    now_plain = None
    welcome_length = 94

    def keyPressEvent(self, event):
        try:
            cursor = self.textCursor()
            cursor_pos = cursor.position()
            all_text = self.toPlainText()

            if event.key() == Qt.Key_Backspace:
                if cursor_pos <= self.welcome_length:
                    if not cursor.hasSelection():
                        event.ignore()
                        return
                    sel_start = min(cursor.selectionStart(), cursor.selectionEnd())
                    if sel_start < self.welcome_length:
                        event.ignore()
                        return
                super().keyPressEvent(event)
                return

            elif event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                if cursor_pos <= self.welcome_length:
                    event.ignore()
                    return
                if event.key() in (Qt.Key_Up, Qt.Key_Down):
                    event.ignore()
                    return

            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                last_newline = all_text.rfind('\n')
                current_line = all_text[last_newline + 1:] if last_newline >= 0 else all_text
                command_text = current_line.replace(app_state.entry, "", 1).strip()
                self.parent().parent().parent().process_command(command_text)

                output_text = self.toPlainText()
                output_length = len(output_text)
                cursor = self.textCursor()
                cursor.movePosition(QtGui.QTextCursor.End)
                self.setTextCursor(cursor)
                self.welcome_length = output_length

                self.now_plain = self.toPlainText()
                event.ignore()
            else:
                super().keyPressEvent(event)
        except Exception as e:
            self.parent().parent().parent().error(str(e) + "\n")