# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QTreeWidgetItem

from src.constant.help.help_constant import TEMPLATE_FILE_OUTPUT_CONFIG_HELP
from src.constant.template_dialog_constant import OUTPUT_CONFIG_LIST_HEADER_TEXT, FILE_LIST_HEADER_TEXT
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.list_widget.template_maintain_file_config_list_widget import TemplateMaintainFileConfigListWidget
from src.view.tree.tree_item.tree_item_func import set_item_output_config, set_item_template_file
from src.view.tree.tree_widget.template_config_tree_widget import TemplateOutputConfigTreeWidget

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
        self.config_tree_widget: TemplateOutputConfigTreeWidget = ...
        self.file_layout: QVBoxLayout = ...
        self.file_header_label: QLabel = ...
        self.file_list_widget: TemplateMaintainFileConfigListWidget = ...
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
        self.config_tree_widget = TemplateOutputConfigTreeWidget(self)
        self.config_layout.addWidget(self.config_tree_widget)
        # 填充数据
        self.fill_config_tree_widget()

        # 右侧文件列表
        self.file_layout = QVBoxLayout()
        self._layout.addLayout(self.file_layout)
        self.file_header_label = QLabel()
        self.file_layout.addWidget(self.file_header_label)
        self.file_list_widget = TemplateMaintainFileConfigListWidget(self)
        self.file_layout.addWidget(self.file_list_widget)
        # 填充数据
        self.file_list_widget.fill_list_widget(self.unbind_file_list)

    def fill_config_tree_widget(self):
        # 添加配置树列表数据
        for config in self.output_config_list:
            config_item = QTreeWidgetItem(self.config_tree_widget)
            config_item.setText(0, config.config_name)
            # 保存配置数据
            set_item_output_config(config_item, config)
            self.config_tree_widget.addTopLevelItem(config_item)
            # 处理已绑定的文件列表数据
            if config.bind_file_list:
                for bind_file in config.bind_file_list:
                    bind_file_item = QTreeWidgetItem(config_item)
                    bind_file_item.setText(0, bind_file.file_name)
                    # 保存模板文件
                    set_item_template_file(bind_file_item, bind_file)
        self.config_tree_widget.expandAll()

    def setup_other_label_text(self):
        self.config_header_label.setText(OUTPUT_CONFIG_LIST_HEADER_TEXT)
        self.file_header_label.setText(FILE_LIST_HEADER_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_FILE_OUTPUT_CONFIG_HELP

    # ------------------------------ 信号槽处理 end ------------------------------ #
