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
import os
import sys
import platform

# Function to determine the available display server
def set_qt_platform():
    # Check if the operating system is Linux
    if platform.system() == 'Linux':
        if 'WAYLAND_DISPLAY' in os.environ:
            os.environ['QT_QPA_PLATFORM'] = 'wayland'
            print("Using Wayland as the display server.")
        else:
            os.environ['QT_QPA_PLATFORM'] = 'xcb'
            print("Using X11 (xcb) as the display server.")
    elif platform.system() == 'Windows':
        # Windows typically does not require setting this
        pass
    elif platform.system() == 'Darwin':  # macOS
        # macOS typically does not require setting this
        pass
    else:
        # Optionally handle other operating systems or set a default
        os.environ['QT_QPA_PLATFORM'] = 'xcb'  # Default to X11 for non-Linux

# Set the appropriate platform before importing QApplication
set_qt_platform()

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import QCoreApplication, QSize
from PyQt5.QtWidgets import QApplication

from epiccoder import set_global_eol_mode
from epiccoder.mainwindow import MainWindow

from pathlib import Path

from epiccoder.splashscreen import SplashScreen
from epiccoder.themes import get_default_font


def get_start_path() -> Path:
    try:
        path = Path(sys.argv[1])
        assert path.is_dir() or path.is_file()
    except (IndexError, AssertionError):
        path = Path.home()
    return path


def main():
    # Create the application instance
    app = QApplication(sys.argv)

    # Create splash screen that will close itself when main window appears
    splash = SplashScreen()
    splash.show()

    # dictate app final close behavior
    app.setQuitOnLastWindowClosed(True)
    # appctxt.lastWindowClosed.conned(run_this_func_before_quit)

    # Set the font for the application
    default_font = get_default_font(family="monospace", size=14)
    app.setFont(default_font)

    if sys.platform.startswith("win"):
        set_global_eol_mode(QsciScintilla.EolWindows)  # \r\n (Windows)
    else:
        set_global_eol_mode(QsciScintilla.EolUnix)  # \n (Default for Linux & other OS)

    # init QSettings once so we can use default constructor throughout project
    QCoreApplication.setOrganizationName("TravisSeymour")
    QCoreApplication.setOrganizationDomain("travisseymour.com")
    QCoreApplication.setApplicationName("EPICcoder")

    start_path = get_start_path()

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
