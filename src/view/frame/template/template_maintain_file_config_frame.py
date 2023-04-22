# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel

from src.constant.template_dialog_constant import OUTPUT_CONFIG_LIST_HEADER_TEXT, FILE_LIST_HEADER_TEXT
from src.view.frame.dialog_frame_abc import DialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/22 12:39'


class TemplateMaintainFileConfigFrame(DialogFrameABC):
    """模板维护文件和输出配置关系的对话框框架"""

    def __init__(self, output_config_list, unbind_file_list, *args):
        self.output_config_list = output_config_list
        self.unbind_file_list = unbind_file_list
        self._layout: QHBoxLayout = ...
        self.config_layout: QVBoxLayout = ...
        self.config_header_label: QLabel = ...
        self.config_tree_widget = ...
        self.file_layout: QVBoxLayout = ...
        self.file_header_label: QLabel = ...
        self.file_list_widget = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self._layout = QHBoxLayout()
        self.frame_layout.addLayout(self._layout)
        # 左侧配置树结构
        self.config_layout = QVBoxLayout()
        self._layout.addLayout(self.config_layout)
        self.config_header_label = QLabel()
        self.config_layout.addWidget(self.config_header_label)
        # 右侧文件列表
        self.file_layout = QVBoxLayout()
        self._layout.addLayout(self.file_layout)
        self.file_header_label = QLabel()
        self.file_layout.addWidget(self.file_header_label)

    def setup_other_label_text(self):
        self.config_header_label.setText(OUTPUT_CONFIG_LIST_HEADER_TEXT)
        self.file_header_label.setText(FILE_LIST_HEADER_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #
