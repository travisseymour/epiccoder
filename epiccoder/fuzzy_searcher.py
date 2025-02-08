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

from typing import Optional

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QApplication

import os
from pathlib import Path
import re


class SearchItem(QListWidgetItem):
    def __init__(self, name: str, full_path: str, lineno: int, end: int, line: str) -> None:
        """
        Initializes a search result item.

        :param name: Name of the file.
        :param full_path: Full file path.
        :param lineno: Line number where the match was found.
        :param end: End position of the match in the line.
        :param line: The matching part of the line (trimmed).
        """
        self.name = name
        self.full_path = full_path
        self.lineno = lineno
        self.end = end
        self.line = line
        self.formatted = f"{self.name}:{self.lineno}:{self.end} - {self.line} ..."

        super().__init__(self.formatted)

        self.setFont(QApplication.instance().font())

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return self.formatted


class SearchWorker(QThread):
    finished = pyqtSignal(list)

    def __init__(self):
        super(SearchWorker, self).__init__(None)
        self.items = []
        self.search_path: Optional[str] = None
        self.search_text: Optional[str] = None
        self.search_project: Optional[bool] = None

    @staticmethod
    def is_binary(path):
        """
        Check if file is binary
        """
        try:
            with open(path, "rb") as f:
                return b"\0" in f.read(1024)
        except FileNotFoundError:
            return False

    @staticmethod
    def walkdir(path, exclude_dirs: list, exclude_files: list):
        for (
            root,
            dirs,
            files,
        ) in os.walk(path, topdown=True):
            # filtering
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            files[:] = [f for f in files if Path(f).suffix not in exclude_files]
            yield root, dirs, files

    def search(self):
        debug = False
        self.items = []
        # you can add more
        exclude_dirs = {".git", ".svn", ".hg", ".bzr", ".idea", "__pycache__", "venv"}
        if self.search_project:
            exclude_dirs.remove("venv")
        exclude_files = {".svg", ".png", ".exe", ".pyc", ".qm", ".jpg", ".jpeg", ".gif"}

        try:
            reg = re.compile(self.search_text, re.IGNORECASE)
        except re.error as e:
            if debug:
                print(f"Regex error: {e}")
            self.finished.emit([])  # or handle the error as appropriate
            return

        for root, _, files in self.walkdir(self.search_path, exclude_dirs, exclude_files):
            # total search limit
            if len(self.items) > 5_000:
                break
            for filename in files:
                full_path = os.path.join(root, filename)
                if self.is_binary(full_path):
                    continue

                try:
                    with open(full_path, "r", encoding="utf8") as f:
                        try:
                            for i, line in enumerate(f):
                                if m := reg.search(line):
                                    fd = SearchItem(
                                        filename,
                                        full_path,
                                        i,
                                        m.end(),
                                        line[m.start() :].strip()[:50],  # limiting to 50 chars
                                    )
                                    self.items.append(fd)
                        except re.error as e:
                            if debug:
                                print(e)
                except (UnicodeDecodeError, OSError) as e:
                    if debug:
                        print(e)
                    continue

        self.finished.emit(self.items)

    def run(self):
        self.search()

    def update(self, pattern, path, search_project):
        self.search_text = pattern
        self.search_path = path
        self.search_project = search_project
        self.start()
