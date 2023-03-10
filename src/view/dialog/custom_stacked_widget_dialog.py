# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QStackedWidget, QSpacerItem

from src.constant.type_mapping_dialog_constant import SAVE_DATA_TIPS
from src.view.dialog.name_check_dialog import NameCheckDialog
from src.view.list_widget.abstract_list_widget import AbstractListWidget

_author_ = 'luwt'
_date_ = '2023/2/13 14:47'


class CustomStackedWidgetDialog(NameCheckDialog):
    add_data_signal = ...
    edit_data_signal = ...
    
    def __init__(self, screen_rect, title, item_names, data_id=None):
        # 温馨提示label
        self.save_data_tips_label: QLabel = ...

        # 左侧列表控件
        self.list_widget: AbstractListWidget = ...

        # 堆栈式窗口
        self.stacked_widget: QStackedWidget = ...
        self.stacked_layout: QHBoxLayout = ...

        # 通过是否存在data_id来判断是否需要读取数据库内容，如果存在则为编辑，应该读取数据库
        super().__init__(screen_rect, title, item_names, data_id, data_id is not None)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        """重写构建内容方法，重新设置布局，设置堆栈式窗口"""
        # 温馨提示
        self.save_data_tips_label = QLabel()
        self.save_data_tips_label.setObjectName('tips_label')
        self.frame_layout.addWidget(self.save_data_tips_label)
        # 增加一点间距
        self.frame_layout.addSpacerItem(QSpacerItem(0, 10))

        self.stacked_layout = QHBoxLayout(self.frame)
        self.frame_layout.addLayout(self.stacked_layout)

        self.list_widget = AbstractListWidget(self.frame)
        # 填充左边列表项
        self.fill_list_widget()
        self.list_widget.setCurrentRow(0)
        self.stacked_layout.addWidget(self.list_widget)

        # 创建堆栈式窗口
        self.stacked_widget = QStackedWidget(self.frame)
        self.stacked_layout.addWidget(self.stacked_widget)

        self.stacked_layout.setStretch(0, 3)
        self.stacked_layout.setStretch(1, 20)

        # 填充右侧堆栈式窗口
        self.fill_stacked_widget()

    def fill_list_widget(self): ...

    def fill_stacked_widget(self): ...

    def setup_label_text(self):
        self.save_data_tips_label.setText(SAVE_DATA_TIPS)
        super().setup_label_text()

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def check_data_changed(self) -> bool:
        return True

    def connect_other_signal(self):
        self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        super().connect_other_signal()

    # ------------------------------ 信号槽处理 end ------------------------------ #
