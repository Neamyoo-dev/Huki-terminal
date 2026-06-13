from __future__ import annotations

from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor


class EventMixin:
    def warning(self, info: str | list | tuple) -> None:
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        color_format = QTextCharFormat()
        color_format.setForeground(QBrush(QColor("yellow")))
        cursor.setCharFormat(color_format)

        cursor.insertText("\n" + "".join(info))

        cursor.setCharFormat(QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def info(self, info: str | list | tuple) -> None:
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        color_format = QTextCharFormat()
        color_format.setForeground(QBrush(QColor("blue")))
        cursor.setCharFormat(color_format)

        cursor.insertText("\n" + "".join(info))

        cursor.setCharFormat(QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def error(self, info: str | list | tuple | Exception) -> None:
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)

        color_format = QTextCharFormat()
        color_format.setForeground(QBrush(QColor("red")))
        cursor.setCharFormat(color_format)

        if isinstance(info, (list, tuple)):
            cursor.insertText("\n" + "".join(info))
        else:
            cursor.insertText("\n" + str(info))

        cursor.setCharFormat(QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def print(self, value: str | list | tuple, sep: str = "", end: str = "") -> None:
        text = sep.join(value) if isinstance(value, (list, tuple)) else str(value)
        self.text_edit.appendPlainText(text + end)