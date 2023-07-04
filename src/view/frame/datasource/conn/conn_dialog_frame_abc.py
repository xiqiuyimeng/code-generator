# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton

from src.constant.ds_dialog_constant import CONN_NAME_TEXT, TEST_CONN_BTN_TEXT, TEST_CONN_BOX_TITLE, \
    SAVE_CONN_BOX_TITLE, QUERY_CONN_BOX_TITLE
from src.constant.help.help_constant import SQL_DS_HELP
from src.service.async_func.async_sql_conn_task import AddConnExecutor, EditConnExecutor, QueryConnInfoExecutor
from src.service.async_func.async_sql_ds_task import TestConnLoadingMaskExecutor
from src.service.system_storage.conn_sqlite import SqlConnection
from src.service.system_storage.conn_type import *
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.frame.datasource.ds_dialog_frame_abc import DsDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/3 13:08'


class ConnDialogFrameABC(DsDialogFrameABC):
    """连接对话框框架抽象类，整体结构应为四部分：标题区、连接名表单区、连接信息表单区、按钮区"""
    save_signal = pyqtSignal(OpenedTreeItem)
    # 修改后的连接名称
    edit_signal = pyqtSignal(str)

    def __init__(self, parent_dialog, dialog_title, exists_conn_names, conn_id):
        self.dialog_data: SqlConnection = ...
        self.new_dialog_data: SqlConnection = ...
        self.conn_type: ConnType = self.get_conn_type()
        self.conn_info: dataclass = ...

        # 测试连接按钮
        self.test_conn_button: QPushButton = ...

        self.test_conn_executor: TestConnLoadingMaskExecutor = ...
        self.add_conn_executor: AddConnExecutor = ...
        self.edit_conn_executor: EditConnExecutor = ...

        super().__init__(parent_dialog, dialog_title.format(self.conn_type.display_name),
                         exists_conn_names, conn_id, placeholder_blank_width=1)

    def get_conn_type(self) -> ConnType:
        ...

    def get_new_dialog_data(self):
        return SqlConnection()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def get_blank_left_buttons(self) -> tuple:
        self.test_conn_button = QPushButton(self)
        self.test_conn_button.setObjectName('test_conn_button')
        return self.test_conn_button,

    def setup_other_label_text(self):
        self.name_label.setText(CONN_NAME_TEXT)
        # 连接信息
        self.setup_conn_info_label_text()
        # 按钮文本
        self.test_conn_button.setText(TEST_CONN_BTN_TEXT)

    def setup_conn_info_label_text(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return SQL_DS_HELP

    def check_input(self):
        super().check_input()
        # 实现测试连接按钮是否可用的逻辑
        if all(dataclasses.astuple(self.conn_info)):
            self.test_conn_button.setDisabled(False)
        else:
            self.test_conn_button.setDisabled(True)

    def collect_input(self):
        self.new_dialog_data.conn_name = self.name_input.text()
        conn_param = self.collect_conn_info_input()
        # 根据参数构建连接信息对象
        self.conn_info = globals()[self.conn_type.type_class](*conn_param)
        self.new_dialog_data.conn_info_type = self.conn_info
        self.new_dialog_data.conn_type = self.conn_type.type

    def collect_conn_info_input(self) -> tuple:
        ...

    def button_available(self) -> bool:
        return self.new_dialog_data.conn_name \
            and all(dataclasses.astuple(self.conn_info)) \
            and self.name_available

    def check_data_changed(self) -> bool:
        self.new_dialog_data.construct_conn_info()
        return self.new_dialog_data != self.dialog_data

    def connect_child_signal(self):
        self.test_conn_button.clicked.connect(self.test_connection)
        # 连接信息相关的信号槽连接
        self.connect_conn_info_signal()

    def test_connection(self):
        self.test_conn_executor = TestConnLoadingMaskExecutor(self.new_dialog_data, self.conn_type,
                                                              self.parent_dialog, self.parent_dialog,
                                                              TEST_CONN_BOX_TITLE)
        self.test_conn_executor.start()

    def connect_conn_info_signal(self):
        ...

    def save_func(self):
        self.new_dialog_data.construct_conn_info()
        # 存在原数据，说明是编辑（当添加连接时， dialog_data = None, 当编辑时，读取数据库，dialog_data = SQLConnection）
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.name_changed = self.new_dialog_data.conn_name != self.dialog_data.conn_name
            self.edit_conn_executor = EditConnExecutor(self.new_dialog_data, self.name_changed,
                                                       self.parent_dialog, self.parent_dialog,
                                                       SAVE_CONN_BOX_TITLE, self.edit_post_process)
            self.edit_conn_executor.start()
        else:
            # 新增操作
            self.add_conn_executor = AddConnExecutor(self.new_dialog_data, self.parent_dialog, self.parent_dialog,
                                                     SAVE_CONN_BOX_TITLE, self.save_post_process)
            self.add_conn_executor.start()

    def save_post_process(self, opened_item_record):
        self.save_signal.emit(opened_item_record)
        self.parent_dialog.close()

    def edit_post_process(self):
        self.edit_signal.emit(self.new_dialog_data.conn_name)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_read_storage_executor(self, callback):
        return QueryConnInfoExecutor(self.dialog_data, self.parent_dialog, self.parent_dialog,
                                     QUERY_CONN_BOX_TITLE, callback)

    def get_old_name(self) -> str:
        return self.dialog_data.conn_name

    # ------------------------------ 后置处理 end ------------------------------ #
