# EPICcoder

Copyright © 2022-2025 Travis L. Seymour, PhD

---

![Snapshot of EPICcoder Interface](https://cogmodlab.sites.ucsc.edu/files/2022/08/epiccoder_ui_interface_snapshot-1024x925.png)

---

EPICcoder is a _**<font color="orange">minimal</font>**_ programmer's text editor created for use with the EPIC and EPICpy simulation environments (see <https://github.com/travisseymour/EPICpy>). It features syntax highlighting for the following file formats:  

* PPS Production Rule Files (*.prs)  
* Text Files (*.txt)  
* Python Code Files (*.py)
* C Code Files (*.c)  
* C++ Code Files (*.cpp)
* C++ Header Files (*.h)

EPICcoder requires Python 3.9 or higher.

**NOTE**: This code is based heavily on the awesome video tutorial (https://www.youtube.com/watch?v=ihyDi1aPNBw) by FUSEN from 2022 (current sources hosted here: https://github.com/Fus3n/pyqt-code-editor-yt), which in turn borrowed heavily from the tutorials at <https://qscintilla.com/>.

Note: This project's code is released under the **GPLv3** license to comply with the requirements of PyQT5 library. I hope to convert this project to PySide6 shortly so that a less restrictive license can be used instead. If any files used here are missing the proper attribution, please let me know.
 The GPLv3 licence has been included along with this program. If not, see <http://www.gnu.org/licenses/>.

---

## Installation Overview

To install EPICcoder, I suggest you use `uv` (https://docs.astral.sh/uv/) on MacOS, Windows, and Linux. Although you can use a very similar set of commands to install EPICcoder with `PipX` (https://pipx.pypa.io/latest/), I will describe how to do so using `uv` below.

## Install `uv`

You should install `uv` using the instructions at https://docs.astral.sh/uv/getting-started/installation/. However, the commands are simple and have been reproduced here for the most common use cases (though many other approaches are described for each platform on the `uv` installation webpage):

### MacOS & Linux

Use curl to download the script and execute it with sh:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have curl, you can use wget:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

### Windows

Use irm to download the script and execute it with iex:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Install EPICcoder

```bash
uv tool install git+https://github.com/travisseymour/EPICcoder.git
```

Hopefully, that worked without a problem! Otherwise, see below for ways to troubleshoot the most common issues:

🚩 If `uv` tool install complains about the `git` tool being missing, then you must [**install git**](https://git-scm.com/downloads) and then retry the command above.

🚩 If `uv` tool install complains that no appropriate version of Python is installed on your system, then you can install such a version using this command:

`uv python install [VERSION]`

e.g.:

```bash
uv python install 3.10
```

🚩 If `uv` still says it cannot find Python, then find a version yourself like this:

```bash
uv python list
```

You should see all the installed python versions and their respective file paths. Copy one of the paths that match the target Python version and re-run the EPICcoder installation using this form `uv tool install git+https://github.com/travisseymour/EPICcoder.git --ptyhon [THE COPIED PYTHON PATH]`.

For example:

- It might look like this on Linux:
  - ```bash
    uv tool install git+https://github.com/travisseymour/EPICcoder.git --python .local/share/uv/python/cpython-3.10.14-linux-x86_64-gnu/bin/python3
    ```
- It might look like this on MacOS:
  - ```bash
    uv tool install git+https://github.com/travisseymour/EPICcoder.git --python .local/share/uv/python/cpython-3.10.2-macos-x86_64-none/bin/python3
    ```
- It might look like this on Windows:
  - ```bash
    uv tool install git+https://github.com/travisseymour/EPICcoder.git --python AppData\Roaming\uv\python\cpython-3.11.9-windows-x86_64-none\python.exe
    ```

## Run EPICcoder

Start EPICcoder by opening your operating system's terminal application and type this command:

```bash
epiccoder
```

---

## Upgrade EPICcoder

Upgrade EPICcoder by opening your operating system's terminal application and type this command:

```bash
uv tool upgrade epiccoder
```

## Uninstall EPICcoder

Uninstall EPICcoder by opening your operating system's terminal application and type this command:

```bash
uv tool uninstall epiccoder
```