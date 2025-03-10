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

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon

from epiccoder.resource import get_resource
from epiccoder.themes import get_default_font


class ThreeStateButton(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Track the current state
        self.state = 0

        # Use built-in Qt icons
        style = self.style()
        self.icons = [
            QIcon(get_resource("images", "search", "search_folder_glass.png")),  # Search Folder
            QIcon(get_resource("images", "search", "search_files_glass.png")),  # Search All Open Files
            QIcon(get_resource("images", "search", "search_file_glass.png")),  # Search Current File Only
        ]

        self.labels = [" Search All Files in Folder", " Search All Open Files", " Search Current File Only"]

        # Create the button with the correct initial label
        self.button = QPushButton(self.labels[self.state])  # ✅ Fix: Start with correct label
        self.button.setIconSize(QSize(40, 40))
        self.button.setStyleSheet("font-size: 12pt;")
        self.button.setCheckable(True)  # Allows toggling
        self.button.setIcon(self.icons[self.state])  # Set initial icon

        # Connect click event
        self.button.clicked.connect(self.toggle_state)

        layout.addWidget(self.button)
        self.setLayout(layout)

    def toggle_state(self):
        """Cycle through 3 states and update icon & text."""
        self.state = (self.state + 1) % 3  # Cycle through 0 → 1 → 2 → 0
        self.button.setIcon(self.icons[self.state])
        self.button.setText(self.labels[self.state])

    def get_current_state_label(self) -> str:
        """Returns the label of the current state."""
        return self.labels[self.state].strip()


if __name__ == "__main__":
    # Run the app
    app = QApplication([])

    default_font = get_default_font(family="monospace", size=14)
    app.setFont(default_font)

    window = ThreeStateButton()
    window.show()

    # Example usage
    print(window.get_current_state_label())  # Prints "Folder" (initial state)

    app.exec()
