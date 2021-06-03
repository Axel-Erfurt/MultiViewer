#!/usr/bin/python3
#-*- coding:utf-8 -*-
import csv 
import os
import pandas as pd
from PyQt5 import QtPrintSupport
from PyQt5.QtGui import (QIcon, QKeySequence, QTextCursor, QPalette,
                        QCursor, QDropEvent, QTextDocument, QTextTableFormat, QColor)
from PyQt5.QtCore import (QFile, Qt, QFileInfo, QDir, 
                        QMetaObject)
from PyQt5.QtWidgets import (QMainWindow , QAction, QWidget, QLineEdit, 
                             QMessageBox, QAbstractItemView, QApplication, 
                             QTableWidget, QTableWidgetItem, QGridLayout, 
                             QFileDialog, QMenu, QInputDialog, QPushButton)


class TableWidgetDragRows(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDragDropOverwriteMode(False)
        self.setDropIndicatorShown(True)

        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent):
        if not event.isAccepted() and event.source() == self:
            drop_row = self.drop_on(event)

            rows = sorted(set(item.row() for item in self.selectedItems()))
            rows_to_move = ([[QTableWidgetItem(self.item(row_index, column_index)) 
                            for column_index in range(self.columnCount())]
                            for row_index in rows])
            for row_index in reversed(rows):
                self.removeRow(row_index)
                if row_index < drop_row:
                    drop_row -= 1

            for row_index, data in enumerate(rows_to_move):
                row_index += drop_row
                self.insertRow(row_index)
                for column_index, column_data in enumerate(data):
                    self.setItem(row_index, column_index, column_data)
            event.accept()
            for row_index in range(len(rows_to_move)):
                self.item(drop_row + row_index, 0).setSelected(True)
                self.item(drop_row + row_index, 1).setSelected(True)
        super().dropEvent(event)

    def drop_on(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            return self.rowCount()

        return index.row() + 1 if self.is_below(event.pos(), index) else index.row()

    def is_below(self, pos, index):
        rect = self.visualRect(index)
        margin = 2
        if pos.y() - rect.top() < margin:
            return False
        elif rect.bottom() - pos.y() < margin:
            return True
        # noinspection PyTypeChecker
        return rect.contains(pos, True) and not (int(self.model().flags(index)) & Qt.ItemIsDropEnabled) and pos.y() >= rect.center().y()

class MyWindow(QMainWindow):
    def __init__(self, aPath, parent=None):
        super(MyWindow, self).__init__(parent)
        QMetaObject.connectSlotsByName(self)
        self.delimit = '\t'
        self.mycolumn = 0
        self.windowList = []
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.isChanged = False
        self.fileName = ""
        self.fname = "Liste"
        self.mytext = ""
        self.colored = False
        self.copiedRow = []
        self.copiedColumn = []
        ### QTableView seetings
        self.tableView = TableWidgetDragRows()
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setGridStyle(1)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setShowGrid(True)
        self.tableView.horizontalHeader().setBackgroundRole(QPalette.Window)
        self.tableView.setDropIndicatorShown(True)
        self.setCentralWidget(self.tableView)
        self.isChanged = False
        self.setStyleSheet(stylesheet(self))
        self.msg("Welcome to CSV Reader")
        
    def changeSelection(self):
        self.tableView.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def msgbox(self, message):
        QMessageBox.warning(self, "Message", message)


    def handleQuit(self):
        quit()


    def loadCsvOnOpen(self, fileName):
        if fileName:

            df = pd.read_csv(fileName, header=None, delimiter='\t', \
            skip_blank_lines=True, error_bad_lines=False, na_filter= False)
            header = df.iloc[0]

            self.tableView.setColumnCount(len(df.columns))
            self.tableView.setRowCount(len(df.index))
    
            for i in range(len(df.index)):
                for j in range(len(df.columns)):
                    self.tableView.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

            for j in range(self.tableView.columnCount()):
                m = QTableWidgetItem(str(j))
                self.tableView.setHorizontalHeaderItem(j, m)
    
            self.tableView.selectRow(0)
            self.isChanged = False
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
            self.msg(fileName + " loaded")

    def loadCsv(self):
        if self.isChanged == True:
            quit_msg = "<b>The Document was changed.<br>Do you want to save changes?</ b>"
            reply = QMessageBox.question(self, 'Save Confirmation', 
                     quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.saveOnQuit()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open CSV",
        (QDir.homePath() + "/Dokumente/CSV"), "CSV (*.csv *.tsv *.txt)")
        if fileName:
            self.loadCsvOnOpen(fileName)

    def closeEvent(self, event):
        if self.isChanged == True:
            quit_msg = "<b>The document was changed.<br>Do you want to save the changes?</ b>"
            reply = QMessageBox.question(self, 'Save Confirmation', 
                     quit_msg, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
                self.saveOnQuit()
        print("Goodbye ...")

    def msg(self, message):
        self.statusBar().showMessage(message)



def stylesheet(self):
        return """
 QTableWidget
{
background: #e1e1e1;
selection-color: white;
border: 1px solid lightgrey;
selection-background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
color: #202020;
outline: 0;
} 

QTableWidget::item::hover{
background: qlineargradient(y1: 0, y2: 1, stop: 0 #babdb6, stop: 0.5 #d3d7cf, stop: 1 #babdb6);
}
QTableWidget::item::focus
{
background: qlineargradient( y1: 0, y2: 1, stop: 0 #729fcf, stop: 1  #204a87);
border: 0px;
}

QHeaderView::section
{background-color:#d3d7cf;
color: #2e3436; 
font: bold
}

QTableCornerButton::section 
{
background-color:#d3d7cf; 
}

QStatusBar
{
    font-size: 7pt;
    color: #717171
}
QLineEdit
{
   color: #484848;
    background-color: #fbfbfb;
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

QPushButton
{
background: #d3d7cf ;
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
    """

#if __name__ == "__main__":
#    import sys
#
#    app = QApplication(sys.argv)
#    app.setApplicationName('MyWindow')
#    main = MyWindow('')
#    main.setMinimumSize(820, 300)
#    main.setWindowTitle("CSV Viewer")
#    main.show()
#
#sys.exit(app.exec_())