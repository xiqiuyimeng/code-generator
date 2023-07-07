# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QListWidgetItem, QTreeWidgetItem

from src.view.custom_widget.item_view_abc import DraggableItemViewABC
from src.view.list_widget.list_item_func import get_template_file_data
from src.view.tree.tree_item.tree_item_func import get_item_output_config, get_item_template_file, \
    set_item_template_file
from src.view.tree.tree_widget.tree_widget_abc import DisplayTreeWidget

_author_ = 'luwt'
_date_ = '2023/4/23 9:01'


class TemplateOutputConfigTreeWidget(DisplayTreeWidget, DraggableItemViewABC):
    # 绑定文件数变化信号
    bind_file_changed = pyqtSignal()

    def deal_source_list_item_data(self, source_item):
        # 从列表中拖拽项到树中
        template_file = get_template_file_data(source_item)
        # 设置一个虚拟配置id即可
        template_file.output_config_id = -1

    def deal_source_tree_item_data(self, source_item):
        # 从树中拖拽项到树中
        output_config = get_item_output_config(source_item.parent())
        template_file = get_item_template_file(source_item)
        output_config.bind_file_list.remove(template_file)

    def deal_new_tree_item_data(self, source_item, new_item):
        # 处理拖拽进来的项数据
        # 获取配置数据
        output_config = get_item_output_config(new_item.parent())
        if output_config.bind_file_list is None:
            output_config.bind_file_list = list()
        # 处理文件数据
        if isinstance(source_item, QListWidgetItem):
            template_file = get_template_file_data(source_item)
            set_item_template_file(new_item, template_file)
            output_config.bind_file_list.append(template_file)
        elif isinstance(source_item, QTreeWidgetItem):
            template_file = get_item_template_file(source_item)
            set_item_template_file(new_item, template_file)
            output_config.bind_file_list.append(template_file)
        self.bind_file_changed.emit()
