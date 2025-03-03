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

import re
from typing import Optional

from PyQt5.Qsci import QsciLexerCustom, QsciScintilla
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtWidgets import QApplication

from epiccoder.darkmode import is_dark_mode
from epiccoder.themes import theme


class TextCustomLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(TextCustomLexer, self).__init__(parent)
        theme_name = QSettings().value("theme", "Monokai")
        self.default_text_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["foreground"])
        self.default_bg_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["background"])

        # Default Settings
        self.setDefaultColor(self.default_text_color)
        self.setDefaultPaper(self.default_bg_color)
        self.setDefaultFont(QApplication.instance().font())

        self.DEFAULT = 0
        self.NUMBER = 1

        # colors
        # bright_green = QColor("#a6e22b")
        # red = QColor("#f9245e")
        # teal = QColor("#c678dd")
        # brown = QColor("#736643")
        # light_brown = QColor("#b39e69")
        # yellow = QColor("#e7db74")
        # orange = QColor("#fc9221")
        # hot_pink = QColor("#ff00cc")
        # light_blue = QColor("#6495ed")

        # styles
        self.setColor(QColor(self.default_text_color), self.DEFAULT)
        self.setColor(QColor("#ac7db8"), self.NUMBER)  # purple

        # paper color
        # self.setPaper(self.default_bg_color, self.DEFAULT)
        # self.setPaper(self.default_bg_color, self.NUMBER)

        self.token_pattern = re.compile(r"[*]|\/\/+|\s+|\w+|\W|\s")

    def description(self, style: int) -> str:
        if style == self.DEFAULT:
            return "DEFAULT"
        elif style == self.NUMBER:
            return "NUMBER"
        else:
            return ""

    def get_tokens(self, text) -> list[tuple[str, int]]:
        p = self.token_pattern

        return [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]
        token_list = [(s.lower(), i) if isinstance(s, str) else (s, i) for s, i in self.get_tokens(text)]

        def next_tok(skip: int = None):
            if len(token_list) > 0:
                if skip is not None and skip != 0:
                    for _ in range(skip - 1):
                        if len(token_list) > 0:
                            token_list.pop(0)
                return token_list.pop(0)
            else:
                return None

        while True:
            current_token = next_tok()

            if current_token is None:
                break

            tok: str = current_token[0]
            tok_len: int = current_token[1]

            if tok.isnumeric():
                self.setStyling(tok_len, self.NUMBER)
            else:
                self.setStyling(tok_len, self.DEFAULT)


