# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QStackedWidget, QSpacerItem

from src.constant.type_mapping_dialog_constant import SAVE_DATA_TIPS
from src.view.frame.frame_func import construct_list_stacked_ui
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/4/3 12:50'


class StackedDialogFrame(NameCheckDialogFrame):
    """堆栈式窗口对话框框架，内置左侧列表与右侧堆栈式窗口"""

    def __init__(self, parent_dialog, title, exits_names, data_id=None):
        # 温馨提示label
        self.save_data_tips_label: QLabel = ...

        # 左侧列表控件
        self.list_widget: ListWidgetABC = ...

        # 堆栈式窗口
        self.stacked_widget: QStackedWidget = ...
        self.stacked_layout: QHBoxLayout = ...

        # 通过是否存在data_id来判断是否需要读取数据库内容，如果存在则为编辑，应该读取数据库
        super().__init__(parent_dialog, title, exits_names, data_id, data_id is not None)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        """重写构建内容方法，重新设置布局，设置堆栈式窗口"""
        # 温馨提示
        self.save_data_tips_label = QLabel()
        self.save_data_tips_label.setObjectName('tips_label')
        self.frame_layout.addWidget(self.save_data_tips_label)
        # 增加一点间距
        self.frame_layout.addSpacerItem(QSpacerItem(0, 10))

        # 构建堆栈式窗口
        construct_list_stacked_ui(ListWidgetABC, self.frame_layout, self, 3, 20)
        # 填充左边列表项
        self.fill_list_widget()
        # 填充右侧堆栈式窗口
        self.fill_stacked_widget()

    def fill_list_widget(self):
        ...

    def fill_stacked_widget(self):
        ...

    def setup_label_text(self):
        self.save_data_tips_label.setText(SAVE_DATA_TIPS)
        super().setup_label_text()

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def check_data_changed(self) -> bool:
        return True

    # ------------------------------ 信号槽处理 end ------------------------------ #
