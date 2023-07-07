# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QTabWidget, QWidget, QVBoxLayout

from src.view.custom_widget.text_editor import TextEditor

_author_ = 'luwt'
_date_ = '2023/5/5 16:44'


class PreviewGenerateFileTabWidget(QTabWidget):

    def make_tab(self, file_name, file_content):
        # 创建tab页
        tab_widget = QWidget()
        tab_widget_layout = QVBoxLayout(tab_widget)
        tab_widget_layout.setContentsMargins(0, 0, 0, 0)
        tab_widget.setLayout(tab_widget_layout)
        # 内容为一个文本编辑区
        content_editor = TextEditor()
        tab_widget_layout.addWidget(content_editor)
        content_editor.setPlainText(file_content)
        # 添加引用
        setattr(tab_widget, 'content_editor', content_editor)
        # 添加到tab页中
        self.addTab(tab_widget, file_name)
        return tab_widget