class PPSCustomLexer(QsciLexerCustom):
    def __init__(self, parent):
        super(PPSCustomLexer, self).__init__(parent)

        theme_name = QSettings().value("theme", "Monokai")
        self.default_text_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["foreground"])
        self.default_bg_color = QColor(theme[theme_name]["dark" if is_dark_mode() else "light"]["background"])

        self.last_tok: Optional[str] = None

        # Default Settings
        self.setDefaultColor(self.default_text_color)
        self.setDefaultPaper(self.default_bg_color)
        self.setDefaultFont(QApplication.instance().font())

        # Keywords

        self.RULE_SECTIONS = ["if", "then"]

        self.COMPARISONS = [
            "not",
            "equal",
            "greater",
            "least",
            "different",
            "less-than",
            "less_than",
            "greater-than",
            "greater_than",
            "equal-to",
            "equal_to",
        ]
        self.DIRECTIVES = [
            "if-only-one",
            "if_only_one",
            "use-only-one",
            "use_only_one",
            "randomly-choose-one",
            "randomly_choose_one",
            "unique",
        ]
        self.ARCHITECTURES = [
            "goal",
            "step",
            "tag",
            "visual",
            "auditory",
            "tactile",
            "more",
            "initial-memory-contents",
            "initial_memory_contents",
            "parameters",
            "named-location",
            "named_location",
            "motor",
            "ocular",
            "manual",
            "vocal",
        ]
        self.KEYWORDS = [
            "add",
            "adddb",
            "del",
            "delete",
            "log",
            "define",
            "set-mode",
            "set_mode",
            "send-to-motor",
            "send_to_motor",
            "delay-countdown",
            "delay_countdown",
            "increment",
            "send-to-temporal",
            "send_to_temporal",
        ]

        # color per style
        self.DEFAULT = 0

        self.RULE_SECTION = 1
        self.COMPARISON = 2
        self.DIRECTIVE = 3
        self.ARCHITECTURE = 4

        self.COMMENT = 5
        self.NUMBER = 6

        self.RULE_NAME = 7
        self.VARIABLE = 8

        self.KEYWORD = 9
        self.PARENS = 10

        # styles
        self.setColor(QColor(self.default_text_color), self.DEFAULT)
        self.setColor(QColor(self.default_text_color), self.PARENS)
        if is_dark_mode():
            self.setColor(QColor("#e7db74"), self.RULE_SECTION)  # Soft Gold
            self.setColor(QColor("#a6e22b"), self.COMPARISON)  # Bright Lime Green
            self.setColor(QColor("#f9245e"), self.DIRECTIVE)  # Vivid Pinkish-Red
            self.setColor(QColor("#c678dd"), self.ARCHITECTURE)  # Soft Purple
            self.setColor(QColor("#736643"), self.COMMENT)  # Muted Brownish-Olive
            self.setColor(QColor("#ac7db8"), self.NUMBER)  # Dusty Lavender
            self.setColor(QColor("#e7db74"), self.RULE_NAME)  # Soft Gold (Same as RULE_SECTION)
            self.setColor(QColor("#ff00cc"), self.VARIABLE)  # Neon Pink
            self.setColor(QColor("#6495ed"), self.KEYWORD)  # Cornflower Blue

        else:
            self.setColor(QColor("#755f00"), self.RULE_SECTION)  # Darker Gold
            self.setColor(QColor("#22863a"), self.COMPARISON)  # Dark Green
            self.setColor(QColor("#d70040"), self.DIRECTIVE)  # Crimson Red
            self.setColor(QColor("#b847e1"), self.ARCHITECTURE)  # Soft Purple
            self.setColor(QColor("#8b7765"), self.COMMENT)  # Warm Brownish-Gray
            self.setColor(QColor("#9842a0"), self.NUMBER)  # Vibrant Magenta
            self.setColor(QColor("#755f00"), self.RULE_NAME)  # Darker Gold
            self.setColor(QColor("#cc0077"), self.VARIABLE)  # Hot Pink
            self.setColor(QColor("#005ab5"), self.KEYWORD)  # Deep Blue

        # font
        normal_font: QFont = QApplication.instance().font()
        bold_font: QFont = QApplication.instance().font()
        bold_font.setBold(True)
        self.setFont(normal_font, self.DEFAULT)
        self.setFont(normal_font, self.PARENS)
        self.setFont(bold_font, self.RULE_SECTION)
        self.setFont(bold_font, self.COMPARISON)
        self.setFont(bold_font, self.DIRECTIVE)
        self.setFont(bold_font, self.ARCHITECTURE)
        self.setFont(normal_font, self.COMMENT)
        self.setFont(normal_font, self.NUMBER)
        self.setFont(bold_font, self.RULE_NAME)
        self.setFont(normal_font, self.VARIABLE)
        self.setFont(bold_font, self.KEYWORD)

        self.token_pattern = re.compile(r"[*]|\/\/+|\s+|\w+|\W|\s")

    def language(self) -> str:
        return "PPS_Rule_Lexer"

    def description(self, style: int) -> str:
        if style == self.DEFAULT:
            return "DEFAULT"
        elif style == self.RULE_SECTION:
            return "RULE_SECTION"
        elif style == self.COMPARISON:
            return "COMPARISON"
        elif style == self.DIRECTIVE:
            return "DIRECTIVE"
        elif style == self.ARCHITECTURE:
            return "ARCHITECTURE"
        elif style == self.COMMENT:
            return "COMMENT"
        elif style == self.NUMBER:
            return "NUMBER"
        elif style == self.RULE_NAME:
            return "RULE_NAME"
        elif style == self.VARIABLE:
            return "VARIABLE"
        elif style == self.KEYWORD:
            return "KEYWORD"
        elif style == self.PARENS:
            return "PARENS"
        else:
            return ""

    def get_tokens(self, text) -> list[str, int]:
        # 3. Tokenize the text
        # ---------------------

        p = self.token_pattern

        # 'token_list' is a list of tuples: (token_name, token_len), ex: '(class, 5)'
        return [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)
        editor: QsciScintilla = self.parent()

        text = editor.text()[start:end]
        token_list = [(s.lower(), i) if isinstance(s, str) else (s, i) for s, i in self.get_tokens(text)]

        string_flag = False

        if start > 0:
            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style_nr == self.COMMENT:
                string_flag = False

        def next_tok(skip: int = None):
            if len(token_list) > 0:
                if skip is not None and skip != 0:
                    for _ in range(skip - 1):
                        if len(token_list) > 0:
                            token_list.pop(0)
                return token_list.pop(0)
            else:
                return None

        def peek_tok(n=0):
            try:
                return token_list[n]
            except IndexError:
                return [""]

        def skip_space_peek(skip=None):
            i = 0
            tok = " "
            if skip is not None:
                i = skip
            while tok[0].isspace():
                tok = peek_tok(i)
                i += 1
            return tok, i

        last_token: Optional[str] = None
        current_token: Optional[str] = None

        while True:
            if current_token:
                last_token = current_token
            current_token = next_tok()

            if current_token is None:
                break

            tok: str = current_token[0]
            tok_len: int = current_token[1]

            if string_flag:
                self.setStyling(tok_len, self.COMMENT)
                if tok[-1] in ("\n", "\r") or tok[0] in ("\n", "\r"):
                    string_flag = False
                continue

            elif tok in self.RULE_SECTIONS:
                self.setStyling(tok_len, self.RULE_SECTION)
            elif tok in self.COMPARISONS:
                self.setStyling(tok_len, self.COMPARISON)
            elif tok in self.DIRECTIVES:
                self.setStyling(tok_len, self.DIRECTIVE)
            elif tok in self.ARCHITECTURES:
                self.setStyling(tok_len, self.ARCHITECTURE)
            elif tok in self.KEYWORDS:
                self.setStyling(tok_len, self.KEYWORD)
            elif tok.isnumeric():
                self.setStyling(tok_len, self.NUMBER)
            elif tok in ("(", ")"):
                self.setStyling(tok_len, self.PARENS)
            elif tok.startswith(";") or tok.startswith("//"):
                self.setStyling(tok_len, self.COMMENT)
                string_flag = True
            else:
                peek = peek_tok()

                if len(tok) > 2 and last_token and last_token[0] == "(" and peek and peek[0][0] in ("\n", "\r"):
                    self.setStyling(tok_len, self.RULE_NAME)
                elif tok == "?" and last_token and last_token[0] in ("?", " ", "("):
                    self.setStyling(tok_len, self.VARIABLE)
                elif "?" not in tok and last_token and last_token[0] == "?":
                    self.setStyling(tok_len, self.VARIABLE)
                else:
                    self.setStyling(tok_len, self.DEFAULT)
