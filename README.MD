EPICcoder

![Snapshot of EPICcoder Interface](https://cogmodlab.sites.ucsc.edu/files/2022/08/epiccoder_ui_interface_snapshot-1024x925.png)

---

EPICcoder is a _**<font color="orange">minimal</font>**_ programmer's text editor created for use with the EPIC, EPICpy and pyEPIC simulation environments (see <https://cogmodlab.ucsc.edu/2022/03/14/epic/>). It features syntax highlighting for the following file formats:  

* PPS Production Rule Files (*.prs)  
* Text Files (*.txt)  
* Python Code Files (*.py)
* C Code Files (*.c)  
* C++ Code Files (*.cpp)
* C++ Header Files (*.h)

**NOTE**: This code is based heavily on the sample code1 and video tutorial2 by, FUSEN3 which itself borrows heavily from the tutorials at <https://qscintilla.com/>.
The EPICcoder binaries can be found here at <https://cogmodlab.sites.ucsc.edu/2022/08/25/epiccoder/>.
1. <https://github.com/Fus3n/pyqt-code-editor-yt>
2. <https://www.youtube.com/watch?v=ihyDi1aPNBw>
3. <https://github.com/Fus3n>

Note: This project's code is released under the **GPLv3** license to comply with the requirements of PyQT5 library. If QScintilla is ever added to PySide2, a less restrictive license will be used instead. If any files used here are missing the proper attribution, please let me know.
 Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

---

## Binary File Creation

Binaries are available for Linux, MacOS, and Windows at <https://cogmodlab.sites.ucsc.edu/2022/08/25/epiccoder/>.
To create these binaries, the entire project is managed by the pro version of the F-Man Build System (fbs) (<https://build-system.fman.io/>). Also see <https://www.pythonguis.com/tutorials/packaging-pyqt5-apps-fbs/>.

