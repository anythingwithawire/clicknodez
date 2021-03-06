#
# Copyright 2015-2017 Eric Thivierge
#
import sys
from random import random

from PyQt5.QtCore import Qt, QByteArray, QDataStream, QIODevice, QMimeData, QRect
# from PySide2.Qt import QString
from PyQt5.QtGui import QKeySequence, QFont

from PyQt5.QtWidgets import QMainWindow, QApplication, QLineEdit, QTableWidget, QTableWidgetItem, QAbstractItemView, \
    QMenu
from qtpy import QtGui, QtWidgets, QtCore

import pyperclip
import os, sys
from clipboard import ClipboardEx

class H3TableHandler:
    def __init__(self, parent=None):
        self.parent = parent
    def right_click(self):
        # bar = self.parent.menuBar()
        top_menu = QMenu(self.parent)

        menu = top_menu.addMenu("Menu")
        config = menu.addMenu("Configuration ...")

        _load = config.addAction("&Load ...")
        _save = config.addAction("&Save ...")

        config.addSeparator()

        config1 = config.addAction("Config1")
        config2 = config.addAction("Config2")
        config3 = config.addAction("Config3")

        action = menu.exec_(QtGui.QCursor.pos())

        if action == _load:
            # do this
            pass
        elif action == _save:
            # do this
            pass
        elif action == config1:
            # do this
            pass
        elif action == config2:
            # do this
            pass
        elif action == config3:
            # do this
            pass

class cclip():
    data = ''


