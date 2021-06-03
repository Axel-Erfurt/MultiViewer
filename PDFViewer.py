#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView

mfile = ""
root = os.path.dirname(sys.argv[0])

class Window(QWebEngineView):
    def __init__(self):
        super(Window, self).__init__()
        self.PDFJS = f"file://{os.path.abspath('./web/viewer.html')}"


    def loadPDF(self, mfile):
        self.PDF = f'file://{mfile}'
        print(self.PDFJS)
        print("loading PDF:", self.PDF)
        self.load(QUrl.fromUserInput(f'{self.PDFJS}?file={self.PDF}'))        

if __name__ == '__main__':

    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())