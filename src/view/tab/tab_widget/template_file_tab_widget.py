# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit

from src.constant.template_dialog_constant import FILE_NAME_TEMPLATE_LABEL_TEXT
from src.view.custom_widget.text_editor import TextEditor
from src.view.list_widget.list_item_func import get_template_file_data
from src.view.tab.tab_bar.tab_bar_abc import TabBarABC

_author_ = 'luwt'
_date_ = '2023/3/13 11:29'


class TemplateFileTabWidget(QTabWidget):

    def __init__(self, file_list_widget, *args):
        super().__init__(*args)
        self.file_list_widget = file_list_widget
        self.setTabBar(TabBarABC(self))

    def removeTab(self, index: int):
        """重写删除tab方法，在删除时，将tab页数据刷入模板文件对象"""
        # 一定能找到tab对应的列表项
        list_index = [row for row in range(self.file_list_widget.count())
                      if self.tabText(index) == self.file_list_widget.item(row).text()][0]
        list_item = self.file_list_widget.item(list_index)
        template_file_data = get_template_file_data(list_item)
        # 将tab页内保存的文本数据刷入对象中
        template_file_data.file_content = self.widget(index).content_editor.toPlainText()
        template_file_data.file_name_template = self.widget(index).file_name_edit.text()
        super().removeTab(index)

    def add_file_tab(self, template_file):
        tab_widget = QWidget()
        self.addTab(tab_widget, template_file.file_name)
        self.setCurrentIndex(self.count() - 1)

        tab_layout = QVBoxLayout(tab_widget)
        file_name_layout = QFormLayout()
        tab_layout.addLayout(file_name_layout)
        file_name_label = QLabel()
        file_name_edit = QLineEdit()
        file_name_layout.addRow(file_name_label, file_name_edit)

        content_editor = TextEditor()
        tab_layout.addWidget(content_editor)

        file_name_label.setText(FILE_NAME_TEMPLATE_LABEL_TEXT)

        # 填充数据
        file_name_edit.setText(template_file.file_name_template)
        content_editor.setPlainText(template_file.file_content)

        setattr(tab_widget, 'file_name_edit', file_name_edit)
        setattr(tab_widget, 'content_editor', content_editor)
