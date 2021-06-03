#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPalette, QKeySequence, QIcon
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTime, QMimeData
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
                            QPushButton, QSizePolicy, QSlider, QMessageBox, QStyle, QVBoxLayout,  
                            QWidget, QShortcut)
import os
import subprocess
#QT_DEBUG_PLUGINS

class VideoPlayer(QWidget):

    def __init__(self, aPath, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.setAttribute( Qt.WA_NoSystemBackground, True )
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)
        
        self.lbl = QLineEdit('00:00:00')
        self.lbl.setFixedWidth(70)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.setStyleSheet(stylesheet(self))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setFixedWidth(70)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.setStyleSheet(stylesheet(self))

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)
        self.playButton.setStyleSheet("background-color: black")
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setStyleSheet (stylesheet(self)) 
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.sliderMoved.connect(self.handleLabel)
        self.positionSlider.setSingleStep(2)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(5, 0, 5, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.lbl)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.elbl)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)

        self.setLayout(layout)

        self.widescreen = True

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.positionChanged.connect(self.handleLabel)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        print("QT5 Player started")
        self.suspend_screensaver()


    def suspend_screensaver(self):
        'suspend linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled false', shell=True)
        proc.wait()

    def resume_screensaver(self):
        'resume linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled true', shell=True)
        proc.wait()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Videos (*.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

    def playFromURL(self):
        self.mediaPlayer.pause()
        clip = QApplication.clipboard()
        myurl = clip.text()
        self.mediaPlayer.setMedia(QMediaContent(QUrl(myurl)))
        self.playButton.setEnabled(True)
        self.mediaPlayer.play()
        self.hideSlider()
        print(myurl)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        
    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0,0,0,0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: ", self.mediaPlayer.errorString())

    def closeEvent(self, event):
        self.mediaPlayer.stop()
        self.resume_screensaver()
        print("Goodbye ...")
        QApplication.quit()
        
    def handleQuit(self):
        self.mediaPlayer.stop()
        self.resume_screensaver()
        print("Goodbye ...")
        QApplication.quit()

    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        mheight = self.frameGeometry().height()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, mwidth / mratio)

    def handleInfo(self):
            msg = QMessageBox()
            msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            msg.setGeometry(self.frameGeometry().left() + 30, self.frameGeometry().top() + 30, 300, 400)
            msg.setIcon(QMessageBox.Information)
            msg.setText("QT5 Player")
            msg.setInformativeText(self.myinfo)
            msg.setStandardButtons(QMessageBox.Close)
#            msg.exec()
            msg.show()
            
    
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

    def forwardSlider10(self):
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000*60)

    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000*60)
        
    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
    
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
    
    def loadFilm(self, f):
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
            self.playButton.setEnabled(True)
            self.mediaPlayer.play()
            print(self.mediaPlayer.media().canonicalResource().resolution())
      
    def openFileAtStart(self, filelist):
            matching = [s for s in filelist if ".myformat" in s]
            if len(matching) > 0:
                self.loadFilm(matching)

##################### update Label ##################################
    def handleLabel(self):
            self.lbl.clear()
            mtime = QTime(0,0,0,0)
            self.time = mtime.addMSecs(self.mediaPlayer.position())
            self.lbl.setText(self.time.toString())
###################################################################

def stylesheet(self):
    return """

QSlider::handle:horizontal 
{
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #333, stop:1 #555555);
width: 14px;
border-radius: 0px;
}

QSlider::groove:horizontal {
border: 1px solid #444;
height: 10px;
background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000, stop:1 #222222);
}

QLineEdit
{
background: black;
color: #585858;
border: 0px solid #076100;
font-size: 12px;
font-weight: bold;
}
    """

#if __name__ == '__main__':
#
#    import sys
##    QApplication.setDesktopSettingsAware(False)
#    app = QApplication(sys.argv)
#
#    player = VideoPlayer('')
#    player.setAcceptDrops(True)
#    player.setWindowTitle("QT5 Player")
#    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#    player.setGeometry(100, 300, 600, 380)
#    player.setContextMenuPolicy(QtCore.Qt.CustomContextMenu);
#    player.customContextMenuRequested[QtCore.QPoint].connect(player.contextMenuRequested)
#    player.hideSlider()
#    player.show()
#    player.widescreen = True
#    if len(sys.argv) > 1:
#        print(sys.argv[1])
#        player.loadFilm(sys.argv[1])
#sys.exit(app.exec_())
