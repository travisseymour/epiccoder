"""
EPICcoder is a minimal programmer's text editor created for use with the
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

from typing import Literal

from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication

from epiccoder.mainwindow import MainWindow

import sys
from pathlib import Path


def get_default_font(family: Literal["sans-serif", "serif", "monospace"] = "monospace", size: int = 14) -> QFont:
    """Returns a cross-platform QFont object with fallbacks."""
    font_families = {
        "sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "Sans-serif"],
        "serif": ["Times New Roman", "Times", "Liberation Serif", "Serif"],
        "monospace": ["Courier New", "Courier", "DejaVu Sans Mono", "Monospace"],
    }

    font = QFont()
    for fam in font_families[family]:  # family is guaranteed to be a valid key
        font.setFamily(fam)
        if QFont(fam).exactMatch():  # Ensures the font exists on the system
            break

    font.setPointSize(size)
    return font


def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # dictate app final close behavior
    app.setQuitOnLastWindowClosed(True)
    # appctxt.lastWindowClosed.conned(run_this_func_before_quit)

    # Set the font for the application
    default_font = get_default_font(family="monospace", size=14)
    QApplication.instance().setFont(default_font)

    # init QSettings once so we can use default constructor throughout project
    QCoreApplication.setOrganizationName("TravisSeymour")
    QCoreApplication.setOrganizationDomain("travisseymour.com")
    QCoreApplication.setApplicationName("EPICcoder")

    try:
        start_path = Path(sys.argv[1])
        assert start_path.is_dir() or start_path.is_file()
    except:
        start_path = Path.home()

    main_win = MainWindow()
    main_win.file_manager_frame.resize(QSize(200, main_win.file_manager_frame.height()))
    main_win.set_folder(start_path if start_path.is_dir() else start_path.parent)
    if start_path.is_file():
        main_win.open_file(start_path)
    main_win.show()
    exit_code = app.exec_()

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
