# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutui.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_aboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName("aboutDialog")
        aboutDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        aboutDialog.resize(680, 640)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(14)
        aboutDialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(aboutDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.labelEPICicon = QtWidgets.QLabel(aboutDialog)
        self.labelEPICicon.setMinimumSize(QtCore.QSize(180, 180))
        self.labelEPICicon.setBaseSize(QtCore.QSize(180, 180))
        self.labelEPICicon.setText("")
        self.labelEPICicon.setScaledContents(True)
        self.labelEPICicon.setObjectName("labelEPICicon")
        self.horizontalLayout.addWidget(self.labelEPICicon)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(aboutDialog)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.pushButtonClose = QtWidgets.QPushButton(aboutDialog)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.pushButtonClose.setFont(font)
        self.pushButtonClose.setDefault(True)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.verticalLayout.addWidget(self.pushButtonClose)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(aboutDialog)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        _translate = QtCore.QCoreApplication.translate
        aboutDialog.setWindowTitle(_translate("aboutDialog", "About EPICpy"))
        self.textBrowser.setHtml(
            _translate(
                "aboutDialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'Consolas'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
                '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'JetBrains Mono\',\'monospace\'; font-size:28pt; font-weight:600; color:#000000;">** EPIC Coder **</span></p>\n'
                '<p align="center" style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'JetBrains Mono\',\'monospace\'; font-size:18pt; font-weight:600; color:#000000;">Travis L. Seymour, PhD</span><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">EPICcoder is a <span style=" font-weight:600; text-decoration: underline;">minimal</span> programmer\'s text editor created for use with the EPIC, EPICpy and pyEPIC simulation environments. It features syntax highlighting for the following file formats: <br /></p>\n'
                '<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;"><li style=" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">PPS Production Rule Files (*.prs) </span></li>\n'
                '<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Text Files (*.txt) </li>\n'
                '<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Python Code Files (*.py)</li>\n'
                '<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">C Code Files (*.c) </li>\n'
                '<li style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">C++ Code Files (*.cpp)</li>\n'
                '<li style=" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">C++ Header Files (*.h)<br /></li></ul>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600;">NOTE</span>: This code is based heavily on the sample code<span style=" vertical-align:super;">1</span> and video tutorial<span style=" vertical-align:super;">2</span> by, FUSEN<span style=" vertical-align:super;">3</span> which itself borrows heavily from the tutorials at &lt;<a href="https://qscintilla.com/"><span style=" text-decoration: underline; color:#0000ff;">https://qscintilla.com/</span></a>&gt;.</p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:12pt;">1. &lt;</span><a href="https://github.com/Fus3n/pyqt-code-editor-yt"><span style=" text-decoration: underline; color:#0000ff;">https://github.com/Fus3n/pyqt-code-editor-yt</span></a><span style=" font-size:12pt;">&gt;<br />2. &lt;</span><a href="https://www.youtube.com/watch?v=ihyDi1aPNBw"><span style=" text-decoration: underline; color:#0000ff;">https://www.youtube.com/watch?v=ihyDi1aPNBw</span></a><span style=" font-size:12pt;">&gt;<br />3. &lt;</span><a href="https://github.com/Fus3n"><span style=" text-decoration: underline; color:#0000ff;">https://github.com/Fus3n</span></a><span style=" font-size:12pt;">&gt;</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'JetBrains Mono\',\'monospace\'; color:#000000;">See </span><a href="https://www.github.com/travisseymour/epiccoder"><span style=" text-decoration: underline; color:#0000ff;">https://www.github.com/travisseymour/epiccoder</span></a><span style=" font-family:\'JetBrains Mono\',\'monospace\'; color:#000000;"> for more information.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'JetBrains Mono','monospace'; font-size:15.8pt; font-weight:600; text-decoration: underline; color:#000000;\">License Statement (GPLv3):</span></p>\n"
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#3584e4; background-color:#ffffff;">EPIC Coder is a minimal programmer\'s text editor created for use with the EPIC, EPICpy and pyEPIC simulation environments. </span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#3584e4; background-color:#ffffff;">Copyright (C) 2022 Travis L. Seymour, PhD</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#3584e4; background-color:#ffffff;">This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#3584e4; background-color:#ffffff;">This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.</span></p>\n'
                '<p style="-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>\n'
                '<p style=" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#3584e4; background-color:#ffffff;">You should have received a copy of the GNU General Public License along with this program. If not, see &lt;</span><a href="http://www.gnu.org/licenses/"><span style=" text-decoration: underline; color:#0000ff;">http://www.gnu.org/licenses/</span></a><span style=" color:#3584e4; background-color:#ffffff;">&gt;.</span></p></body></html>',
            )
        )
        self.pushButtonClose.setText(_translate("aboutDialog", "Close"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    aboutDialog = QtWidgets.QDialog()
    ui = Ui_aboutDialog()
    ui.setupUi(aboutDialog)
    aboutDialog.show()
    sys.exit(app.exec_())
