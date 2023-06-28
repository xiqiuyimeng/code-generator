# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QFrame, QVBoxLayout, QGridLayout

from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.box.message_box import pop_question
from src.view.dialog.custom_dialog_abc import StackedDialogABC
from src.view.dialog.export_dialog import ExportDialog
from src.view.dialog.import_dialog import ImportDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.table.table_widget.custom_export_table_widget import CustomCopyExportTableWidget

_author_ = 'luwt'
_date_ = '2023/3/8 13:27'


class TableDialogFrame(DialogFrameABC):
    """通用表格对话框框架，包含一个主体展示表格及相关操作按钮"""

    def __init__(self, *args, **kwargs):
        # 表格主体框架
        self.table_frame: QFrame = ...
        self.table_frame_layout: QVBoxLayout = ...
        # 操作表格按钮布局
        self.operation_table_btn_layout: QGridLayout = ...
        # 添加新行按钮
        self.add_row_button: QPushButton = ...
        # 删除行按钮
        self.del_row_button: QPushButton = ...
        # 复制行按钮
        self.copy_row_button: QPushButton = ...
        # 导入按钮
        self.import_button: QPushButton = ...
        # 导出按钮
        self.export_button: QPushButton = ...
        # 主体表格
        self.table_widget: CustomCopyExportTableWidget = ...
        # 读取表格数据列表执行器
        self.list_table_data_executor: LoadingMaskThreadExecutor = ...
        # 删除行数据执行器
        self.del_row_data_executor: LoadingMaskThreadExecutor = ...
        # 批量删除行数据执行器
        self.batch_del_row_data_executor: LoadingMaskThreadExecutor = ...
        # 复制行数据执行器
        self.copy_row_data_executor: LoadingMaskThreadExecutor = ...
        # 行具体信息对话框
        self.row_data_dialog: StackedDialogABC = ...
        # 导入数据对话框
        self.import_rows_dialog: ImportDialog = ...
        # 导出数据对话框
        self.export_rows_dialog: ExportDialog = ...
        super().__init__(*args, **kwargs)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 类型映射表格
        self.table_frame = QFrame(self)
        self.table_frame_layout = QVBoxLayout(self.table_frame)
        # 将表格布局边距清空
        self.table_frame_layout.setContentsMargins(0, 0, 0, 0)
        # 操作按钮组
        self.operation_table_btn_layout = QGridLayout(self.table_frame)
        self.setup_operation_button()
        self.table_frame_layout.addLayout(self.operation_table_btn_layout)
        # 创建表格
        self.make_table_widget()
        self.table_frame_layout.addWidget(self.table_widget)
        self.frame_layout.addWidget(self.table_frame)

    def setup_operation_button(self):
        first_operation_button = self.setup_first_button()
        self.operation_table_btn_layout.addWidget(first_operation_button, 0, 0, 1, 1)
        self.add_row_button = QPushButton(self)
        self.add_row_button.setObjectName('create_row_button')
        self.operation_table_btn_layout.addWidget(self.add_row_button, 0, 1, 1, 1)
        self.del_row_button = QPushButton()
        self.del_row_button.setObjectName('del_row_button')
        self.operation_table_btn_layout.addWidget(self.del_row_button, 0, 2, 1, 1)
        self.copy_row_button = QPushButton(self)
        self.copy_row_button.setObjectName('copy_row_button')
        self.operation_table_btn_layout.addWidget(self.copy_row_button, 0, 3, 1, 1)
        self.setup_import_export_button()

    def setup_first_button(self) -> QPushButton:
        ...

    def setup_import_export_button(self):
        self.import_button = QPushButton(self)
        self.import_button.setObjectName('import_button')
        self.operation_table_btn_layout.addWidget(self.import_button, 0, 4, 1, 1)
        self.export_button = QPushButton(self)
        self.export_button.setObjectName('export_button')
        self.operation_table_btn_layout.addWidget(self.export_button, 0, 5, 1, 1)

    def make_table_widget(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        # 添加行按钮点击，打开添加行对话框
        self.add_row_button.clicked.connect(lambda: self.open_row_data_dialog())
        # 连接表格中行编辑信号
        self.table_widget.row_edit_signal.connect(self.open_row_data_dialog)
        # 连接表格中行删除信号
        self.table_widget.row_del_signal.connect(self.del_row)
        # 连接表格中行复制信号
        self.table_widget.row_copy_signal.connect(self.copy_row)
        # 连接表格中行导出信号
        self.table_widget.row_export_signal.connect(self.export_row)
        # 连接表头复选框状态变化信号
        self.table_widget.header_widget.header_check_changed.connect(self.set_button_available)
        # 删除行按钮点击信号
        self.del_row_button.clicked.connect(self.del_rows)
        # 复制行按钮点击信号
        self.copy_row_button.clicked.connect(self.copy_rows)
        # 导入按钮
        self.import_button.clicked.connect(self.import_rows)
        # 导出按钮
        self.export_button.clicked.connect(self.export_rows)
        # 子类的其他信号
        self.connect_special_signal()

    def connect_special_signal(self):
        ...

    def open_row_data_dialog(self, row_id=None, row_index=None):
        """打开添加或编辑行数据对话框"""
        self.row_data_dialog = self.get_row_data_dialog(row_id=row_id, row_index=row_index)
        self.row_data_dialog.exec()

    def get_row_data_dialog(self, row_id=None, row_index=None, row_data=None) -> StackedDialogABC:
        row_data_dialog: StackedDialogABC = self.do_get_row_data_dialog(row_id)
        if row_id:
            row_data_dialog.edit_signal.connect(lambda data: self.table_widget.edit_row(row_index, data))
        else:
            # 如果 row_data 存在，那应该是用于导入时，处理异常数据，所以需要手动回显数据
            # 子类框架需要设置 import_error_data 标记，并将其用于判断是否是异常数据回显
            if row_data:
                row_data_dialog.frame.dialog_data = row_data
                row_data_dialog.frame.import_error_data = True
                row_data_dialog.frame.setup_echo_data()
            else:
                row_data_dialog.save_signal.connect(self.table_widget.add_row)
        return row_data_dialog

    def do_get_row_data_dialog(self, row_id) -> StackedDialogABC:
        ...

    def del_row(self, row_id, row_index, item_name):
        del_prompt, del_title = self.get_del_prompt_title()
        if not pop_question(del_prompt.format(item_name), del_title, self):
            return
        self.del_row_data_executor = self.get_del_executor(row_id, item_name, row_index, del_title)
        self.del_row_data_executor.start()

    def get_del_prompt_title(self) -> tuple:
        ...

    def get_del_executor(self, row_id, item_name, row_index, del_title) -> LoadingMaskThreadExecutor:
        ...

    def copy_row(self, row_id):
        self.do_copy_rows((row_id,))

    def export_row(self, row_id):
        self.do_export_rows((row_id,))

    def set_button_available(self, checked):
        # 如果表格存在行，删除按钮、导出按钮和复制按钮状态根据传入状态变化，否则应该置为不可用
        if self.table_widget.rowCount():
            self.del_row_button.setDisabled(not checked)
            self.copy_row_button.setDisabled(not checked)
            self.export_button.setDisabled(not checked)
        else:
            self.del_row_button.setDisabled(True)
            self.copy_row_button.setDisabled(True)
            self.export_button.setDisabled(True)

    def del_rows(self):
        # 收集所有选中项数据，进行删除
        delete_ids, delete_names = self.table_widget.get_all_checked_id_names()
        batch_del_prompt, batch_del_title = self.get_batch_del_prompt_title()
        if not pop_question(batch_del_prompt.format(len(delete_ids)), batch_del_title, self):
            return
        self.batch_del_row_data_executor = self.get_batch_del_executor(delete_ids, delete_names, batch_del_title)
        self.batch_del_row_data_executor.start()

    def get_batch_del_prompt_title(self) -> tuple:
        ...

    def get_batch_del_executor(self, delete_ids, delete_names, del_title) -> LoadingMaskThreadExecutor:
        ...

    def copy_rows(self):
        # 收集所有选中项id
        checked_ids = self.table_widget.get_all_checked_id_names()[0]
        self.do_copy_rows(checked_ids)

    def do_copy_rows(self, row_ids):
        self.copy_row_data_executor = self.get_copy_executor(row_ids)
        self.copy_row_data_executor.start()

    def get_copy_executor(self, copy_row_ids) -> LoadingMaskThreadExecutor:
        ...

    def import_rows(self):
        # 打开导入对话框
        self.import_rows_dialog = self.get_import_dialog(self.import_success_callback, self.get_row_data_dialog)
        self.import_rows_dialog.exec()

    def get_import_dialog(self, import_success_callback, get_row_data_dialog) -> ImportDialog:
        ...

    def import_success_callback(self, add_data_list, del_data_list=None):
        if del_data_list:
            self.table_widget.del_duplicate_rows(del_data_list)
        self.table_widget.add_rows(add_data_list)

    def export_rows(self):
        # 收集所有选中项id
        checked_ids = self.table_widget.get_all_checked_id_names()[0]
        self.do_export_rows(checked_ids)

    def do_export_rows(self, row_ids):
        # 打开导出对话框
        self.export_rows_dialog = self.get_export_dialog(row_ids)
        self.export_rows_dialog.exec()

    def get_export_dialog(self, row_ids) -> ExportDialog:
        ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_table_data_executor = self.get_list_table_data_executor()
        self.list_table_data_executor.start()
        # 设置删除行按钮初始状态
        self.init_del_button_status()

    def get_list_table_data_executor(self) -> LoadingMaskThreadExecutor:
        ...

    def init_del_button_status(self):
        # 初始化按钮状态
        self.set_button_available(False)

    # ------------------------------ 后置处理 end ------------------------------ #
