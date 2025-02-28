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
from functools import partial
from typing import Optional, List

import sys
from pathlib import Path

from PyQt5.QtCore import QSettings, Qt, QSize, QDir, QModelIndex, QEvent
from PyQt5.QtGui import QIcon, QFont, QPixmap, QResizeEvent, QCloseEvent, QShowEvent, QColor
from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QFrame,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QSplitter,
    QFileSystemModel,
    QTreeView,
    QLineEdit,
    QCheckBox,
    QListWidget,
    QSpacerItem,
    QTabWidget,
    QMessageBox,
    QFileDialog,
    QMenu,
    QAction,
    QApplication,
    QTabBar,
    QProxyStyle,
    QStyle,
)

from epiccoder import config
from epiccoder.aboutwindow import AboutWin
from epiccoder.customeditor import CustomEditor
from epiccoder.darkmode import is_dark_mode
from epiccoder.duplicatedlg import DuplicateFileNameWin
from epiccoder.fuzzy_searcher import SearchWorker, SearchItem
from epiccoder.questionbox import question_box, critical_box, warning_box
from epiccoder.resource import get_resource
from epiccoder.textutils import normalize_line_endings
from epiccoder.themes import theme

from epiccoder.version import __version__


# Configurable generator for integers, starting at 1 by default
def integer_generator(start=1, end=sys.maxsize):
    """Generator for successive integers from start to end."""
    for i in range(start, end):
        yield i


int_gen = integer_generator(0)  # Starts from 1 up to sys.maxsize


class CustomTabBarStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QStyle.PM_TabBarScrollButtonWidth:
            return 30
        return super(CustomTabBarStyle, self).pixelMetric(metric, option, widget)


