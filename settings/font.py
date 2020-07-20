# -*- coding: utf-8 -*-
"""字体设置"""
from PyQt5 import QtGui

_author_ = 'luwt'
_date_ = '2020/7/18 17:07'


def set_font():
    font = QtGui.QFont()
    font.setFamily("楷体")
    font.setPointSize(13)
    return font


def set_title_font(title):
    return "<html><head/><body><p align=\"center\"><span " \
           "style=\" font-size:20pt; font-weight:600;\">" \
           f"{title}</span></p></body></html>"


def set_label_font(text):
    return "<html><span style=\" font-size:15pt; " \
           f"font-weight:600;\">{text}</span></html>"

