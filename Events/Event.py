from PyQt5 import QtCore

from Events.CustomPlainTextEdit import *
from ui import Ui_MainWindow


class Event(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.text_edit = CustomPlainTextEdit(self.frame)

        self.text_edit.setGeometry(QtCore.QRect(0, 50, 1521, 671))
        self.text_edit.setStyleSheet("QPlainTextEdit#plainTextEdit"
                                     "{background-color: rgb(12, 12, 12);font: 13pt \"Cascadia Code\";color:rgb(255, "
                                     "255, 255);"
                                     "border-radius:13px;}")
        self.text_edit.setObjectName("plainTextEdit")

    def warning(self, info: str | list | tuple):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        color_format = QtGui.QTextCharFormat()
        color_format.setForeground(QtGui.QBrush(QtGui.QColor("yellow")))
        cursor.setCharFormat(color_format)

        cursor.insertText("\n" + "".join(info))

        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def info(self, info: str | list | tuple):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        color_format = QtGui.QTextCharFormat()
        color_format.setForeground(QtGui.QBrush(QtGui.QColor("blue")))
        cursor.setCharFormat(color_format)

        cursor.insertText("\n" + "".join(info))

        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def error(self, info: str | list | tuple | Exception):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)

        color_format = QtGui.QTextCharFormat()
        color_format.setForeground(QtGui.QBrush(QtGui.QColor("red")))
        cursor.setCharFormat(color_format)

        if isinstance(info, (list, tuple)):
            cursor.insertText("\n" + "".join(info))
        else:
            cursor.insertText("\n" + str(info))

        cursor.setCharFormat(QtGui.QTextCharFormat())
        self.text_edit.setTextCursor(cursor)

    def print(self, value: str | list | tuple, sep="", end=""):
        text = sep.join(value) if isinstance(value, (list, tuple)) else str(value)
        self.text_edit.appendPlainText(text + end)