class TableWidgetCustom(QTableWidget, QTableWidgetItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        #self.text_clip = None
        self.text_clip = ''
        self.__node_counter = 0

        self.setWindowTitle("FlowGraph Main")
        self.setGeometry(2000, 0, 200, 200)
        #min graph window here

        self.mime_data = ClipboardEx().clipboard.mimeData()

    def colorTable(self):
        for row in range(self.rowCount()):
            for column in range(self.columnCount()):
                item1 = QtWidgets.QTableWidgetItem()
            if row % 2 == 0:
                item1.setBackground(QtGui.QColor(255, 128, 128))
            self.table.setItem(row,0,item1)

    def keyPressEvent(self, event):
        if event.matches(QKeySequence.Save):
            self.save()
        if event.matches(QKeySequence.Open):
            self.restore()
        if event.matches(QKeySequence.Delete):
            self.delete()
        if event.matches(QKeySequence.Copy):
            self.copy()
        if event.matches(QKeySequence.Paste):
            self.paste()
        QTableWidget.keyPressEvent(self, event)

    def delete(self):
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item.isSelected():
                    item = QTableWidgetItem()
                    item.setText(str(""))
                    self.setItem(row, col, item)


    def save(self):
        print("saving")
        # using findChildren is for simplicity, it's probably better to create
        # your own list of widgets to cycle through
        f = open(str(self.windowTitle())+"_data", "wt")
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.item(row, col)
                if item:
                    txt = item.text()
                else:
                    txt = 'x'
                f.write(txt)
                f.write(",")
            f.write("\n")
        f.close()

    def copy(self):
        #self.clipboard.clear(mode=self.clipboard.Clipboard)
        clip = ""
        i=0
        print(self.rowCount(), self.columnCount())
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                item = self.item(row, col)
                if item.isSelected():
                    i = i + 1
                    #item = QTableWidgetItem()
                    item = self.item(row, col)
                    clip = clip + str(item.text())+str(" \t ")
            cclip.data = str(clip) + str("\n")
        cclip.data = cclip.data + str("\n")
        print("selected ", i, "\n", cclip.data)


    def paste(self):
        #self.clipboard.clear(mode=self.clipboard.Clipboard)
        i = 0
        print(self.rowCount(), self.columnCount())
        l = cclip.data.split("\t")
        #l = self.mime_data.data("text").split(",")
        #l = dddd.split(',')
        print("==l==>", l)
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                item = self.item(row, col)
                if item.isSelected():
                    item = QTableWidgetItem()
                    item = self.item(row, col)
                    item.setText(l[i].strip())
                    self.setItem(row, col, item)
                    i = i + 1
                    if i >= len(l)-1:
                        i=0


    def restore(self):
        print("restore")
        f = open(str(self.windowTitle())+"_data", "rt")
        i = 0
        for row in range(self.rowCount()):
            l = f.readline()
            d = l.split(",")
            for col in range(self.columnCount()):
                item = QTableWidgetItem()
                if col >= len(d):
                    item.setText("")
                else:
                    item.setText(str(d[col]))
                i = i + 1
                self.setItem(row, col, item)
                item.setTextAlignment(Qt.AlignHCenter)

        f.close()

    def h3_table_right_click(self, position):
        o_h3_table = H3TableHandler(parent=self)
        o_h3_table.right_click()


class DataWindow(QMainWindow, TableWidgetCustom):
    def __init__(self, e=None):
        super().__init__()

        self.pc = pyperclip

        self.cb = ClipboardEx()
        self.cb.show()
        self.mime_data = self.cb.clipboard.mimeData()

        self.pb1 = QtWidgets.QPushButton('Set Node IP\nFrom Cable', self)
        self.pb1.resize(100, 32)
        self.pb1.move(50, 50)
        self.pb1.clicked.connect(self.pb1_clicked)

        '''pb2 = QtWidgets.QPushButton('Set Node OP\nFrom Cable', self)
        pb2.resize(100, 32)
        pb2.move(150, 50)
        pb2.clicked.connect(self.pb2_clicked)

        pb3 = QtWidgets.QPushButton('Zoom In', self)
        pb3.resize(100, 32)
        pb3.move(50, 100)
        pb3.clicked.connect(self.pb3_clicked)

        pb4 = QtWidgets.QPushButton('Zoom Out', self)
        pb4.resize(100, 32)
        pb4.move(150, 100)
        pb4.clicked.connect(self.pb4_clicked)

        pb5 = QtWidgets.QPushButton('Node Make', self)
        pb5.resize(100, 32)
        pb5.move(50, 150)
        pb5.clicked.connect(self.pb5_clicked)

        pb6 = QtWidgets.QPushButton('Node Trunk', self)
        pb6.resize(100, 32)
        pb6.move(150, 150)
        pb6.clicked.connect(self.pb6_clicked)'''


        self.cableInfoWidget = TableWidgetCustom()
        # self.cableInfoWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.cableInfoWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.cableInfoWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.cableInfoWidget.setColumnCount(6)
        self.cableInfoWidget.setRowCount(20)
        self.cableInfoWidget.setGeometry(1000, 0, 400, 600)

        self.cableInfoWidget.setWindowTitle("Cable Termination Map")
        self.cableInfoWidget.setHorizontalHeaderLabels((("FmTermName;FmCoreNum;Cable;ToCoreNum;ToTermName").split(";")))

        self.cableInfoWidget.show()
        self.cableInfoWidget.restore()

        self.nodeInfoWidget = TableWidgetCustom()
        # self.nodeInfoWidget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.nodeInfoWidget.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.nodeInfoWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.nodeInfoWidget.setColumnCount(13)
        self.nodeInfoWidget.setRowCount(20)
        self.nodeInfoWidget.setGeometry(500, 0, 400, 600)

        self.nodeInfoWidget.setWindowTitle("Node Termination Map")
        self.nodeInfoWidget.setHorizontalHeaderLabels((("x;y;TermName;TermNum;SeqNum;Node;SeqNum;TermNum;TermName;x;y;width;height").split(";")))
        self.nodeInfoWidget.restore()

        # self.restore()
        # self.nodeInfoWidget.cellClicked.connect(self.save)

        self.nodeInfoWidget.show()

        #self.h = self.h3_table_right_click(TableWidgetCustom.PositionAtTop)




    def pb1_clicked(self):
        pass

    def pb2_clicked(self):
        pass

    def pb3_clicked(self):
        self.graph.scale(1.5, 1.5)

    def pb4_clicked(self):
        self.graph.scale(0.5, 0.5)

    def pb5_clicked(self):
        pass

    def pb6_clicked(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = DataWindow()
    w.resize(500, 500)
    w.setWindowTitle("FlowGraph")
    w.show()
    sys.exit(app.exec_())

