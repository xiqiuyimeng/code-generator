# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QMessageBox, QErrorMessage
_author_ = 'luwt'
_date_ = '2020/6/21 16:08'


def pop_success(msg):
    QMessageBox.information(QMessageBox(), 'mysql', msg, QMessageBox.Ok)


def pop_fail():...


