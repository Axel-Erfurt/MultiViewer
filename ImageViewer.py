#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Image Viewer'
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, 800, 600)
    
        # Create widget
        self.label = QLabel(self)
        
    def show_image(self, infile):
        pixmap = QPixmap(infile)
        ratio = (pixmap.width() / pixmap.height())
        print(ratio)
        self.label.setScaledContents(True)
        self.label.setPixmap(pixmap.scaled(800, 600, Qt.KeepAspectRatio))
        
        self.show()
        if ratio >= 1:
            self.resize(self.width(), self.width() / ratio)
        else:
            self.resize(self.height()  * ratio, self.height())

#if __name__ == '__main__':
#    app = QApplication(sys.argv)
#    ex = App()
#    ex.show_image('/home/brian/Bilder/gela6Bleistift.jpg')
#    sys.exit(app.exec_())