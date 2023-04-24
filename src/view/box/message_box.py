﻿# -*- coding: utf-8 -*-
"""
消息弹窗
"""

from PyQt5.QtWidgets import QMessageBox

from src.constant.message_box_constant import OK_BUTTON, ACCEPT_BUTTON, REJECT_BUTTON

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


def pop_ok(msg, title, window=None):
    """
    弹出执行成功消息框
    :param msg: 弹窗消息
    :param title: 标题
    :param window: 父窗体
    """
    msg_box = QMessageBox(QMessageBox.NoIcon, title, msg, parent=window)
    # pix = QPixmap(":/icon/right.jpg")\
    #     .scaled(30, 30, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    # msg_box.setIconPixmap(pix)
    msg_box.addButton(OK_BUTTON, QMessageBox.AcceptRole)
    msg_box.exec()


def pop_fail(msg, title, window=None):
    """
    弹出失败消息框
    :param msg: 弹窗消息
    :param title: 标题
    :param window: 父窗体
    """
    msg_box = QMessageBox(QMessageBox.Critical, title, msg, parent=window)
    msg_box.addButton(OK_BUTTON, QMessageBox.AcceptRole)
    msg_box.exec()


def pop_question(msg, title, window=None):
    """
    弹出询问消息框
    :param msg: 弹窗消息
    :param title: 弹窗标题
    :param window: 父窗体
    """
    msg_box = QMessageBox(QMessageBox.Question, title, msg, parent=window)
    msg_box.addButton(ACCEPT_BUTTON, QMessageBox.AcceptRole)
    msg_box.addButton(REJECT_BUTTON, QMessageBox.RejectRole)
    reply = msg_box.exec()
    return True if reply == QMessageBox.AcceptRole else False

