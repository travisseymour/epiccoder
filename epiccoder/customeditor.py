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

import builtins
import sys
from pathlib import Path
from typing import Callable, Optional

import keyword
import pkgutil

from PyQt5.Qsci import QsciScintilla
from PyQt5.Qsci import QsciLexerPython
from PyQt5.Qsci import QsciLexerCPP
from PyQt5.Qsci import QsciAPIs

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont, QColor, QKeyEvent
from PyQt5.QtWidgets import QApplication

from epiccoder.darkmode import is_dark_mode
from epiccoder.lexer import PPSCustomLexer, TextCustomLexer
from epiccoder.themes import theme


class CustomEditor(QsciScintilla):
    """
    CustomEditor is a text editor widget built on QsciScintilla that supports syntax highlighting,
    auto-completion, and change detection for a variety of file types.
    """

    def __init__(
        self,
        parent=None,
        file_path: Optional[Path] = None,
        star_func: Optional[Callable] = None,
    ):
        super(CustomEditor, self).__init__(parent)

        assert isinstance(file_path, Path), ValueError("file_path must be provided and be a pathlib.Path object")
        assert isinstance(star_func, Callable), ValueError("star_func must be provided and be a callable")

        self.file_path = file_path
        self.star_func = star_func

        # encoding
        self.setUtf8(True)
        # Font
        self.window_font = QApplication.instance().font()
        self.setFont(self.window_font)

        # brace matching
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # indentation
        self.setIndentationGuides(True)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)

        # autocomplete
        self.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AcusNever)

        # caret
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        if is_dark_mode():
            self.setCaretForegroundColor(QColor("#00FFFF"))  # Cyan for dark mode
            self.setCaretLineBackgroundColor(QColor("#2E3B45"))  # Soft Dark Blue for dark mode
        else:
            self.setCaretForegroundColor(QColor("#000000"))  # Black for light mode
            self.setCaretLineBackgroundColor(QColor("#FFFACD"))  # Pale Yellow for light mode

        # EOL
        if sys.platform.startswith("win"):
            self.setEolMode(QsciScintilla.EolWindows)  # \r\n (Windows)
        else:
            self.setEolMode(QsciScintilla.EolUnix)  # \n (Default for Linux & other OS)

        self.setEolVisibility(False)

        # lexer for syntax highlighting

        theme_name = QSettings().value("theme", "Monokai")
        self.default_text_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["foreground"])
        self.default_bg_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["background"])

        if self.file_path.suffix == ".py":
            self.pylexer = QsciLexerPython(self)

            self.pylexer.setDefaultColor(self.default_text_color)
            self.pylexer.setDefaultPaper(self.default_bg_color)
            self.pylexer.setDefaultFont(QApplication.instance().font())

            self.pylexer.setColor(self.default_text_color, QsciLexerPython.Default)  # Default text color

            if is_dark_mode():
                self.pylexer.setColor(QColor("#57C7FF"), QsciLexerPython.Number)  # Sky Blue
                self.pylexer.setColor(QColor("#FF9F1C"), QsciLexerPython.Keyword)  # Bright Orange
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.DoubleQuotedString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.SingleQuotedString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.TripleDoubleQuotedString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.TripleSingleQuotedString)  # Vibrant Lime Green

                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.DoubleQuotedFString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerPython.SingleQuotedFString)  # Vibrant Lime Green
                self.pylexer.setColor(
                    QColor("#A3E635"), QsciLexerPython.TripleDoubleQuotedFString
                )  # Vibrant Lime Green
                self.pylexer.setColor(
                    QColor("#A3E635"), QsciLexerPython.TripleSingleQuotedFString
                )  # Vibrant Lime Green

                self.pylexer.setColor(QColor("#FFB86C"), QsciLexerPython.FunctionMethodName)  # Warm Golden Yellow
                self.pylexer.setColor(QColor("#9E9E9E"), QsciLexerPython.Comment)  # Medium Gray
                self.pylexer.setColor(QColor("#9E9E9E"), QsciLexerPython.CommentBlock)  # Medium Gray
                self.pylexer.setColor(QColor("#BD93F9"), QsciLexerPython.Identifier)  # Soft Lavender
            else:
                self.pylexer.setColor(QColor("#005BBB"), QsciLexerPython.Number)  # Deep Blue
                self.pylexer.setColor(QColor("#D75F00"), QsciLexerPython.Keyword)  # Burnt Orange
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.DoubleQuotedString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.SingleQuotedString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.TripleDoubleQuotedString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.TripleSingleQuotedString)  # Dark Green

                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.DoubleQuotedFString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.SingleQuotedFString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.TripleDoubleQuotedFString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerPython.TripleSingleQuotedFString)  # Dark Green

                self.pylexer.setColor(QColor("#BB5500"), QsciLexerPython.FunctionMethodName)  # Rich Amber
                self.pylexer.setColor(QColor("#5F5F5F"), QsciLexerPython.Comment)  # Dark Gray
                self.pylexer.setColor(QColor("#5F5F5F"), QsciLexerPython.CommentBlock)  # Dark Gray
                self.pylexer.setColor(QColor("#7D2181"), QsciLexerPython.Identifier)  # Deep Purple

        elif self.file_path.suffix in (".h", ".c", ".cpp", ".hpp"):
            self.pylexer = QsciLexerCPP(self)

            self.pylexer.setDefaultColor(self.default_text_color)
            self.pylexer.setDefaultPaper(self.default_bg_color)
            self.pylexer.setDefaultFont(QApplication.instance().font())

            if is_dark_mode():
                self.pylexer.setColor(QColor("#57C7FF"), QsciLexerCPP.Number)  # Sky Blue
                self.pylexer.setColor(QColor("#FF9F1C"), QsciLexerCPP.Keyword)  # Bright Orange
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerCPP.DoubleQuotedString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#A3E635"), QsciLexerCPP.SingleQuotedString)  # Vibrant Lime Green
                self.pylexer.setColor(QColor("#57C7FF"), QsciLexerCPP.Operator)  # Sky Blue
                self.pylexer.setColor(QColor("#9E9E9E"), QsciLexerCPP.Comment)  # Medium Gray
                self.pylexer.setColor(QColor("#9E9E9E"), QsciLexerCPP.CommentDoc)  # Medium Gray
                self.pylexer.setColor(QColor("#BD93F9"), QsciLexerCPP.Identifier)  # Soft Lavender
                self.pylexer.setColor(QColor("#0FB9B1"), QsciLexerCPP.PreProcessor)  # Teal
                self.pylexer.setColor(QColor("#FF5555"), QsciLexerCPP.GlobalClass)  # Vivid Red (for class names)
            else:
                self.pylexer.setColor(QColor("#005BBB"), QsciLexerCPP.Number)  # Deep Blue
                self.pylexer.setColor(QColor("#D75F00"), QsciLexerCPP.Keyword)  # Burnt Orange
                self.pylexer.setColor(QColor("#007500"), QsciLexerCPP.DoubleQuotedString)  # Dark Green
                self.pylexer.setColor(QColor("#007500"), QsciLexerCPP.SingleQuotedString)  # Dark Green
                self.pylexer.setColor(QColor("#005BBB"), QsciLexerCPP.Operator)  # Deep Blue
                self.pylexer.setColor(QColor("#5F5F5F"), QsciLexerCPP.Comment)  # Dark Gray
                self.pylexer.setColor(QColor("#5F5F5F"), QsciLexerCPP.CommentDoc)  # Dark Gray
                self.pylexer.setColor(QColor("#7D2181"), QsciLexerCPP.Identifier)  # Deep Purple
                self.pylexer.setColor(QColor("#004488"), QsciLexerCPP.PreProcessor)  # Dark Cyan
                self.pylexer.setColor(QColor("#D00000"), QsciLexerCPP.GlobalClass)  # Bold Red (for class names)

        elif self.file_path.suffix == ".prs":
            self.pylexer = PPSCustomLexer(self)

        else:
            self.pylexer = TextCustomLexer(self)

        self.configure_lexer(self.pylexer, self.window_font)

        # Api (you can add autocompletion using this)
        self.api = QsciAPIs(self.pylexer)
        # adding builtin functions and keywords
        for key in keyword.kwlist + dir(builtins):
            self.api.add(key)

        for (
            _,
            name,
            _,
        ) in pkgutil.iter_modules():  # adding all modules names from current interpreter
            self.api.add(name)

        self.api.prepare()

        self.setLexer(self.pylexer)

        # line numbers
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setMarginWidth(0, "000")
        self.setMarginsForegroundColor(QColor("#ff888888"))
        self.setMarginsBackgroundColor(QColor("#282c34"))
        self.setMarginsFont(self.window_font)

        # key press
        # self.keyPressEvent = self.handle_editor_press

        # text change indicator
        self.got_first_change_event = False
        self.textChanged.connect(self.onTextChanged)

    def configure_lexer(self, lexer, font: QFont):
        lexer.setDefaultColor(self.default_text_color)
        lexer.setDefaultPaper(self.default_bg_color)
        lexer.setDefaultFont(font)
        for i in range(50):
            lexer.setFont(font, i)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_Space:
            self.autoCompleteFromAll()
        else:
            return super().keyPressEvent(e)

    def onTextChanged(self):
        # Ignore First Change Event
        if not self.got_first_change_event:
            self.got_first_change_event = True
        # Signal Next Event If Change Is Novel
        else:
            self.star_func(self.file_path)
