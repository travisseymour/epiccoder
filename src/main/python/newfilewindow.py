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
import sys
from pathlib import Path
from typing import Union

from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from fbs_runtime.application_context.PyQt5 import ApplicationContext

from version import __version__
from newfile import Ui_formNewFile

class NewFileWidget(QWidget):
    def __init__(self, context: ApplicationContext,
                 folder: Union[Path, str],
                 file_type: str,
                 file_name: str = 'Untitled'):
        super(QWidget, self).__init__()

        self.folder = folder
        self.file_type = file_type.lower()
        self.file_name = file_name if file_name else 'Untitled'
        self.file_types = dict(zip(('.txt','.prs','.txt','.cpp','.h','.py'), (0,1,2,3,4)))
        if not self.file_type in self.file_types:
            raise ValueError(f'Parameter file_type must be in {list(self.file_types)}, not "{file_type}".')

        self.context = context

        # init settings
        self.settings = QSettings()
        self.new_file_widget_width = self.settings.value(
            "new_file_widget_width", type=int, defaultValue=364
        )
        self.new_file_widget_height = self.settings.value(
            "new_file_widget_height", type=int, defaultValue=213
        )

        self.ui = Ui_formNewFile()
        self.init_ui()

        self.setWindowIcon(QIcon(self.context.get_resource("uiicons", "app-icon.svg")))

    def init_ui(self):
        self.resize(self.new_file_widget_width, self.new_file_widget_height)

        style_sheet = Path(self.context.get_resource("css/style.qss")).read_text()
        style_sheet = style_sheet.replace(
            ":/icons/close-icon.svg",
            self.context.get_resource("uiicons", "close-icon.svg"),
        )
        self.setStyleSheet(style_sheet)

        # setup font
        # self.window_font = QFont("Fira Code")
        # self.window_font.setPointSize(12)
        # self.setFont(self.window_font)

        # ==========

        self.ui.comboBoxFileType.setCurrentIndex(self.file_types[self.file_type])
        fn = Path(self.file_name).stem
        fn = Path(fn).with_suffix(self.file_type)
        fn = Path(self.folder, fn)
        if fn.exists():
            for i in range(sys.maxsize):
                fn = Path(self.folder, f"{fn.stem}{i}{fn.suffix}")
                if not fn.exists():
                    break
            else:
                fn = Path(self.folder, f"{fn.stem}{fn.suffix}")
        self.ui.lineEditDefaultFileName.setText(fn.name)

        self.show()

