"""
EPICcoder is a minimal programmer's text editor created for use with the
EPIC, EPICpy and pyEPIC simulation environments.
Copyright (C) 2022 Travis L. Seymour, PhD

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

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, QSettings
from PyQt5.QtGui import QFontDatabase
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from mainwindow import MainWindow
import sys
from pathlib import Path


class AppContext(ApplicationContext):
    def __init__(self):
        super(AppContext, self).__init__()
        self.main_win = None

        fonts = QFontDatabase()
        fonts.addApplicationFont(
            self.get_resource("fonts", "FiraCode", "FiraCode-Regular.ttf")
        )
        fonts.addApplicationFont(
            self.get_resource("fonts", "FiraCode", "FiraCode-Bold.ttf")
        )
        fonts.addApplicationFont(self.get_resource("fonts", "Consolas", "CONSOLA.TTF"))
        fonts.addApplicationFont(self.get_resource("fonts", "Consolas", "CONSOLAB.TTF"))
        fonts.addApplicationFont(
            self.get_resource("fonts", "JetBrainsMono", "JetBrainsMono-Regular.ttf")
        )
        fonts.addApplicationFont(
            self.get_resource("fonts", "JetBrainsMono", "JetBrainsMono-Bold.ttf")
        )

    def run(self):
        try:
            start_path = Path(sys.argv[1])
            assert start_path.is_dir() or start_path.is_file()
        except:
            start_path = Path.home()

        self.main_win = MainWindow(context=self)
        self.main_win.set_folder(
            start_path if start_path.is_dir() else start_path.parent
        )
        if start_path.is_file():
            self.main_win.open_file(start_path)
        self.main_win.show()
        return self.app.exec_()


if __name__ == "__main__":
    appctxt = AppContext()

    # init QSettings once so we can use default constructor throughout project
    QCoreApplication.setOrganizationName("TravisSeymour")
    QCoreApplication.setOrganizationDomain("travisseymour.com")
    QCoreApplication.setApplicationName("EPICcoder")

    # dictate app final close behavior
    # appctxt.app.connect(appctxt.app, QtCore.SIGNAL("lastWindowClosed()"),
    #                     appctxt.app, QtCore.SLOT("quit()"))

    appctxt.app.setQuitOnLastWindowClosed(True)
    # appctxt.lastWindowClosed.conned(run_this_func_before_quit)

    exit_code = appctxt.run()
    sys.exit(exit_code)
