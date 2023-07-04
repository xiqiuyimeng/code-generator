# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidgetItem

from src.constant.icon_enum import get_icon
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/2/13 16:04'


class DsTypeListWidget(ListWidgetABC):

    def fill_list_widget(self, ds_types):
        # 渲染页面
        if ds_types:
            for ds_type in ds_types:
                item = QListWidgetItem()
                item.setText(ds_type)
                item.setIcon(get_icon(ds_type))
                self.addItem(item)
