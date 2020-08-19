# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QTreeWidgetItem


_author_ = 'luwt'
_date_ = '2020/8/18 20:07'


class LoadingItem(QTreeWidgetItem):

    @QtCore.pyqtSlot()
    def start(self):
        if hasattr(self, "_movie"):
            self._movie.start()

    @QtCore.pyqtSlot()
    def stop(self):
        if hasattr(self, "_movie"):
            self._movie.stop()
            self.setIcon(0, QtGui.QIcon())

    def set_gif(self, filename):
        if not hasattr(self, "_movie"):
            self._movie = QtGui.QMovie()
            self._movie.setFileName(filename)
            self.setIcon(0, QtGui.QIcon(self._movie.currentPixmap()))
            self._movie.frameChanged.connect(self.on_frameChanged)
            # if self._movie.loopCount() != -1:
            #     self._movie.finished.connect(self.start)
        self.stop()

    @QtCore.pyqtSlot(int)
    def on_frameChanged(self):
        self.setIcon(0, QtGui.QIcon(self._movie.currentPixmap()))


