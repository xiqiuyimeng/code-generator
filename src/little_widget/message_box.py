# -*- coding: utf-8 -*-
"""
消息弹窗
"""

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from src.constant.constant import OK_BUTTON, ACCEPT_BUTTON, \
    REJECT_BUTTON, WARNING_OK, WARNING_RESELECT


_author_ = 'luwt'
_date_ = '2020/6/21 16:08'


def pop_msg(title, msg):
    """
    弹出普通信息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    """
    msg_box = QMessageBox(QMessageBox.Information, title, msg)
    msg_box.addButton(OK_BUTTON, QMessageBox.AcceptRole)
    msg_box.exec()


def pop_ok(title, msg):
    """
    弹出执行成功消息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    """
    msg_box = QMessageBox(QMessageBox.NoIcon, title, msg)
    pix = QPixmap(":/icon/right.jpg")\
        .scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    msg_box.setIconPixmap(pix)
    msg_box.addButton(OK_BUTTON, QMessageBox.AcceptRole)
    msg_box.exec()


def pop_fail(title, msg):
    """
    弹出失败消息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    """
    msg_box = QMessageBox(QMessageBox.Critical, title, msg)
    msg_box.addButton(OK_BUTTON, QMessageBox.AcceptRole)
    msg_box.exec()


def pop_question(title, msg):
    """
    弹出询问消息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    """
    msg_box = QMessageBox(QMessageBox.Question, title, msg)
    msg_box.addButton(ACCEPT_BUTTON, QMessageBox.AcceptRole)
    msg_box.addButton(REJECT_BUTTON, QMessageBox.RejectRole)
    reply = msg_box.exec()
    return True if reply == QMessageBox.AcceptRole else False


def pop_warning(title, msg):
    """
    弹出警告信息框
    :param title: 弹窗标题
    :param msg: 弹窗消息
    """
    msg_box = QMessageBox(QMessageBox.Warning, title, msg)
    msg_box.addButton(WARNING_OK, QMessageBox.AcceptRole)
    msg_box.addButton(WARNING_RESELECT, QMessageBox.RejectRole)
    reply = msg_box.exec()
    return True if reply == QMessageBox.AcceptRole else False

