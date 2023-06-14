# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QStackedWidget, QHBoxLayout

from src.constant.help.help_constant import HELP_TYPE_TUPLE
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.frame.frame_func import construct_list_stacked_ui
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/6/13 11:40'


class HelpDialogFrame(DialogFrameABC):
    """帮助对话框框架"""

    def __init__(self, help_info_type, *args):
        # 当前查看的帮助信息类型
        self.help_info_type = help_info_type
        # 存储帮助信息对应的类型集合
        self.help_info_type_tuple = HELP_TYPE_TUPLE
        # 左侧列表控件
        self.list_widget: ListWidgetABC = ...
        # 堆栈式窗口
        self.stacked_widget: QStackedWidget = ...
        self.stacked_layout: QHBoxLayout = ...
        super().__init__(*args, placeholder_blank_width=3, need_help_button=False)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 构建堆栈式窗口
        construct_list_stacked_ui(ListWidgetABC, self.frame_layout, self, 1, 5)
        # 填充左边列表项
        self.fill_list_widget()
        # 填充右侧堆栈式窗口
        self.fill_stacked_widget()

    def fill_list_widget(self):
        self.list_widget.fill_list_widget(self.help_info_type_tuple)

    def fill_stacked_widget(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 根据当前传进来的帮助信息类型决定展示哪一页
        self.list_widget.setCurrentRow(self.help_info_type_tuple.index(self.help_info_type))

    # ------------------------------ 后置处理 end ------------------------------ #