class SmallTabBar(QTabBar):
    def __init__(self, parent=None):
        super(SmallTabBar, self).__init__(parent)
        # Ensure the tabs are closable.
        self.setTabsClosable(True)
        # Set our custom style so that the scroll buttons are wider.
        self.setStyle(CustomTabBarStyle())

    def tabSizeHint(self, index):
        size = super(SmallTabBar, self).tabSizeHint(index)
        # Instead of halving the height completely, reduce it to (for example) 70% of the original
        # to leave enough room for the close button.
        new_height = int(size.height() * 0.7)
        size.setHeight(new_height)
        return size


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.set_new_tab_busy = None
        self.force_close: bool = False

        theme_name = QSettings().value("theme", "Monokai")
        self.default_text_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["foreground"])
        self.default_bg_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["background"])

        # add before init
        self.side_bar_clr = self.default_bg_color  # "#282c34"

        # init settings
        self.settings = QSettings()

        self.main_window_width = self.settings.value("main_window_width", type=int, defaultValue=1200)
        self.main_window_height = self.settings.value("main_window_height", type=int, defaultValue=800)

        self.window_font: Optional[QFont] = None
        self.last_h_split_sizes: List[int] = []
        self.dupe_file: Optional[QMenu] = None
        self.delete_file: Optional[QMenu] = None
        self.model: Optional[QFileSystemModel] = None
        self.tree_view: Optional[QTreeView] = None
        self.search_frame: Optional[QFrame] = None
        self.search_git_checkbox: Optional[QCheckBox] = None
        self.search_worker: Optional[SearchWorker] = None
        self.search_list_view: Optional[QListWidget] = None
        self.tab_view: Optional[QTabWidget] = None

        self.h_split = None
        self.file_manager_frame = None
        self.side_bar = None

        self.init_ui()

        self.current_side_bar = None

        self.setWindowIcon(QIcon(get_resource("uiicons", "app-icon.svg")))

        self.setMinimumWidth(500)

    def init_ui(self):
        self.setWindowTitle(f"EPIC Coder v{__version__} | Travis L. Seymour, PhD.")
        self.resize(self.main_window_width, self.main_window_height)

        style_sheet = Path(get_resource("css/style.qss")).read_text()
        style_sheet = style_sheet.replace(
            ":/icons/close-icon.svg",
            str(get_resource("uiicons", "close-icon.svg")),
        )
        self.setStyleSheet(style_sheet)

        # setup font
        self.window_font = QApplication.instance().font()
        self.setFont(self.window_font)

        self.set_up_menu()
        self.set_up_body()
        self.statusBar().setFont(self.window_font)
        self.statusBar().showMessage("hello")

        self.last_h_split_sizes = [400, self.width() - 400]
        self.h_split.setSizes(self.last_h_split_sizes)

        # Install event filter on the tab bar so we can update the status bar on hover.
        self.tab_view.tabBar().installEventFilter(self)

        self.show()

    def set_up_menu(self):
        menu_bar = self.menuBar()
        menu_bar.setFont(self.window_font)

        # File Menu
        file_menu = menu_bar.addMenu("File")
        file_menu.setFont(self.window_font)

        # Open File/Folder
        open_file: QAction = file_menu.addAction("Open File")
        open_file.setFont(self.window_font)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)

        open_folder: QAction = file_menu.addAction("Open Folder")
        open_folder.setFont(self.window_font)
        open_folder.setShortcut("Ctrl+K")
        open_folder.triggered.connect(self.open_folder)

        file_menu.addSeparator()

        # Save/SaveAs File
        save_file: QAction = file_menu.addAction("Save")
        save_file.setFont(self.window_font)
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)

        save_as: QAction = file_menu.addAction("Save As")
        save_as.setFont(self.window_font)
        save_as.setShortcut("Ctrl+Shift+S")
        save_as.triggered.connect(self.save_as)

        file_menu.addSeparator()

        # New File SubMenu & Actions
        new_file_menu = QMenu("New File", self)
        new_file_menu.setFont(self.window_font)

        txt_action: QAction = QAction("Text File (*.txt)", self)
        txt_action.triggered.connect(partial(self.new_file, ".txt"))

        prs_action: QAction = QAction("EPIC Production Rule File (*.prs)", self)
        prs_action.triggered.connect(partial(self.new_file, ".prs"))

        py_action: QAction = QAction("Python Code File (*.py)", self)
        py_action.triggered.connect(partial(self.new_file, ".py"))

        cpp_action: QAction = QAction("C++ Code File (*.cpp)", self)
        cpp_action.triggered.connect(partial(self.new_file, ".cpp"))

        h_action: QAction = QAction("C++ Header File (*.h)", self)
        h_action.triggered.connect(partial(self.new_file, ".h"))

        for obj in (txt_action, prs_action, py_action, cpp_action, h_action):
            new_file_menu.addAction(obj)

        file_menu.addMenu(new_file_menu)
        file_menu.addSeparator()

        # Duplicate File
        self.dupe_file: QAction = file_menu.addAction("Duplicate")
        self.dupe_file.setShortcut("Ctrl+D")
        self.dupe_file.triggered.connect(self.duplicate_file)
        self.dupe_file.setEnabled(False)

        file_menu.addSeparator()

        # Delete File
        self.delete_file: QAction = file_menu.addAction("Delete")
        self.delete_file.setShortcut("Ctrl+X")
        self.delete_file.triggered.connect(self.remove_file)
        self.delete_file.setEnabled(False)

        file_menu.addSeparator()

        # Quit Action
        quit_app: QAction = file_menu.addAction("Quit")
        quit_app.setShortcut("Ctrl+Q")
        quit_app.triggered.connect(self.close)

        # Edit menu
        edit_menu: QMenu = menu_bar.addMenu("Edit")
        edit_menu.setFont(self.window_font)

        copy_action: QAction = edit_menu.addAction("Copy")
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)

        paste_action: QAction = edit_menu.addAction("Paste")
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)

        # Help menu
        help_menu: QMenu = menu_bar.addMenu("Help")
        help_menu.setFont(self.window_font)

        about: QAction = help_menu.addAction("About")
        about.setShortcut("Ctrl+A")
        about.triggered.connect(self.show_about)

    def show_about(self):
        about = AboutWin(self)
        about.setFont(QApplication.instance().font())
        about.show()

    def show_help(self):
        pass

    def showEvent(self, event: QShowEvent) -> None:
        config.set_ready(True)
        QMainWindow.showEvent(self, event)

    def get_editor(self, file_path: Path) -> CustomEditor:
        # The CustomEditor is assumed to store the file path in an attribute called `file_path`
        # and it already calls star_func (self.add_star) when its text changes.
        editor = CustomEditor(file_path=file_path, star_func=self.add_star)
        return editor

    @staticmethod
    def is_binary(path):
        """Check if file is binary"""
        with open(path, "rb") as f:
            return b"\0" in f.read(1024)

    def add_star(self, file_path: Path):
        # Add an asterisk (*) to the tab label to indicate unsaved changes.
        # Compare the tab text (after stripping any asterisk) with the file name.
        for i in range(self.tab_view.count()):
            tab_text = self.tab_view.tabText(i)
            clean_text = tab_text.lstrip("*")
            if clean_text == file_path.name:
                if not tab_text.startswith("*"):
                    self.tab_view.setTabText(i, "*" + tab_text)
                return

    def next_new_file_path(self, file_type: str, stem: str = "untitled") -> Path:
        _stem = stem if stem else "untitled"
        for _ in range(9999):
            p = Path(self.model.rootPath(), f"{_stem}{next(int_gen)}{file_type.lower()}")
            if not p.exists():
                return p
        return Path(self.model.rootPath(), f"{_stem}{next(int_gen)}{file_type.lower()}")

    def set_new_tab(self, path: Optional[Path], is_new_file=False, file_type: str = "txt"):
        if self.set_new_tab_busy:
            return

        try:
            self.set_new_tab_busy = True

            if path:
                try:
                    if not path.is_file():
                        return
                except AttributeError:
                    return

            # Normalize the path
            norm_path = path.resolve() if path and not is_new_file else path
            new_file_path = self.next_new_file_path(file_type) if is_new_file else norm_path

            # Check if file is already open by comparing the normalized path.
            for i in range(self.tab_view.count()):
                if self.tab_view.tabToolTip(i) == str(new_file_path):
                    self.tab_view.setCurrentIndex(i)
                    return

            # Create new tab.
            editor: CustomEditor = self.get_editor(new_file_path)
            tab_label = new_file_path.name
            tab_tooltip = str(new_file_path)

            if is_new_file:
                self.tab_view.addTab(editor, f"*{tab_label}")
                self.tab_view.setTabToolTip(self.tab_view.count() - 1, tab_tooltip)
                self.statusBar().showMessage(f"Opened '{new_file_path.name}'", 4000)
                self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
                return

            if self.is_binary(path):
                self.statusBar().showMessage("EPIC Coder Cannot Open Binary Files!", 4000)
                return

            self.tab_view.addTab(editor, tab_label)
            self.tab_view.setTabToolTip(self.tab_view.count() - 1, tab_tooltip)
            try:
                editor.setText(new_file_path.read_text())
            except Exception as e:
                warning_box(
                    self, "Error Reading File", f"Could not read {str(new_file_path)}:\n{str(e)}", font=self.window_font
                )
                return

            self.tab_view.setCurrentIndex(self.tab_view.count() - 1)
            self.statusBar().showMessage(f"Opened {new_file_path.name}", 4000)

            self.dupe_file.setEnabled(self.tab_view.count() > 0)
            self.delete_file.setEnabled(self.tab_view.count() > 0)
        finally:
            self.set_new_tab_busy = False

    def set_cursor_pointer(self, e):
        self.setCursor(Qt.PointingHandCursor)

    def set_cursor_arrow(self, e):
        self.setCursor(Qt.ArrowCursor)

    def get_side_bar_label(self, path, name):
        label = QLabel()
        label.setPixmap(QPixmap(path).scaled(QSize(30, 30)))
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setFont(self.window_font)
        label.mousePressEvent = lambda e: self.show_hide_tab(e, name)
        label.enterEvent = self.set_cursor_pointer
        label.leaveEvent = self.set_cursor_arrow
        return label

    @staticmethod
    def get_frame() -> QFrame:
        frame = QFrame()
        frame.setFrameShape(QFrame.NoFrame)
        frame.setFrameShadow(QFrame.Plain)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #21252b;
                border-radius: 5px;
                border: none;
                padding: 5px;
                color: #D3D3D3;
            }
            QFrame:hover {
                color: white;
            }
            """
        )
        return frame

    def set_up_body(self):
        # Body
        body_frame = QFrame()
        body_frame.setFrameShape(QFrame.NoFrame)
        body_frame.setFrameShadow(QFrame.Plain)
        body_frame.setLineWidth(0)
        body_frame.setMidLineWidth(0)
        body_frame.setContentsMargins(0, 0, 0, 0)
        body_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        body_frame.setLayout(body)

        ##############################
        ###### SIDE BAR ##########
        self.side_bar = QFrame()
        self.side_bar.setFrameShape(QFrame.StyledPanel)
        self.side_bar.setFrameShadow(QFrame.Plain)
        self.side_bar.setStyleSheet(f"background-color: {self.side_bar_clr};")
        side_bar_layout = QVBoxLayout()
        side_bar_layout.setContentsMargins(5, 10, 5, 0)
        side_bar_layout.setSpacing(0)
        side_bar_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        folder_label = self.get_side_bar_label(get_resource("uiicons", "folder-icon-blue.svg"), "folder-icon")
        folder_label.setToolTip('View Folder Contents')
        side_bar_layout.addWidget(folder_label)

        search_label = self.get_side_bar_label(get_resource("uiicons", "search-icon.svg"), "search-icon")
        search_label.setToolTip('Search All Files')
        side_bar_layout.addWidget(search_label)

        search_local_label = self.get_side_bar_label(get_resource("uiicons", "search-local-icon.svg"), "search-local-icon")
        search_local_label.setToolTip('Search Current File')
        side_bar_layout.addWidget(search_local_label)

        self.side_bar.setLayout(side_bar_layout)

        # Split view
        self.h_split = QSplitter(Qt.Horizontal)

        ##############################
        ###### FILE MANAGER ##########
        self.file_manager_frame = self.get_frame()
        self.file_manager_frame.setMaximumWidth(self.window().width())
        self.file_manager_frame.setMinimumWidth(200)
        tree_frame_layout = QVBoxLayout()
        tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        tree_frame_layout.setSpacing(0)

        self.model = QFileSystemModel()
        self.model.setRootPath(os.getcwd())
        self.model.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs | QDir.Files)

        ##############################
        ###### FILE VIEWER ##########
        self.tree_view = QTreeView()
        self.tree_view.setFont(self.window_font)
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(os.getcwd()))
        self.tree_view.setSelectionMode(QTreeView.SingleSelection)
        self.tree_view.setSelectionBehavior(QTreeView.SelectRows)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.tree_view_context_menu)
        self.tree_view.doubleClicked.connect(self.tree_view_clicked)
        self.tree_view.setIndentation(10)
        self.tree_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.tree_view.setHeaderHidden(True)
        self.tree_view.setColumnHidden(1, True)
        self.tree_view.setColumnHidden(2, True)
        self.tree_view.setColumnHidden(3, True)

        ##############################
        ###### SEARCH VIEW ##########
        self.search_frame = self.get_frame()
        self.search_frame.setMaximumWidth(self.window().width())
        self.search_frame.setMinimumWidth(200)

        search_layout = QVBoxLayout()
        search_layout.setAlignment(Qt.AlignTop)
        search_layout.setContentsMargins(0, 10, 0, 0)
        search_layout.setSpacing(0)

        search_input = QLineEdit()
        search_input.setPlaceholderText("Search")
        search_input.setFont(self.window_font)
        search_input.setAlignment(Qt.AlignTop)
        search_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #21252b;
                border-radius: 5px;
                border: 1px solid #D3D3D3;
                padding: 5px;
                color: #D3D3D3;
            }
            QLineEdit:hover {
                color: white;
            }
            """
        )

        self.search_git_checkbox = QCheckBox("Include .git")
        self.search_git_checkbox.setToolTip("If checked, will include .git folders in search.")
        self.search_git_checkbox.setFont(self.window_font)
        self.search_git_checkbox.setStyleSheet("color: white; margin-bottom: 10px;")

        self.search_worker = SearchWorker()
        self.search_worker.finished.connect(self.search_finished)

        search_input.textChanged.connect(
            lambda text: self.search_worker.update(
                text,
                self.model.rootDirectory().absolutePath(),
                self.search_git_checkbox.isChecked(),
            )
        )

        self.search_list_view = QListWidget()
        self.search_list_view.setFont(self.window_font)
        self.search_list_view.setStyleSheet(
            """
            QListWidget {
                background-color: #21252b;
                border-radius: 5px;
                border: 1px solid #D3D3D3;
                padding: 5px;
                color: #D3D3D3;
            }
            """
        )
        self.search_list_view.itemClicked.connect(self.search_list_view_clicked)

        search_layout.addWidget(self.search_git_checkbox)
        search_layout.addWidget(search_input)
        search_layout.addSpacerItem(QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Minimum))
        search_layout.addWidget(self.search_list_view)
        self.search_frame.setLayout(search_layout)

        tree_frame_layout.addWidget(self.tree_view)
        self.file_manager_frame.setLayout(tree_frame_layout)

        ##############################
        ###### TAB VIEW ##########
        self.tab_view = QTabWidget()
        self.tab_view.setFont(self.window_font)
        self.tab_view.setContentsMargins(0, 0, 0, 0)
        self.tab_view.setTabsClosable(True)
        self.tab_view.setMovable(True)
        self.tab_view.setDocumentMode(True)
        self.tab_view.setTabBar(SmallTabBar())
        self.tab_view.tabCloseRequested.connect(self.close_tab)
        self.tab_view.setStyleSheet(
            """
            /* Default appearance for all tabs */
            QTabBar::tab {
                background: #363a42;    /* background color for inactive tabs */
                color: white;           /* text color for inactive tabs */
                padding: 5px;
                margin: 2px;
            }
            /* Appearance for the selected (foreground) tab */
            QTabBar::tab:selected {
                background: #ffdf00;    /* background color for the active tab */
                color: black;        /* text color for the active tab */
            }
            /* Optionally, change the appearance when hovering over a tab */
            QTabBar::tab:hover {
                background: lightblue;
                color: black;
            }
        """
        )

        ##############################
        ###### SETUP WIDGETS ##########
        self.h_split.addWidget(self.file_manager_frame)
        self.h_split.addWidget(self.tab_view)

        body.addWidget(self.side_bar)
        body.addWidget(self.h_split)
        body_frame.setLayout(body)
        self.setCentralWidget(body_frame)

    def search_finished(self, items):
        self.search_list_view.clear()
        for i in items:
            self.search_list_view.addItem(i)

    def search_list_view_clicked(self, item: SearchItem):
        self.set_new_tab(Path(item.full_path))
        editor: CustomEditor = self.tab_view.currentWidget()
        editor.setCursorPosition(item.lineno, item.end)
        editor.setFocus()

    def close_tab(self, index, quiet: bool = False):
        if self.tab_view.tabText(index).startswith("*"):
            if not quiet:
                ret = question_box(
                    self,
                    "Changed File Alert!",
                    f"Close {Path(self.tab_view.tabText(index)).name} and Ignore Changes?",
                    buttons=QMessageBox.Yes | QMessageBox.No,
                    font=self.window_font,
                )
                if ret == QMessageBox.No:
                    return
        self.tab_view.removeTab(index)
        self.dupe_file.setEnabled(self.tab_view.count() > 0)
        self.delete_file.setEnabled(self.tab_view.count() > 0)

    def show_hide_tab(self, e, type_):
        if type_ == "folder-icon":
            if self.file_manager_frame not in self.h_split.children():
                self.h_split.replaceWidget(0, self.file_manager_frame)
                self.h_split.setSizes(self.last_h_split_sizes)
        elif type_ == "search-icon":
            if self.search_frame not in self.h_split.children():
                self.last_h_split_sizes = self.h_split.sizes()
                self.h_split.replaceWidget(0, self.search_frame)
                self.search_frame.setMaximumWidth(self.window().width())
                self.search_frame.setMinimumWidth(200)
        elif type_ == "search-local-icon":
            if self.search_frame not in self.h_split.children():
                self.last_h_split_sizes = self.h_split.sizes()
                self.h_split.replaceWidget(0, self.search_frame)
                self.search_frame.setMaximumWidth(self.window().width())
                self.search_frame.setMinimumWidth(200)
        if self.current_side_bar == type_:
            frame = self.h_split.children()[0]
            if frame.isHidden():
                frame.show()
            else:
                frame.hide()
        self.current_side_bar = type_

    def tree_view_context_menu(self, pos):
        pass

    def tree_view_clicked(self, index: QModelIndex):
        path = self.model.filePath(index)
        try:
            p = Path(path)
            self.set_new_tab(p)
        except Exception as e:
            warning_box(
                self, "Problem With Folder Choice", f"Unable to open {str(path)}: {str(e)}", font=self.window_font
            )

    def new_file(self, file_type: str):
        self.set_new_tab(None, is_new_file=True, file_type=file_type)

    @staticmethod
    def verify_duplicate_file_name(dupe_path: Path) -> Optional[Path]:
        dlg = DuplicateFileNameWin(dupe_path)
        dlg.setFont(QApplication.instance().font())
        dlg.exec_()
        if dlg.result():
            return dlg.path_result
        else:
            return None

    def duplicate_file(self):
        if not self.tab_view.count():
            return
        editor = self.tab_view.currentWidget()
        if not hasattr(editor, "file_path"):
            return
        p = editor.file_path
        dupe_path = self.next_new_file_path(file_type=p.suffix, stem=p.stem)
        dupe_path = Path(p.parent, dupe_path.name)
        dupe_path = self.verify_duplicate_file_name(dupe_path)
        if dupe_path is None:
            return
        dupe_path.write_text(normalize_line_endings(p.read_text(), editor.eolMode()))
        self.set_new_tab(path=dupe_path, is_new_file=False, file_type=p.suffix)

    def remove_file(self):
        if not self.tab_view.count() or self.tab_view.currentWidget() is None:
            return
        editor = self.tab_view.currentWidget()
        if not hasattr(editor, "file_path"):
            return
        p = editor.file_path
        ret = question_box(
            self,
            "File Deletion Warning!",
            f"Are You Sure You Want To Delete {str(p)}?\n\nThis operation cannot be undone!",
            buttons=QMessageBox.Yes | QMessageBox.No,
            font=self.window_font,
        )
        if ret == QMessageBox.No:
            return
        try:
            p.unlink(missing_ok=True)
            self.close_tab(self.tab_view.currentIndex(), quiet=True)
        except Exception as e:
            critical_box(self, "File I/O Error!", f"Unable To Delete File {str(p)}: ({str(e)})", font=self.window_font)

    def save_file(self):
        editor = self.tab_view.currentWidget()
        if editor is None or not hasattr(editor, "file_path") or editor.file_path is None:
            self.save_as()
            return
        try:
            editor.file_path.write_text(normalize_line_endings(editor.text(), editor.eolMode()))
        except Exception as e:
            self.statusBar().showMessage(f"Write Error: {e}", 4000)
            return
        # Remove the asterisk from the tab label if present.
        tab_text = self.tab_view.tabText(self.tab_view.currentIndex()).lstrip("*")
        self.tab_view.setTabText(self.tab_view.currentIndex(), tab_text)
        self.statusBar().showMessage(f"Saved {editor.file_path.name}", 4000)

    def save_as(self):
        editor = self.tab_view.currentWidget()
        if editor is None:
            return
        initial_name = str(editor.file_path) if editor.file_path else ""
        if editor.file_path and editor.file_path.suffix:
            initial_filter = f"*{editor.file_path.suffix.lower()}"
        else:
            initial_filter = ""
        file_path = QFileDialog.getSaveFileName(
            self,
            caption="Save As",
            directory=initial_name,
            filter="All Files (*);;PRS Rule Files (*.prs);;Text Files (*.txt);;Python Files (*.py);;C++ Code Files (*.cpp);;C++ Header Files (*.h)",
            initialFilter=initial_filter,
        )[0]
        if file_path == "":
            self.statusBar().showMessage("Save-As Operation Cancelled", 4000)
            return
        new_path = Path(file_path)
        try:
            new_path.write_text(normalize_line_endings(editor.text(), editor.eolMode()))
        except IOError as e:
            self.statusBar().showMessage(f"Write Error: {e}", 4000)
            return
        # Update the tab text to show only the file name and set its tooltip to the full path.
        self.tab_view.setTabText(self.tab_view.currentIndex(), new_path.name)
        self.tab_view.setTabToolTip(self.tab_view.currentIndex(), str(new_path))
        self.statusBar().showMessage(f"Saved {new_path.name}", 4000)
        editor.file_path = new_path

    def open_file(self, file_path: Optional[Path] = None):
        if isinstance(file_path, Path) and file_path.is_file():
            f = file_path
        else:
            ops = QFileDialog.Options()
            ops |= QFileDialog.DontUseNativeDialog
            new_file, _ = QFileDialog.getOpenFileName(
                self,
                caption="Pick A File",
                directory=str(self.model.rootDirectory().absolutePath()),
                filter="All Files (*);;PRS Rule Files (*.prs);;Text Files (*.txt);;Python Files (*.py);;C++ Code Files (*.cpp);;C++ Header Files (*.h)",
                options=ops,
            )
            if new_file == "":
                self.statusBar().showMessage("Open-File Operation Cancelled", 4000)
                return
            f = Path(new_file)
        self.set_new_tab(f)

    def open_folder(self):
        ops = QFileDialog.Options()
        ops |= QFileDialog.DontUseNativeDialog
        new_folder = QFileDialog.getExistingDirectory(self, "Pick A Folder", "", options=ops)
        if new_folder:
            self.model.setRootPath(new_folder)
            self.tree_view.setRootIndex(self.model.index(new_folder))
            self.statusBar().showMessage(f"Opened {new_folder}", 4000)
            # Update the window title to include the new folder path.
            self.setWindowTitle(f"EPIC Coder v{__version__} - {new_folder}")

    def set_folder(self, folder: Path):
        if folder.is_dir():
            folder_str = str(folder)
            self.model.setRootPath(folder_str)
            self.tree_view.setRootIndex(self.model.index(folder_str))
            self.statusBar().showMessage(f"Opened in {folder_str}", 4000)
            # Update the window title to include the folder path.
            self.setWindowTitle(f"EPIC Coder v{__version__} - {folder_str}")

    def copy(self):
        editor = self.tab_view.currentWidget()
        if hasattr(editor, "copy"):
            editor.copy()

    def paste(self):
        editor = self.tab_view.currentWidget()
        if hasattr(editor, "paste"):
            editor.paste()

    def resizeEvent(self, event: QResizeEvent):
        self.settings.setValue("main_window_width", self.size().width())
        self.settings.setValue("main_window_height", self.size().height())

    def closeEvent(self, event: QCloseEvent) -> None:
        unsaved_tabs = [i for i in range(self.tab_view.count()) if self.tab_view.tabText(i).startswith("*")]
        if unsaved_tabs and not self.force_close:
            ret = question_box(
                self,
                "Unsaved Changes",
                "Some files have unsaved changes. Do you really want to exit?",
                buttons=QMessageBox.Yes | QMessageBox.No,
                font=self.window_font,
            )
            if ret == QMessageBox.No:
                event.ignore()
                return
        event.accept()

    # Event filter to update the status bar when hovering over a tab.
    def eventFilter(self, obj, event):
        if obj == self.tab_view.tabBar():
            if event.type() == QEvent.MouseMove:
                pos = event.pos()
                index = self.tab_view.tabBar().tabAt(pos)
                if index != -1:
                    # Use the tooltip (full path) as the status message.
                    self.statusBar().showMessage(self.tab_view.tabToolTip(index))
                else:
                    self.statusBar().clearMessage()
            elif event.type() == QEvent.Leave:
                self.statusBar().clearMessage()
        return super(MainWindow, self).eventFilter(obj, event)
