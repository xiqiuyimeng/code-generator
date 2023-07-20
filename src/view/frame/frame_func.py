# -*- coding: utf-8 -*-
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QStackedWidget, QFrame, \
    QApplication, QStyle

from src.constant.dialog_constant import NAME_UNCHANGED_PROMPT, NAME_AVAILABLE, NAME_EXISTS
from src.service.read_qrc.read_config import read_qss

_author_ = 'luwt'
_date_ = '2023/4/3 12:47'


def set_name_input_style(name_available: bool, current_name: str, old_name: str,
                         name_input: QLineEdit, name_checker: QLabel):
    if name_available:
        # 如果名称无变化，提示
        if old_name == current_name:
            prompt = NAME_UNCHANGED_PROMPT
        else:
            prompt = NAME_AVAILABLE.format(current_name)
        name_checker.setObjectName('checker_right')
        name_input.setObjectName('')
    else:
        prompt = NAME_EXISTS.format(current_name)
        name_checker.setObjectName('checker_wrong')
        name_input.setObjectName('name_input')
    name_input.setStyleSheet(read_qss())
    name_checker.setText(prompt)
    name_checker.setStyleSheet(read_qss())


def reset_name_input_style(name_input: QLineEdit, name_checker: QLabel):
    name_input.setObjectName('')
    name_input.setStyleSheet(read_qss())
    name_checker.setObjectName('')
    name_checker.setStyleSheet(read_qss())
    name_checker.setText('')


def check_available(name, old_name, exists_names):
    if old_name:
        # 假如原有的名称已经重复，那么再输入一遍原有名称，应该提示不可用
        if exists_names.count(old_name) > 1 and name == old_name:
            return False
        return (old_name != name and name not in exists_names) or old_name == name
    else:
        return name not in exists_names


def check_name_available(name, old_name, exists_names, name_input, name_checker):
    if name:
        name_available = check_available(name, old_name, exists_names)
        set_name_input_style(name_available, name, old_name, name_input, name_checker)
        return name_available
    else:
        reset_name_input_style(name_input, name_checker)
        return False


# ---------------------------------------- 表格代理对话框检测文本重复 ---------------------------------------- #

def check_text_available(text: str, exists_data_list, duplicate_checker: QLabel, duplicate_prompt: str):
    text_available = text not in exists_data_list
    if text_available:
        duplicate_checker.setObjectName('')
        duplicate_checker.setText('')
    else:
        duplicate_checker.setObjectName('checker_wrong')
        duplicate_checker.setText(duplicate_prompt)
    duplicate_checker.setStyleSheet(read_qss())
    return text_available


# ---------------------------------------- 构造左边列表，右边堆栈式窗口布局 ---------------------------------------- #

def construct_list_stacked_ui(list_widget_type: type, frame_layout: QVBoxLayout,
                              parent_frame: QFrame, left_stretch, right_stretch):
    # 创建布局，放置列表部件和堆栈式窗口部件
    parent_frame.stacked_layout = QHBoxLayout(parent_frame)
    frame_layout.addLayout(parent_frame.stacked_layout)
    # 创建列表部件
    parent_frame.list_widget = list_widget_type(parent_frame)
    parent_frame.stacked_layout.addWidget(parent_frame.list_widget)
    # 创建堆栈式窗口
    parent_frame.stacked_widget = QStackedWidget(parent_frame)
    parent_frame.stacked_layout.addWidget(parent_frame.stacked_widget)
    # 设置左右比例
    parent_frame.stacked_layout.setStretch(0, left_stretch)
    parent_frame.stacked_layout.setStretch(1, right_stretch)

    # 连接信号
    parent_frame.list_widget.currentRowChanged.connect(parent_frame.stacked_widget.setCurrentIndex)


# ---------------------------------------- 创建带有文件选择功能的输入框和对应label ---------------------------------------- #

def construct_lineedit_file_action():
    file_url_label = QLabel()
    file_url_label.setObjectName('form_label')
    file_url_linedit = QLineEdit()
    choose_file_action = QAction()
    choose_file_action.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirOpenIcon))
    file_url_linedit.addAction(choose_file_action, QLineEdit.ActionPosition.TrailingPosition)
    return file_url_label, file_url_linedit, choose_file_action
