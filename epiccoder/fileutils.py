import mimetypes
from pathlib import Path
from typing import Union


def is_binary_file(file_path: Union[str, Path], num_bytes: int = 1024) -> bool:
    """
    Detects if a file is binary or text.
    Uses a combination of MIME type detection and a heuristic check.

    - Reads the first `num_bytes` of the file.
    - If there are null bytes (`b'\x00'`), it's likely binary.
    - Falls back to `mimetypes` for additional checking.
    """

    filepath = str(file_path)

    # Try MIME type detection first
    mime_type, encoding = mimetypes.guess_type(filepath)

    # If the MIME type starts with "text/", it's likely a text file
    if mime_type and mime_type.startswith("text/"):
        return False  # Not binary

    # Read a small part of the file and check for binary indicators
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(num_bytes)
            if b"\x00" in chunk:  # Null byte is a strong binary indicator
                return True
            elif not chunk:  # Empty file? Assume text
                return False
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return False  # Assume text if we can't read the file

    return False  # Default to text
