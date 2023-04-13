# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.type_mapping_dialog_constant import DS_COL_TYPE_BUTTON_TEXT, \
    ADD_TYPE_MAPPING_BUTTON_TEXT, DEL_TYPE_MAPPING_BUTTON_TEXT, DEL_TYPE_MAPPING_PROMPT, DEL_TYPE_MAPPING_BOX_TITLE, \
    BATCH_DEL_TYPE_MAPPING_PROMPT, TYPE_MAPPING_BOX_TITLE
from src.service.async_func.async_type_mapping_task import DelTypeMappingExecutor, BatchDelTypeMappingExecutor, \
    ListTypeMappingExecutor
from src.view.dialog.type_mapping.ds_col_type_dialog import DsColTypeDialog
from src.view.dialog.type_mapping.type_mapping_detail_dialog import TypeMappingDetailDialog
from src.view.frame.table_dialog_frame import TableDialogFrame
from src.view.table.table_widget.type_mapping_table_widget.type_mapping_table_widget import TypeMappingTableWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:39'


class TypeMappingDialogFrame(TableDialogFrame):
    """类型映射表格对话框框架"""

    def __init__(self, parent_dialog, dialog_title):
        # 打开数据列类型对话框按钮
        self.open_ds_col_type_button: QPushButton = ...
        # 列类型列表对话框
        self.ds_col_type_list_dialog: DsColTypeDialog = ...
        super().__init__(parent_dialog, dialog_title, quit_button_row_index=4)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def make_table_widget(self):
        self.table_widget = TypeMappingTableWidget(self.table_frame)

    def setup_first_button(self) -> QPushButton:
        self.open_ds_col_type_button = QPushButton(self)
        return self.open_ds_col_type_button

    def setup_other_label_text(self):
        self.open_ds_col_type_button.setText(DS_COL_TYPE_BUTTON_TEXT)
        self.add_row_button.setText(ADD_TYPE_MAPPING_BUTTON_TEXT)
        self.del_row_button.setText(DEL_TYPE_MAPPING_BUTTON_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_special_signal(self):
        self.open_ds_col_type_button.clicked.connect(self.open_ds_col_type_list_dialog)

    def open_ds_col_type_list_dialog(self):
        """打开数据源列类型对话框"""
        self.ds_col_type_list_dialog = DsColTypeDialog(self.parent_dialog.parent_screen_rect)
        self.ds_col_type_list_dialog.exec()

    def get_row_data_dialog(self, row_id) -> TypeMappingDetailDialog:
        type_mapping_names = list(map(lambda x: x.mapping_name, self.table_widget.cols))
        return TypeMappingDetailDialog(self.parent_dialog.parent_screen_rect, type_mapping_names, row_id)

    def get_del_prompt_title(self):
        return DEL_TYPE_MAPPING_PROMPT, DEL_TYPE_MAPPING_BOX_TITLE

    def get_del_executor(self, row_id, item_name, row_index, del_title) -> DelTypeMappingExecutor:
        return DelTypeMappingExecutor(row_id, item_name, row_index, self.parent_dialog, self.parent_dialog,
                                      del_title, self.table_widget.del_row)

    def get_batch_del_prompt_title(self):
        return BATCH_DEL_TYPE_MAPPING_PROMPT, DEL_TYPE_MAPPING_BOX_TITLE

    def get_batch_del_executor(self, delete_ids, delete_names, del_title) -> BatchDelTypeMappingExecutor:
        return BatchDelTypeMappingExecutor(delete_ids, delete_names, self.parent_dialog, self.parent_dialog,
                                           del_title, self.table_widget.del_rows)

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_list_table_data_executor(self) -> ListTypeMappingExecutor:
        return ListTypeMappingExecutor(self.parent_dialog, self.parent_dialog, TYPE_MAPPING_BOX_TITLE,
                                       self.table_widget.fill_table)

    # ------------------------------ 后置处理 end ------------------------------ #
