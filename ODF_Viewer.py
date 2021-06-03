#!/usr/bin/python3
# -- coding: utf-8 --
from PyQt5.QtWidgets import QTextEdit, QApplication, QMessageBox, QMainWindow
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt, QProcess
import sys, os

tab = "\t"
eof = "\n"

class myEditor(QMainWindow):
    def __init__(self, parent = None):
        super(myEditor, self).__init__(parent)

        self.setStyleSheet(myStyleSheet(self))
        self.mainText = " "
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.editor = QTextEdit() 

        self.editor.setStyleSheet(myStyleSheet(self))
        self.setCentralWidget(self.editor)

    def msgbox(self,title, message):
        QMessageBox.warning(self, title, message)
            
       ### open File
    def openFileOnStart(self, path=None):
        if path:
            print(path)
            file_name = path.rpartition("/")[2].rpartition(".")[0]
            print(file_name)
            QProcess.execute(f"soffice --headless --convert-to html:HTML --outdir /tmp {path}")
            new_path = f"/tmp/{file_name}.html"
            data = open(new_path, 'r').read()
            unistr = str(data)

            if Qt.mightBeRichText(unistr):
                self.editor.setHtml(unistr)
            else:
                self.editor.setPlainText(unistr)
            self.filename = path
            self.document = self.editor.document()
            self.statusBar().showMessage("loaded file '" + path + "'")

    def closeEvent(self, e):
        e.accept()
        
    def handleQuit(self):
        print("Goodbye ...")

    def document(self):
        return self.editor.document

    def setLineWrapMode(self, mode):
        self.editor.setLineWrapMode(mode)

    def setDocumentTitle(self, *args, **kwargs):
        self.editor.setDocumentTitle(*args, **kwargs)

    def set_number_bar_visible(self, value):
        self.numbers.setVisible(value)

    def currentCharFormatChanged(self, format):
        self.fontChanged(format.font())
        self.colorChanged(format.foreground().color())

    def cursorPositionChanged(self):
        self.alignmentChanged(self.editor.alignment())

    def clipboardDataChanged(self):
        self.actionPaste.setEnabled(len(QApplication.clipboard().text()) != 0)

    def mergeFormatOnWordOrSelection(self, format):
        cursor = self.editor.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)

        cursor.mergeCharFormat(format)
        self.editor.mergeCurrentCharFormat(format)
  
def myStyleSheet(self):
    return """
QTextEdit
{
background: #fafafa;
color: #202020;
border: 1px solid #1EAE3D;
selection-background-color: #729fcf;
selection-color: #ffffff;
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

    """       

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    win = myEditor()
#    win.setWindowIcon(QIcon.fromTheme("gnome-mime-application-rtf"))
#    win.setWindowTitle("Libre Viewer" + "[*]")
#    win.setGeometry(0, 0, 800, 600)
#    win.show()
#    #win.openFileOnStart("/home/brian/Dokumente/HTML_Text/VPCM13M1E.html")
#    win.openFileOnStart("/home/brian/Dokumente/ODF/640_TV.odt")
#    app.exec_()
