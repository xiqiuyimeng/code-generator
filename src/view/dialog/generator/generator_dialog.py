# -*- coding: utf-8 -*-

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.constant.generator_dialog_constant import SQL_CONFIRM_SELECTED_HEADER_TXT, \
    STRUCT_CONFIRM_SELECTED_HEADER_TXT, SELECT_TYPE_MAPPING_HEADER_TXT, SELECT_TEMPLATE_HEADER_TXT, \
    FILL_TEMPLATE_CONFIG_HEADER_TXT
from src.service.system_storage.template_sqlite import Template
from src.service.system_storage.type_mapping_sqlite import TypeMapping
from src.service.util.tree_node import TreeData
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.frame.generator.select_list.select_template_dialog_frame import SelectTemplateDialogFrame
from src.view.frame.generator.select_list.select_type_mapping_dialog_frame import SelectTypeMappingDialogFrame
from src.view.frame.generator.selected_data.selected_data_dialog_frame_abc import SelectedDataDialogFrameABC
from src.view.frame.generator.selected_data.sql_selected_data_dialog_frame import SqlSelectedDataDialogFrame
from src.view.frame.generator.selected_data.struct_selected_data_dialog_frame import StructSelectedDataDialogFrame
from src.view.frame.generator.dynamic_template_config_dialog_frame import DynamicTemplateConfigDialogFrame

_author_ = 'luwt'
_date_ = '2022/10/31 11:47'


class GeneratorDialog(CustomDialogABC):
    """生成器对话框，点击生成后弹出的对话框，完成数据确认 -> 选择类型映射 -> 选择模板 -> 填充模板配置 -> 生成"""

    def __init__(self, ds_category, selected_data: TreeData, *args):
        # 选中数据展示页框架
        self.frame: ChainDialogFrameABC = ...
        self.ds_category = ds_category
        # 页面数据
        self.selected_data: TreeData = selected_data
        self.type_mapping: TypeMapping = ...
        self.template: Template = ...
        self.template_config_dict: dict = ...
        super().__init__(*args)

        # 选择类型映射框架
        self.select_type_mapping_frame: SelectTypeMappingDialogFrame = ...
        # 选择模板框架
        self.select_template_frame: SelectTemplateDialogFrame = ...
        # 动态模板配置框架
        self.dynamic_template_config_frame: DynamicTemplateConfigDialogFrame = ...

        # 构建调用链
        self.setup_frame_chain()
        self.connect_frame_signal()

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.setFixedSize(self.parent_screen_rect.width() * 0.8, self.parent_screen_rect.height() * 0.8)

    def get_frame(self) -> SelectedDataDialogFrameABC:
        # 根据类型判断，展示为sql还是结构体对话框框架
        if self.ds_category == SQL_DS_CATEGORY:
            return SqlSelectedDataDialogFrame(self.selected_data, self.dialog_layout,
                                              self, SQL_CONFIRM_SELECTED_HEADER_TXT)
        elif self.ds_category == STRUCT_DS_CATEGORY:
            return StructSelectedDataDialogFrame(self.selected_data, self.dialog_layout,
                                                 self, STRUCT_CONFIRM_SELECTED_HEADER_TXT)

    def setup_frame_chain(self):
        # 类型映射框架
        self.select_type_mapping_frame = SelectTypeMappingDialogFrame(self.dialog_layout, self,
                                                                      SELECT_TYPE_MAPPING_HEADER_TXT)
        self.frame.set_next_frame(self.select_type_mapping_frame)
        self.select_type_mapping_frame.set_previous_frame(self.frame)

        # 模板框架
        self.select_template_frame = SelectTemplateDialogFrame(self.dialog_layout, self, SELECT_TEMPLATE_HEADER_TXT)
        self.select_type_mapping_frame.set_next_frame(self.select_template_frame)
        self.select_template_frame.set_previous_frame(self.select_type_mapping_frame)

        # 动态模板配置框架
        self.dynamic_template_config_frame = DynamicTemplateConfigDialogFrame(self.dialog_layout, self,
                                                                              FILL_TEMPLATE_CONFIG_HEADER_TXT,
                                                                              get_template_func=self.get_template)
        self.select_template_frame.set_next_frame(self.dynamic_template_config_frame)
        self.dynamic_template_config_frame.set_previous_frame(self.select_template_frame)

        # 生成页面框架

    def connect_frame_signal(self):
        self.select_type_mapping_frame.data_changed_signal.connect(self.set_type_mapping)
        self.select_template_frame.data_changed_signal.connect(self.set_template)

    def set_type_mapping(self, type_mapping):
        self.type_mapping = type_mapping

    def set_template(self, template):
        self.template = template

    def get_template(self):
        return self.template
