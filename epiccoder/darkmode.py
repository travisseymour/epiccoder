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

import sys
import subprocess
import darkdetect


def is_linux_dark_mode():
    try:
        # Check for GNOME dark mode
        gnome_mode = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"], capture_output=True, text=True
        ).stdout.strip()
        if gnome_mode in ("'prefer-dark'", "'prefer-dark'"):
            return True

        # Check for KDE dark mode
        kde_mode = (
            subprocess.run(
                ["kwriteconfig5", "--file", "kdeglobals", "--group", "KDE", "--key", "LookAndFeelPackage"],
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .lower()
        )
        if "dark" in kde_mode:
            return True

    except FileNotFoundError:
        pass  # gsettings or kwriteconfig5 not found, assume light mode

    return False


def is_dark_mode():
    if sys.platform == "win32" or sys.platform == "darwin":
        return darkdetect.isDark()
    elif sys.platform == "linux":
        return is_linux_dark_mode()
    return False


if __name__ == "__main__":
    if is_dark_mode():
        print("Dark mode is enabled")
    else:
        print("Light mode is enabled")
