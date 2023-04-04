# -*- coding: utf-8 -*-

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.constant.generator_dialog_constant import SQL_CONFIRM_SELECTED_HEADER_TXT, \
    STRUCT_CONFIRM_SELECTED_HEADER_TXT, SELECT_TYPE_MAPPING_HEADER_TXT, SELECT_TEMPLATE_HEADER_TXT
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.frame.generator.select_template_dialog_frame import SelectTemplateDialogFrame
from src.view.frame.generator.select_type_mapping_dialog_frame import SelectTypeMappingDialogFrame
from src.view.frame.generator.selected_data.selected_data_dialog_frame_abc import SelectedDataDialogFrameABC
from src.view.frame.generator.selected_data.sql_selected_data_dialog_frame import SqlSelectedDataDialogFrame
from src.view.frame.generator.selected_data.struct_selected_data_dialog_frame import StructSelectedDataDialogFrame

_author_ = 'luwt'
_date_ = '2022/10/31 11:47'


class GeneratorDialog(CustomDialogABC):
    """生成器对话框，点击生成后弹出的对话框，完成数据确认 -> 选择类型映射 -> 选择模板 -> 填充模板配置 -> 生成"""

    def __init__(self, ds_category, selected_data, *args):
        self.frame: ChainDialogFrameABC = ...
        self.ds_category = ds_category
        self.selected_data = selected_data
        super().__init__(*args)

        # 选择类型映射框架
        self.select_type_mapping_frame: SelectTypeMappingDialogFrame = ...
        # 选择模板框架
        self.select_template_frame: SelectTemplateDialogFrame = ...

        # 构建调用链
        self.setup_frame_chain()

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
