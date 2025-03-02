import mimetypes
import os
from pathlib import Path
from typing import Union, Sequence, Iterator


def is_binary_file(path)->bool:
    """Check if file is binary"""
    try:
        with open(path, "rb") as f:
            return b"\0" in f.read(1024)
    except FileNotFoundError:
        return True

# def is_binary_file(file_path: Union[str, Path], num_bytes: int = 1024) -> bool:
#     """
#     Detects if a file is binary or text.
#     Uses a combination of MIME type detection and a heuristic check.
#
#     - Reads the first `num_bytes` of the file.
#     - If there are null bytes (`b'\x00'`), it's likely binary.
#     - Falls back to `mimetypes` for additional checking.
#     """
#
#     filepath = str(file_path)
#
#     # Try MIME type detection first
#     mime_type, encoding = mimetypes.guess_type(filepath)
#
#     # If the MIME type starts with "text/", it's likely a text file
#     if mime_type and mime_type.startswith("text/"):
#         return False  # Not binary
#
#     # Read a small part of the file and check for binary indicators
#     try:
#         with open(filepath, "rb") as f:
#             chunk = f.read(num_bytes)
#             if b"\x00" in chunk:  # Null byte is a strong binary indicator
#                 return True
#             elif not chunk:  # Empty file? Assume text
#                 return False
#     except Exception as e:
#         print(f"Error reading file {filepath}: {e}")
#         return False  # Assume text if we can't read the file
#
#     return False  # Default to text


from pathlib import Path
from collections import defaultdict
from typing import List, Tuple


def group_files_by_folder(paths: List[Path]) -> List[Tuple[Path, Tuple[str, ...]]]:
    """
    Groups a list of file paths by their parent directories.

    Args:
        paths (List[Path]): A list of Path objects, each representing a file.

    Returns:
        List[Tuple[Path, Tuple[str, ...]]]: A list of tuples where each tuple contains:
            - A Path object representing the parent directory.
            - A tuple of strings, each being a file name found in that directory.

    Example:
        >>> data = [
        ...     Path("Pictures/one.jpg"),
        ...     Path("Pictures/two.jpg"),
        ...     Path("Pictures/three.jpg"),
        ...     Path("tmpwork/work1.txt"),
        ...     Path("tmpwork/work2.txt"),
        ...     Path("Videos/temp/one.mov"),
        ... ]
        >>> group_files_by_folder(data)
        [(Path('Pictures'), ('one.jpg', 'two.jpg', 'three.jpg')),
         (Path('tmpwork'), ('work1.txt', 'work2.txt')),
         (Path('Videos/temp'), ('one.mov',))]
    """
    folder_map = defaultdict(list)

    for path in paths:
        folder_map[path.parent].append(path.name)

    return [(folder, tuple(files)) for folder, files in folder_map.items()]


def walkdir(path: str, include_hidden: bool = False, exclude_dirs: Sequence = (), exclude_files: Sequence = ()) -> Iterator[Tuple[str, list, list]]:
    """
    Recursively walks through a directory, yielding root paths, directories, and files while allowing
    optional filtering of hidden files and directories.

    Args:
        path (str): The root directory to start walking.
        include_hidden (bool, optional): Whether to include hidden files and directories (starting with '.').
                                         Defaults to False.
        exclude_dirs (Sequence, optional): A sequence of directory names to exclude from traversal.
                                           Defaults to an empty tuple.
        exclude_files (Sequence, optional): A sequence of file extensions (including the dot, e.g., '.txt')
                                            to exclude. Defaults to an empty tuple.

    Yields:
        Iterator[Tuple[str, list, list]]: Each iteration yields a tuple containing:
            - The current root directory as a string.
            - A list of directories in the current root (filtered based on `include_hidden` and `exclude_dirs`).
            - A list of files in the current root (filtered based on `include_hidden` and `exclude_files`).

    Example:
        >>> for root, dirs, files in walkdir("my_folder", exclude_dirs=["venv"], exclude_files=[".log"]):
        ...     print(root, dirs, files)
    """
    for (
        root,
        dirs,
        files,
    ) in os.walk(path, topdown=True):
        # filtering
        if include_hidden:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            files[:] = [f for f in files if Path(f).suffix not in exclude_files]
        else:
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith(".")]
            files[:] = [f for f in files if Path(f).suffix not in exclude_files and not f.startswith(".")]
        yield root, dirs, files
