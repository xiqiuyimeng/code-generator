# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLineEdit, QLabel, QAction

from src.constant.dialog_constant import NAME_UNCHANGED_PROMPT, NAME_AVAILABLE, NAME_EXISTS
from src.constant.icon_enum import get_icon
from src.service.read_qrc.read_config import read_qss

_author_ = 'luwt'
_date_ = '2023/4/3 12:47'


def set_name_input_style(name_available: bool, current_name: str, old_name: str,
                         name_input_qss_id: str, name_input: QLineEdit, check_action: QAction,
                         name_checker: QLabel):
    if name_available:
        # 如果名称无变化，提示
        if old_name == current_name:
            prompt = NAME_UNCHANGED_PROMPT
        else:
            prompt = NAME_AVAILABLE.format(current_name)
        style = "color:green"
        # 重载样式表
        name_input.setStyleSheet(read_qss())
        icon = get_icon(NAME_AVAILABLE)
    else:
        prompt = NAME_EXISTS.format(current_name)
        style = "color:red"
        name_input.setStyleSheet(f"#{name_input_qss_id}{{border-color:red;color:red}}")
        icon = get_icon(NAME_EXISTS)
    check_action.setIcon(icon)
    name_input.addAction(check_action, QLineEdit.ActionPosition.TrailingPosition)
    name_checker.setText(prompt)
    name_checker.setStyleSheet(style)


def reset_name_input_style(name_input: QLineEdit, name_checker: QLabel, check_action: QAction):
    name_input.setStyleSheet(read_qss())
    name_checker.setStyleSheet(read_qss())
    name_checker.setText('')
    name_input.removeAction(check_action)
