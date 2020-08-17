# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from static import style_rc


_author_ = 'luwt'
_date_ = '2020/8/17 10:27'


def read_qss():
    file = QFile(":/style.qss")
    file.open(QIODevice.ReadOnly)
    qss = QTextStream(file).readAll()
    file.close()
    return qss
