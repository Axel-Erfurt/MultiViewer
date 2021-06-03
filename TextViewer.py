#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import (QFile, Qt, QTextStream)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QMessageBox)
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setStyleSheet(myStyleSheet(self))
        self.MaxRecentFiles = 5
        self.windowList = []
        self.recentFileActs = []
        self.curFile = ''
        self.setAcceptDrops(True)
        self.myeditor = QTextEdit()
        self.myeditor.setAcceptRichText(False)
        self.myeditor.setUndoRedoEnabled(True)
        self.myeditor.setStyleSheet(myStyleSheet(self))
        self.createStatusBar()
        self.setWindowTitle("TextViewer")
        self.setWindowIcon(QIcon.fromTheme("gnome-documents"))
        self.setCentralWidget(self.myeditor)
        self.myeditor.setFocus()

    def closeEvent(self, event):
        event.accept()

    def createStatusBar(self):
        self.statusBar().setStyleSheet(myStyleSheet(self))
        self.statusBar().showMessage("Welcome")

    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Message",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        infile = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.myeditor.setPlainText(infile.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File '" +  fileName + "' loaded", 3000)
            

def myStyleSheet(self):
    return """
QTextEdit
{
background: #eeeeec;
color: #202020;
}
QStatusBar
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #e5e5e5,
                                 stop: 0.5 #e9e9e9, stop: 1.0 #d2d2d2);
font-size: 8pt;
color: #555753;
}
QMenuBar
{
background: transparent;
border: 0px;
}
QToolBar
{
background: transparent;
border: 0px;
}
QMainWindow
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
}
QLineEdit
{
     background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                 stop: 0 #E1E1E1, stop: 0.4 #e5e5e5,
                                 stop: 0.5 #e9e9e9, stop: 1.0 #d2d2d2);
}
QPushButton
{
background: #D8D8D8;
}
QLCDNumber
{
color: #204a87;
}
    """       

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    mainWin = MainWindow()
##    assert(mainWin.locale().language() == QLocale.German)
#    mainWin.show()
#    if len(sys.argv) > 1:
#        print(sys.argv[1])
#        if not sys.argv[1] == "":
#            mainWin.myeditor.setPlainText(sys.argv[1])
#            mainWin.myeditor.document().setModified()
#    sys.exit(app.exec_())
