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


def check_available(name, old_name, exits_name_tuple):
    if old_name:
        # 假如原有的名称已经重复，那么再输入一遍原有名称，应该提示不可用
        if exits_name_tuple.count(old_name) > 1 and name == old_name:
            return False
        return (old_name != name and name not in exits_name_tuple) or old_name == name
    else:
        return name not in exits_name_tuple


def check_name_available(name, old_name, exits_name_tuple, name_check_action, name_input,
                         name_checker, name_input_qss_id):
    if name_check_action is Ellipsis:
        name_check_action = QAction()
    if name:
        name_available = check_available(name, old_name, exits_name_tuple)
        set_name_input_style(name_available, name, old_name, name_input_qss_id,
                             name_input, name_check_action, name_checker)
        return name_available
    else:
        reset_name_input_style(name_input, name_checker, name_check_action)
        return False


# ---------------------------------------- 表格代理对话框检测文本重复 ---------------------------------------- #

def check_text_available(text: str, exists_data_tuple, duplicate_checker: QLabel, duplicate_prompt: str):
    text_available = text not in exists_data_tuple
    if text_available:
        duplicate_checker.setStyleSheet(read_qss())
        duplicate_checker.setText('')
    else:
        style = "color:red"
        duplicate_checker.setText(duplicate_prompt)
        duplicate_checker.setStyleSheet(style)
    return text_available
