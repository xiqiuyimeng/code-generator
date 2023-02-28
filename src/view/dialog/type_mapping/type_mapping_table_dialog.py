# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QFrame, QVBoxLayout

from src.constant.type_mapping_dialog_constant import TYPE_MAPPING_LIST_TITLE, DS_COL_TYPE_BUTTON_TEXT, \
    ADD_TYPE_MAPPING_BUTTON_TEXT, DEL_TYPE_MAPPING_BOX_TITLE, DEL_TYPE_MAPPING_PROMPT, TYPE_MAPPING_BOX_TITLE, \
    DEL_TYPE_MAPPING_BUTTON_TEXT, BATCH_DEL_TYPE_MAPPING_PROMPT
from src.service.async_func.async_type_mapping_task import ListTypeMappingExecutor, DelTypeMappingExecutor, \
    BatchDelTypeMappingExecutor
from src.view.box.message_box import pop_question
from src.view.dialog.custom_dialog import CustomDialog
from src.view.dialog.type_mapping.ds_col_type_dialog import DsColTypeDialog
from src.view.dialog.type_mapping.type_mapping_dialog import TypeMappingDetailDialog
from src.view.table.table_widget.type_mapping_table_widget.type_mapping_table_widget import TypeMappingTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 10:03'


class TypeMappingListTableDialog(CustomDialog):
    """类型映射列表对话框"""

    def __init__(self, screen_rect):
        self.table_frame: QFrame = ...
        self.table_frame_layout: QVBoxLayout = ...
        # 类型映射表格
        self.type_mapping_table_widget: TypeMappingTableWidget = ...
        # 打开数据列类型对话框按钮
        self.open_ds_col_type_button: QPushButton = ...
        # 添加新的类型映射按钮
        self.add_type_mapping_button: QPushButton = ...
        # 删除类型映射按钮
        self.del_type_mapping_button: QPushButton = ...
        # 读取类型映射列表执行器
        self.list_type_mapping_executor: ListTypeMappingExecutor = ...
        # 列类型列表对话框
        self.ds_col_type_list_dialog: DsColTypeDialog = ...
        # 删除类型映射执行器
        self.del_type_mapping_executor: DelTypeMappingExecutor = ...
        # 批量删除执行器
        self.batch_del_type_mapping_executor: BatchDelTypeMappingExecutor = ...
        # 类型映射列信息对话框
        self.type_mapping_dialog: TypeMappingDetailDialog = ...
        super().__init__(screen_rect, TYPE_MAPPING_LIST_TITLE, quit_button_row_index=4)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def setup_content_ui(self):
        # 类型映射表格
        self.table_frame = QFrame(self.frame)
        self.table_frame_layout = QVBoxLayout(self.table_frame)
        # 将表格布局边距清空
        self.table_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.type_mapping_table_widget = TypeMappingTableWidget(self.table_frame)
        self.table_frame_layout.addWidget(self.type_mapping_table_widget)
        self.frame_layout.addWidget(self.table_frame)

    def setup_other_button(self):
        self.open_ds_col_type_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.open_ds_col_type_button, 0, 0, 1, 1)
        self.add_type_mapping_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.add_type_mapping_button, 0, 1, 1, 1)

        self.button_layout.addWidget(self.placeholder_blank, 0, 2, 1, 1)
        self.del_type_mapping_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.del_type_mapping_button, 0, 3, 1, 1)

    def setup_other_label_text(self):
        self.open_ds_col_type_button.setText(DS_COL_TYPE_BUTTON_TEXT)
        self.add_type_mapping_button.setText(ADD_TYPE_MAPPING_BUTTON_TEXT)
        self.del_type_mapping_button.setText(DEL_TYPE_MAPPING_BUTTON_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.open_ds_col_type_button.clicked.connect(self.open_ds_col_type_list_dialog)
        self.add_type_mapping_button.clicked.connect(lambda: self.open_type_mapping_col_dialog())
        # 连接表格中行编辑信号
        self.type_mapping_table_widget.row_edit_signal.connect(self.open_type_mapping_col_dialog)
        # 连接表格中行删除信号
        self.type_mapping_table_widget.row_del_signal.connect(self.del_type_mapping)
        # 连接表头复选框状态变化信号
        self.type_mapping_table_widget.header_widget.header_check_changed.connect(self.set_del_btn_available)
        # 删除类型映射按钮信号
        self.del_type_mapping_button.clicked.connect(self.del_type_mappings)

    def open_ds_col_type_list_dialog(self):
        """打开数据源列类型对话框"""
        self.ds_col_type_list_dialog = DsColTypeDialog(self.parent_screen_rect)
        self.ds_col_type_list_dialog.exec()

    def open_type_mapping_col_dialog(self, type_mapping_id=None, row_index=None):
        """打开类型映射信息对话框"""
        type_mapping_names = list(map(lambda x: x.mapping_name, self.type_mapping_table_widget.cols))
        self.type_mapping_dialog = TypeMappingDetailDialog(self.parent_screen_rect,
                                                           type_mapping_names, type_mapping_id)
        if type_mapping_id:
            edit_slot_func = self.type_mapping_table_widget.edit_row
            self.type_mapping_dialog.edit_type_mapping_signal.connect(lambda type_mapping:
                                                                      edit_slot_func(type_mapping, row_index))
        else:
            self.type_mapping_dialog.add_type_mapping_signal.connect(self.type_mapping_table_widget.add_row)
        self.type_mapping_dialog.exec()

    def del_type_mapping(self, type_mapping_id, row_index, type_mapping_name):
        if not pop_question(DEL_TYPE_MAPPING_PROMPT.format(type_mapping_name), DEL_TYPE_MAPPING_BOX_TITLE, self):
            return
        self.del_type_mapping_executor = DelTypeMappingExecutor(type_mapping_id, type_mapping_name, row_index,
                                                                self, self, DEL_TYPE_MAPPING_BOX_TITLE,
                                                                self.type_mapping_table_widget.del_row)
        self.del_type_mapping_executor.start()

    def set_del_btn_available(self, checked):
        self.del_type_mapping_button.setDisabled(not checked)

    def del_type_mappings(self):
        # 收集所有选中项数据，进行删除
        delete_ids, delete_names = self.type_mapping_table_widget.get_all_checked_id_names()
        if not pop_question(BATCH_DEL_TYPE_MAPPING_PROMPT.format(len(delete_ids)),
                            DEL_TYPE_MAPPING_BOX_TITLE, self):
            return
        self.batch_del_type_mapping_executor = BatchDelTypeMappingExecutor(delete_ids, delete_names, self, self,
                                                                           DEL_TYPE_MAPPING_BOX_TITLE,
                                                                           self.type_mapping_table_widget.del_rows)
        self.batch_del_type_mapping_executor.start()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_type_mapping_executor = ListTypeMappingExecutor(self, self, TYPE_MAPPING_BOX_TITLE,
                                                                  self.type_mapping_table_widget.fill_table)
        self.list_type_mapping_executor.start()
        # 设置删除类型映射按钮初始状态
        self.init_del_button_status()

    def init_del_button_status(self):
        # 设置删除按钮状态，初始不可用
        self.set_del_btn_available(False)

    # ------------------------------ 后置处理 end ------------------------------ #
