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

from typing import Literal

from PyQt5.QtGui import QFont


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


theme = {
    "Monokai": {
        "light": {"foreground": "#49483E", "background": "#F8F8F2"},
        "dark": {"foreground": "#F8F8F2", "background": "#272822"},
    }
}
