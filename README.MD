EPICcoder
---

EPICcoder is a _**<font color="orange">minimal</font>**_ programmer's text editor created for use with the EPIC, EPICpy and pyEPIC simulation environments (see <https://cogmodlab.ucsc.edu/2022/03/14/epic/>). It features syntax highlighting for the following file formats:  

* PPS Production Rule Files (*.prs)  
* Text Files (*.txt)  
* Python Code Files (*.py)
* C Code Files (*.c)  
* C++ Code Files (*.cpp)
* C++ Header Files (*.h)

**NOTE**: This code is based heavily on the sample code1 and video tutorial2 by, FUSEN3 which itself borrows heavily from the tutorials at <https://qscintilla.com/>.
The EPICcoder binaries can be found here at <https://cogmodlab.ucsc.edu/2022/10/23/epiccoder/>.
1. <https://github.com/Fus3n/pyqt-code-editor-yt>
2. <https://www.youtube.com/watch?v=ihyDi1aPNBw>
3. <https://github.com/Fus3n>

Note: This project's code is released under the **GPLv3** license to comply with the requirements of PyQT5 library. If QScintilla is ever added to PySide2, a less restrictive license will be used instead. If any files used here are missing the proper attribution, please let me know.
 Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

---

## Binary File Creation

Binaries are available for Linux, MacOS, and Windows at <https://cogmodlab.sites.ucsc.edu/2022/08/25/epiccoder/>.
To create these binaries, the entire project is managed by the pro version of the F-Man Build System (fbs) (<https://build-system.fman.io/>). You can recreate these binaries using the build commands provided below.

HOWEVER,
Note that with the free/opensource version of fbs (<https://github.com/mherrmann/fbs>) (installable with `pip install fbs`), you will be limited to Python 3.6. In order to use fbs with later versions of Python, you will need to purchase the pro version (<https://build-system.fman.io/>) (which I highly recommend if you are producing multi-platform binaries of Python projects).

### Run
`fbs run`

### Build

`fbs clean && fbs freeze`

### Run Frozen

#### Linux
`./target/app_name/app_name`

#### Macos

`./target/app_name/app_name.app/contents/MacOS/app_name`

#### Windows

`/target/app_name/app_name.exe`

### Create Installer Package

`fbs installer`

### Notes 

- In order to build for a particular operating system, you must run the fbs commands from that operating system. For example, you cannot build a package for MacOS from Linux.

- Prior to running `fbs installer`, you may be asked to install the FPM tool (<https://fpm.readthedocs.io/en/latest/installation.html>). On Linux this requires `sudo gem install fpm`. For more information on using fbs to package your PyQT applications, see here: <https://www.pythonguis.com/tutorials/packaging-pyqt5-apps-fbs/>.