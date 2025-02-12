"""
EPIC Coder is a minimal programmer's text editor created for use with the
EPIC, EPICpy and pyEPIC simulation environments.

Copyright (C) 2022-2025 Travis L. Seymour, PhD

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Optional
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication
from PyQt5.QtGui import QFont


def question_box(
    parent: Optional[QWidget],
    title: str,
    text: str,
    buttons: QMessageBox.StandardButtons = QMessageBox.Yes | QMessageBox.No,
    font: Optional[QFont] = None,
) -> int:
    """
    Display a question message box with an optional font and a question mark icon.

    :param parent: The parent widget for the message box (can be None for no parent).
    :param title: The title of the message box.
    :param text: The text content of the message box.
    :param buttons: Buttons to display (default is QMessageBox.Yes | QMessageBox.No).
    :param font: Optional QFont object to specify the font of the message box. Defaults to None.
    :return: The button clicked (e.g., QMessageBox.Yes or QMessageBox.No).
    """
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Question)  # Set the question mark icon
    message_box.setStandardButtons(buttons)

    if font is not None:
        message_box.setFont(font)
    else:
        message_box.setFont(QApplication.instance().font())

    return message_box.exec_()


def critical_box(
    parent: Optional[QWidget],
    title: str,
    text: str,
    buttons: QMessageBox.StandardButtons = QMessageBox.Ok,
    font: Optional[QFont] = None,
) -> int:
    """
    Display a critical message box with an optional font and a critical icon.

    :param parent: The parent widget for the message box (can be None for no parent).
    :param title: The title of the message box.
    :param text: The text content of the message box.
    :param buttons: Buttons to display (default is QMessageBox.Ok).
    :param font: Optional QFont object to specify the font of the message box. Defaults to None.
    :return: The button clicked (e.g., QMessageBox.Ok).
    """
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Critical)  # Set the critical icon
    message_box.setStandardButtons(buttons)

    if font is not None:
        message_box.setFont(font)
    else:
        message_box.setFont(QApplication.instance().font())

    return message_box.exec_()


def warning_box(
    parent: Optional[QWidget],
    title: str,
    text: str,
    buttons: QMessageBox.StandardButtons = QMessageBox.Ok,
    font: Optional[QFont] = None,
) -> int:
    """
    Display a warning message box with an optional font and a warning icon.

    :param parent: The parent widget for the message box (can be None for no parent).
    :param title: The title of the message box.
    :param text: The text content of the message box.
    :param buttons: Buttons to display (default is QMessageBox.Ok).
    :param font: Optional QFont object to specify the font of the message box. Defaults to None.
    :return: The button clicked (e.g., QMessageBox.Ok).
    """
    message_box = QMessageBox(parent)
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Warning)  # Set the warning icon
    message_box.setStandardButtons(buttons)

    if font is not None:
        message_box.setFont(font)
    else:
        message_box.setFont(QApplication.instance().font())

    return message_box.exec_()
