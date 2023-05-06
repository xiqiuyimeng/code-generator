# -*- coding: utf-8 -*-

from src.constant.generator_dialog_constant import RESELECT_BTN_TXT, CHOOSE_TYPE_MAPPING_BTN_TXT
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.tree.tree_widget.tree_widget_abc import DisplayTreeWidget

_author_ = 'luwt'
_date_ = '2023/4/4 11:34'


class SelectedDataDialogFrameABC(ChainDialogFrameABC):
    """选中数据展示对话框框架抽象类，主体为展示树结构"""
    def __init__(self, *args):
        # 选中数据展示树结构
        self.display_tree_widget = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 展示树结构
        self.display_tree_widget = DisplayTreeWidget(self)
        self.setup_tree_ui()
        self.display_tree_widget.expandAll()
        self.frame_layout.addWidget(self.display_tree_widget)

    def setup_tree_ui(self): ...

    def setup_other_label_text(self):
        self.previous_frame_button.setText(RESELECT_BTN_TXT)
        self.next_frame_button.setText(CHOOSE_TYPE_MAPPING_BTN_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #
