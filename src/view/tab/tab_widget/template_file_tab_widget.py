# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QTabWidget

from src.view.list_widget.list_item_func import get_template_file_data
from src.view.tab.tab_bar.tab_bar import AbstractTabBar

_author_ = 'luwt'
_date_ = '2023/3/13 11:29'


class TemplateFileTabWidget(QTabWidget):

    def __init__(self, file_list_widget, *args):
        super().__init__(*args)
        self.file_list_widget = file_list_widget
        self.setTabBar(AbstractTabBar(self))

    def removeTab(self, index: int):
        """重写删除tab方法，在删除时，将tab页数据刷入模板文件对象"""
        # 一定能找到tab对应的列表项
        list_index = tuple(filter(lambda x: self.tabText(index) == self.file_list_widget.item(x).text(),
                                  range(self.file_list_widget.count())))[0]
        list_item = self.file_list_widget.item(list_index)
        template_file_data = get_template_file_data(list_item)
        # 将tab页内保存的文本数据刷入对象中
        template_file_data.file_content = self.widget(index).toPlainText()
        super().removeTab(index)
