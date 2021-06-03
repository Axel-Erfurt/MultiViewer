#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5 import QtWebEngineWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        
        self.url = ""

        self.setWindowTitle("TV")
        self.setGeometry(0, 0, 800, 600)
        self.centralWidget = QtWidgets.QWidget(self)

        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.webView.settings().setAttribute(QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.setCentralWidget(self.webView)
        self.url = ""
        #self.showURL(self.url)
        
    def showURL(self, url):
        print(url)
        self.webView.setUrl(QtCore.QUrl(url))

    def url_changed(self):
        self.setWindowTitle(self.webView.title())

    def go_back(self):
        self.webView.back()

#if __name__ == '__main__':
#
#    import sys
#    app = QtWidgets.QApplication(sys.argv)
#    win = MainWindow()
#    win.show()
#    sys.exit(app.exec_())