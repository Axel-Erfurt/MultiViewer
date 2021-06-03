#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os.path

from PyQt5.QtCore import Qt, QRectF, pyqtSignal, QT_VERSION_STR
from PyQt5.QtGui import QImage, QPixmap, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog


class QtImageViewer(QGraphicsView):
    def __init__(self):
        QGraphicsView.__init__(self)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self._pixmapHandle = None
        self.aspectRatioMode = Qt.KeepAspectRatio
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.zoomStack = []

        self.canZoom = True
        self.canPan = True

    def hasImage(self):
        return self._pixmapHandle is not None

    def clearImage(self):
        if self.hasImage():
            self.scene.removeItem(self._pixmapHandle)
            self._pixmapHandle = None

    def pixmap(self):
        if self.hasImage():
            return self._pixmapHandle.pixmap()
        return None

    def image(self):
        if self.hasImage():
            return self._pixmapHandle.pixmap().toImage()
        return None

    def setImage(self, image):
        if type(image) is QPixmap:
            pixmap = image
        elif type(image) is QImage:
            pixmap = QPixmap.fromImage(image)
        else:
            raise RuntimeError("ImageViewer.setImage: Argument must be a QImage or QPixmap.")
        if self.hasImage():
            self._pixmapHandle.setPixmap(pixmap)
        else:
            self._pixmapHandle = self.scene.addPixmap(pixmap)
        self.setSceneRect(QRectF(pixmap.rect()))
        self.updateViewer()

    def loadImageFromFile(self, fileName):
        image = QImage(fileName)
        self.setImage(image)

    def updateViewer(self):
        if not self.hasImage():
            return
        self.zoomStack = [] 
        self.fitInView(self.sceneRect(), self.aspectRatioMode)
        
    def resizeEvent(self, event):
        """ Maintain current zoom on resize.
        """
        self.updateViewer()

    def mousePressEvent(self, event):
        scenePos = self.mapToScene(event.pos())
        QGraphicsView.mousePressEvent(self, event)


#if __name__ == '__main__':
#    from PyQt5.QtWidgets import QApplication
#    import sys
#    app = QApplication(sys.argv)
#    viewer = QtImageViewer()
#    viewer.loadImageFromFile("/home/brian/Bilder/20180720_075228.jpg")
#    viewer.move(0, 0)
#    viewer.setWindowTitle("Image Viewer")
#    viewer.show()
#    sys.exit(app.exec_())
