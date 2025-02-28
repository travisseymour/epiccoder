from PyQt5.Qsci import QsciScintilla


def normalize_line_endings(text: str, eol_mode: int) -> str:
    """Converts all line endings in the given text to match the specified EOL mode."""

    # Normalize all line endings to Unix (`\n`) first
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Convert to the desired EOL mode
    if eol_mode == QsciScintilla.EolWindows:
        return text.replace("\n", "\r\n")  # Convert all to Windows (`\r\n`)
    elif eol_mode == QsciScintilla.EolMac:
        return text.replace("\n", "\r")  # Convert all to old macOS (`\r`)
    # Default: Unix (`\n`)
    return text
