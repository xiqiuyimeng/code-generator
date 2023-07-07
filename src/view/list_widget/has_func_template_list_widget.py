# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QListWidgetItem

from src.view.list_widget.list_item_func import set_template_data, get_template_data
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/26 10:49'


class HasFuncTemplateListWidget(ListWidgetABC):

    def __init__(self, parent, switch_frame_func):
        self.switch_frame_func = switch_frame_func
        super().__init__(parent)

    def connect_signal(self):
        # 支持双击
        self.doubleClicked.connect(self.double_clicked)

    def double_clicked(self, index):
        item = self.itemFromIndex(index)
        # 取出模板对象
        template = get_template_data(item)
        self.switch_frame_func(template.id, template.template_name)

    def fill_list_widget(self, template_list):
        for template in template_list:
            item = QListWidgetItem(template.template_name)
            set_template_data(item, template)
            self.addItem(item)
