import mmap
from pathlib import Path
from typing import Union

import charset_normalizer
from PyQt5.Qsci import QsciScintilla
import chardet
from charset_normalizer import from_bytes

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

def read_file_with_detection(file_path: Union[str, Path])->str:
    """
    Reads the file at 'file_path' using encoding detection with both chardet and charset_normalizer,
    and returns its content as a Unicode string (decoded text). This string can be used as UTF-8.

    Parameters:
        file_path (str): The path to the file.

    Returns:
        str: The file's content decoded using the detected encoding.
    """
    with open(file_path, 'rb') as f:
        raw = f.read()

    # Detect encoding using chardet.
    result_chardet = chardet.detect(raw)
    encoding_chardet = result_chardet.get('encoding')

    # Detect encoding using charset_normalizer.
    result_normalizer = from_bytes(raw)
    best_guess = result_normalizer.best()  # This returns a NamedTuple with attributes like encoding.
    encoding_normalizer = best_guess.encoding if best_guess else None

    # Decide which encoding to use.
    # Here we prefer chardet's result if available; otherwise, we use charset_normalizer's.
    encoding = encoding_chardet or encoding_normalizer or 'utf-8'

    try:
        text = raw.decode(encoding)
    except Exception as e:
        # If decoding fails, fallback to UTF-8 with replacement of invalid characters.
        text = raw.decode('utf-8', errors='replace')

    return text

def read_file_convert_to_utf8(full_path):
    """
    Reads the file at full_path, detects its encoding using chardet (with a fallback
    to charset_normalizer), decodes its contents, and returns the text as a Unicode string.
    """

    with open(full_path, mode="rb") as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as m:
            raw_data = m.read()

    # First, try to detect the encoding with chardet.
    chardet_result = chardet.detect(raw_data)
    encoding = chardet_result.get('encoding')
    confidence = chardet_result.get('confidence', 0)

    # If chardet doesn't return an encoding or has low confidence, use charset_normalizer.
    if not encoding or confidence < 0.5:
        cn_result = charset_normalizer.detect(raw_data)
        encoding = cn_result.get('encoding', 'utf-8')

    try:
        text = raw_data.decode(encoding)
    except (LookupError, UnicodeDecodeError):
        # If decoding fails using the detected encoding, use charset_normalizer directly.
        results = charset_normalizer.from_bytes(raw_data)
        best_guess = results.best()
        if best_guess is not None:
            text = best_guess.to_string()
        else:
            # Fallback: decode as UTF-8 with error replacement.
            text = raw_data.decode('utf-8', errors='replace')
    return text

