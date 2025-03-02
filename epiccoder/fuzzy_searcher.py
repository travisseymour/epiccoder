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

from typing import Optional, Callable

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QApplication

import os
import re

from epiccoder.fileutils import is_binary_file, group_files_by_folder, walkdir


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

        try:
            self.setFont(QApplication.instance().font())
        except AttributeError:
            ...

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
        self.search_hidden: Optional[Callable] = None
        self.get_search_type: Optional[Callable] = None
        self.get_search_files: Optional[Callable] = None
        self.ignore_case: Optional[Callable] = None

    def search(self):
        ignore_case = self.ignore_case()
        #use_regex = self.use_regex()
        # TODO: Make this an option users can select
        use_regex = False

        debug = False
        self.items.clear()
        # you can add more     rm -rf build/ dist/ *.egg-info
        exclude_dirs = (".git", ".svn", ".hg", ".bzr", "__pycache__", "build", "dist")
        # exclude_files = {".svg", ".png", ".exe", ".pyc", ".qm", ".jpg", ".jpeg", ".gif"}

        # TODO: add ability to toggle regex

        if use_regex:
            try:
                if ignore_case:
                    reg = re.compile(self.search_text, re.IGNORECASE)
                else:
                    reg = re.compile(self.search_text)
            except re.error as e:
                if debug:
                    print(f"Regex error: {e}")
                self.finished.emit([])  # or handle the error as appropriate
                return
        else:
            reg = re.compile(r'.*')

        search_type = self.get_search_type().strip()

        if search_type == "Search All Files in Folder":
            import timeit
            start = timeit.default_timer()
            search_set = walkdir(
                path=self.search_path,
                include_hidden=self.ignore_case(),
                exclude_dirs=exclude_dirs
            )
            print(f'{timeit.default_timer()-start=}')
        else:
            files = self.get_search_files()
            files_grouped_by_folder = group_files_by_folder(files)
            search_set = ((str(folder.resolve()), None, file_list) for folder, file_list in files_grouped_by_folder)


        for root, _, files in search_set:
            # total search limit
            if len(self.items) > 5_000:
                break
            for filename in files:
                full_path = str(os.path.join(root, filename))
                if is_binary_file(full_path):
                    continue

                try:
                    with open(full_path, "r", encoding="utf8") as f:
                        try:
                            if use_regex:
                                for i, line in enumerate(f):
                                    if m := reg.search(line):
                                        fd = SearchItem(
                                            filename,
                                            full_path,
                                            i,
                                            m.end(),
                                            line[m.start():].strip()[:50],  # limiting to 50 chars
                                        )
                                        self.items.append(fd)
                            else:
                                for i, line in enumerate(f):
                                    if (ignore_case and self.search_text.lower() in line.lower()) or self.search_text in line:
                                        fd = SearchItem(
                                            filename,
                                            full_path,
                                            i - 1,
                                            len(line),
                                            line.strip()[:50],  # limiting to 50 chars
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

    def update(self, pattern, path, search_hidden, ignore_case, get_search_type: Callable, get_search_files: Callable):
        print(f'SearchWorker.update called with {pattern=}')
        self.search_text = pattern
        self.search_path = path
        self.search_hidden = search_hidden
        self.ignore_case = ignore_case
        self.get_search_type = get_search_type
        self.get_search_files = get_search_files
        self.start()
