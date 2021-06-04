#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication

infile = sys.argv[1] 

csv = ["csv", "tsv"]
video = ["mp4", "flv", "mpg", "mpeg", "m4v", "mov", "vob", "mkv"]
audio = ["mp3", "m4a", "ogg", "flac", "wav", "aif", "aiff"]
text = ["txt", "m3u", "m3u8", "pls", "py", "sh"]
html = ["html", "htm"]
pdf = ["pdf"]
image = ["png", "jpg", "eps", "gif", "bmp", "tiff", "tif", "jpeg", "svg"]
odt = ["odt", "doc", "docx", "rtf"]

def show_file(infile):
    extension = infile.rpartition(".")[2]
    if extension in csv:    
        show_csv(infile)
    elif extension in video: 
        show_video(infile)
    elif extension in audio: 
        show_audio(infile) 
    elif extension in text: 
        show_text(infile) 
    elif extension in html: 
        show_html(infile) 
    elif extension in pdf: 
        show_pdf(infile) 
    elif extension in odt: 
        show_odt(infile) 
    elif extension in image: 
        show_image(infile) 
        
def show_csv(infile):
    import CSV_Viewer
    app = QApplication(sys.argv)
    main = CSV_Viewer.MyWindow('')
    main.setGeometry(0, 0, 800, 600)
    main.setWindowTitle("CSV Viewer")
    main.show()
    main.loadCsvOnOpen(infile)
    sys.exit(app.exec_())
    
def show_video(infile):
    import VideoViewer
    app = QApplication(sys.argv)
    player = VideoViewer.VideoPlayer('')
    player.setAcceptDrops(True)
    player.setWindowTitle("Video")
    player.setGeometry(100, 300, 600, 380)
    player.show()
    player.widescreen = True
    player.loadFilm(infile)
    sys.exit(app.exec_())
    
def show_audio(infile):
    import VideoViewer
    app = QApplication(sys.argv)
    player = VideoViewer.VideoPlayer('')
    player.setAcceptDrops(True)
    player.setWindowTitle("Audio")
    player.setGeometry(100, 300, 600, 30)
    player.mediaPlayer.setVolume(75)
    player.show()
    player.widescreen = True
    player.loadFilm(infile)
    sys.exit(app.exec_())
    
def show_text(infile):
    import TextViewer
    app = QApplication(sys.argv)
    mainWin = TextViewer.MainWindow()
    mainWin.setGeometry(0, 0, 800, 600)
    mainWin.show()
    my_text = open(infile, 'r').read()
    mainWin.myeditor.setPlainText(my_text)
    sys.exit(app.exec_())
    
def show_html(infile):
    import WebViewer
    app = QApplication(sys.argv)
    win = WebViewer.MainWindow()
    win.show()
    win.url = f"file://{infile}"
    win.showURL(win.url)
    sys.exit(app.exec_())
    
def show_pdf(infile):
        import PDFViewer
        app = QApplication(sys.argv)
        mainWin = PDFViewer.Window()
        mainWin.loadPDF(infile)
        mainWin.showMaximized()
        sys.exit(app.exec_())
        
def show_odt(infile):
    import ODF_Viewer
    app = QApplication(sys.argv)
    win = ODF_Viewer.myEditor()
    win.setWindowTitle("Libre Viewer" + "[*]")
    win.setGeometry(0, 0, 800, 600)
    win.show()
    win.openFileOnStart(infile)
    app.exec_()
    
def show_image(infile):
    import ImageViewer
    app = QApplication(sys.argv)
    ex = ImageViewer.App()
    ex.show_image(infile)
    sys.exit(app.exec_())
        
show_file(infile)
