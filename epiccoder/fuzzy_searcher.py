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
from typing import Optional, Callable, List

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QListWidgetItem, QApplication

import os
import re

from epiccoder import eol_mode
from epiccoder.fileutils import is_binary_file, group_files_by_folder, walkdir, is_hidden
from epiccoder.textutils import read_file_convert_to_utf8, normalize_line_endings


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
        self.search_path: Optional[str] = None
        self.search_text: Optional[str] = None
        self.ignore_hidden: Optional[Callable] = None
        self.get_search_type: Optional[Callable] = None
        self.get_search_files: Optional[Callable] = None
        self.ignore_case: Optional[Callable] = None

    def search_in_file(
            self,
            full_path: str,
            filename: str,
            use_regex: bool,
            ignore_case: bool,
            debug: bool = False
    ) -> List[SearchItem]:
        """
        Searches a single file for matches by loading its full text into memory,
        converting its encoding to UTF-8 using read_file_convert_to_utf8,
        normalizing line endings, splitting into lines, and processing each line.

        If `use_regex` is True, self.search_text is treated as a regex pattern,
        compiled with the appropriate case sensitivity. Otherwise, a standard
        substring search is performed.

        Parameters:
          - full_path: Full path to the file.
          - filename: The file's name.
          - use_regex: Boolean flag; True means treat self.search_text as a regex pattern,
                       False means treat it as plain text.
          - eol_mode: The target EOL mode to normalize to (e.g., QsciScintilla.EolUnix).
          - ignore_case: Boolean flag to ignore case in the search.
          - debug: If True, prints debugging information.

        Returns:
          A list of SearchItem objects for every line that contains a match.
        """
        items: List[SearchItem] = []
        try:
            # Read the file and convert its content to UTF-8.
            text: str = read_file_convert_to_utf8(full_path)
            # Normalize the line endings.
            norm_text: str = normalize_line_endings(text, eol_mode)

            if use_regex:
                flags = re.IGNORECASE if ignore_case else 0
                # Compile the regex pattern using a raw f-string so that user-entered backslashes are treated literally.
                target_regex = re.compile(rf"{self.search_text}", flags)
                # Quick check: if no match is found in the entire text, return early.
                if not target_regex.search(norm_text):
                    return []
            else:
                target_text: str = self.search_text
                # Quick check for substring search.
                if ignore_case:
                    if target_text.lower() not in norm_text.lower():
                        return []
                else:
                    if target_text not in norm_text:
                        return []

            # Proceed to split the text into lines if a match exists.
            lines: List[str] = norm_text.splitlines()

            for i, line in enumerate(lines):
                if use_regex:
                    if m := target_regex.search(line):
                        fd = SearchItem(
                            filename,
                            full_path,
                            i,
                            m.end(),
                            line[m.start():].strip()[:50]  # limiting snippet to 50 characters
                        )
                        items.append(fd)
                else:
                    pos: int
                    if ignore_case:
                        pos = line.lower().find(target_text.lower())
                    else:
                        pos = line.find(target_text)
                    if pos != -1:
                        fd = SearchItem(
                            filename,
                            full_path,
                            i,
                            pos + len(target_text),
                            line[pos:].strip()[:50]
                        )
                        items.append(fd)
        except Exception as e:
            if debug:
                print(f"Error processing file {full_path}: {e}")
        return items

    def search(self):
        ignore_case = self.ignore_case()
        #use_regex = self.use_regex()
        use_regex = False  # TODO: Add a checkbox for this and pass a func to update() to check it
        search_type = self.get_search_type().strip()
        ignore_hidden = self.ignore_hidden()

        debug = False
        items:List[SearchItem] = []

        exclude_dirs = (".git", ".svn", ".hg", ".bzr", "__pycache__", "build", "dist")
        # exclude_files = {".svg", ".png", ".exe", ".pyc", ".qm", ".jpg", ".jpeg", ".gif"}

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
            if len(items) > 5_000:
                break
            for filename in files:
                full_path = str(os.path.join(root, filename))
                if ignore_hidden and is_hidden(full_path):
                    print('\t (skipped hidden file/folder')
                    continue
                print(f'Checking {full_path}')
                if is_binary_file(full_path):
                    print('\t (skipped binary file)')
                    continue

                try:
                    items.extend(
                        self.search_in_file(
                            full_path = full_path,
                            filename = filename,
                            use_regex = use_regex,
                            ignore_case = ignore_case
                        )
                    )
                except (UnicodeDecodeError, OSError) as e:
                    if debug:
                        print(f'Error processing {full_path}: {e}')
                    continue

        self.finished.emit(items)

    def run(self):
        self.search()

    def update(self, pattern, path, ignore_hidden, ignore_case, get_search_type: Callable, get_search_files: Callable):
        print(f'SearchWorker.update called with {pattern=}')
        self.search_text = pattern
        self.search_path = path
        self.ignore_hidden = ignore_hidden
        self.ignore_case = ignore_case
        self.get_search_type = get_search_type
        self.get_search_files = get_search_files
        self.start()
