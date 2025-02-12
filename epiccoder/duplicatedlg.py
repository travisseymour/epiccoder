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

from PyQt5.QtWidgets import QDialog
from pathlib import Path

from epiccoder.duplicateui import Ui_DuplicateFileDialog


class DuplicateFileNameWin(QDialog):
    def __init__(self, dupe_path: Path):
        super(DuplicateFileNameWin, self).__init__()

        self.dupe_path: Path = dupe_path
        self.path_result = Path(dupe_path)  # make a copy

        self.ui = Ui_DuplicateFileDialog()
        self.ui.setupUi(self)

        self.ui.labelError.setVisible(False)
        self.ui.labelError.setMaximumHeight(self.ui.lineEditStem.height())

        self.ui.lineEditStem.setText(self.dupe_path.stem)
        self.ui.labelExt.setText(self.dupe_path.suffix)
        self.ui.labelPath.setText(str(self.dupe_path))

        self.ui.pushButtonCancel.clicked.connect(self.clicked_cancel_button)
        self.ui.pushButtonSelect.clicked.connect(self.clicked_select_button)
        self.ui.lineEditStem.textChanged.connect(self.stem_changed)
        self.ui.lineEditStem.textEdited.connect(self.stem_changed)

        # self.setStyleSheet(
        #
        # )

        # self.setLayout(self.ui.verticalLayout)

    def stem_changed(self, text: str):
        self.path_result = self.dupe_path.with_stem(text)
        self.ui.labelPath.setText(str(self.path_result))
        error_found = not len(text) or self.path_result.exists() is True
        if not text:
            self.ui.labelError.setText("The filename box above cannot be empty!")
        else:
            self.ui.labelError.setText("That file already exists, please choose another file name!")
        self.ui.labelError.setVisible(error_found)
        self.ui.pushButtonSelect.setEnabled(not error_found)

    def clicked_cancel_button(self):
        self.done(False)

    def clicked_select_button(self):
        self.done(True)
