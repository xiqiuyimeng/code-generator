# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QListWidgetItem

from src.view.list_widget.list_item_func import set_template_file_data
from src.view.list_widget.list_widget_abc import DraggableListWidgetABC
from src.view.tree.tree_item.tree_item_func import get_item_template_file, get_item_output_config

_author_ = 'luwt'
_date_ = '2023/4/23 16:42'


class TemplateMaintainFileConfigListWidget(DraggableListWidgetABC):
    # 绑定文件数变化信号
    bind_file_changed = pyqtSignal()

    def fill_list_widget(self, unbind_file_list):
        for unbind_file in unbind_file_list:
            file_item = QListWidgetItem(unbind_file.file_name)
            set_template_file_data(file_item, unbind_file)
            self.addItem(file_item)

    def deal_source_list_item_data(self, source_item):
        # 从列表拖拽项到列表中，不需要做任何处理
        pass

    def deal_source_tree_item_data(self, source_item):
        # 从树中拖拽项到列表中
        template_file = get_item_template_file(source_item)
        template_file.output_config_id = None
        # 获取配置数据
        output_config = get_item_output_config(source_item.parent())
        output_config.bind_file_list.remove(template_file)
        self.bind_file_changed.emit()

    def deal_new_list_item_data(self, source_item, new_item):
        # 处理拖拽进来的项数据
        if isinstance(source_item, QTreeWidgetItem):
            template_file = get_item_template_file(source_item)
            set_template_file_data(new_item, template_file)
