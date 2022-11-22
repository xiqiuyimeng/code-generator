# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QPushButton

from constant.constant import CONN_NAME_TEXT, TEST_CONN_BTN_TEXT
from service.async_func.async_sql_conn_task import AddConnExecutor, EditConnExecutor
from service.async_func.async_sql_ds_task import TestConnLoadingMaskExecutor
from service.system_storage.conn_sqlite import SqlConnection
from service.system_storage.conn_type import *
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from view.dialog.datasource.abstract_ds_dialog import AbstractDsInfoDialog

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class AbstractConnDialog(AbstractDsInfoDialog):
    """连接对话框抽象类，整体对话框结构应为四部分：标题区、连接名表单区、连接信息表单区、按钮区"""

    conn_saved = pyqtSignal(SqlConnection, OpenedTreeItem)
    # 第一个元素为修改后的连接对象，第二个元素为名称是否变化
    conn_changed = pyqtSignal(SqlConnection, bool)

    def __init__(self, connection: SqlConnection, dialog_title, screen_rect, conn_name_id_dict):
        self.dialog_data: SqlConnection = ...
        self.new_dialog_data: SqlConnection = ...
        self.conn_type: ConnType = self.get_conn_type()
        self.conn_info: dataclass = ...

        # 连接信息表单布局
        self.test_conn_button: QPushButton = ...

        self.test_conn_executor: TestConnLoadingMaskExecutor = ...
        self.add_conn_executor: AddConnExecutor = ...
        self.edit_conn_executor: EditConnExecutor = ...

        super().__init__(connection, dialog_title, screen_rect, conn_name_id_dict)

    def get_new_dialog_data(self):
        return SqlConnection()

    def get_old_name(self) -> str:
        return self.dialog_data.conn_name

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.4, self.parent_screen_rect.height() * 0.5)

    def get_conn_type(self) -> ConnType: ...

    def setup_other_button(self):
        # 按钮部分
        self.test_conn_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.test_conn_button, 0, 0, 1, 1)

    def setup_other_label_text(self):
        self.title.setText(self.dialog_title.format(self.conn_type.display_name))
        self.name_label.setText(CONN_NAME_TEXT)
        # 连接信息
        self.setup_conn_info_label()
        # 按钮文本
        self.test_conn_button.setText(TEST_CONN_BTN_TEXT)

    def setup_conn_info_label(self): ...

    def button_available(self) -> bool:
        return self.new_dialog_data.conn_name \
                and all(dataclasses.astuple(self.conn_info)) \
                and self.name_available

    def collect_input(self):
        self.new_dialog_data.conn_name = self.name_input.text()
        conn_param = self.collect_conn_info_input()
        # 根据参数构建连接信息对象
        self.conn_info = globals()[self.conn_type.type_class](*conn_param)
        self.new_dialog_data.conn_info_type = self.conn_info
        self.new_dialog_data.conn_type = self.conn_type.type

    def collect_conn_info_input(self) -> tuple: ...

    def init_other_button_status(self):
        self.test_conn_button.setDisabled(True)

    def set_other_button_available(self):
        self.test_conn_button.setDisabled(False)

    def connect_child_signal(self):
        self.test_conn_button.clicked.connect(self.test_connection)
        # 连接信息相关的信号槽连接
        self.connect_conn_info_signal()

    def connect_conn_info_signal(self): ...

    def test_connection(self):
        self.test_conn_executor = TestConnLoadingMaskExecutor(self.new_dialog_data, self, self)
        self.test_conn_executor.start()

    def save_func(self):
        self.new_dialog_data.construct_conn_info()
        # 存在id，说明是编辑
        if self.dialog_data.id:
            if self.new_dialog_data != self.dialog_data:
                self.new_dialog_data.id = self.dialog_data.id
                self.name_changed = self.new_dialog_data.conn_name != self.dialog_data.conn_name
                self.edit_conn_executor = EditConnExecutor(self.new_dialog_data, self, self,
                                                           self.edit_post_process, self.name_changed)
                self.edit_conn_executor.start()
            else:
                # 没有更改任何信息
                self.ds_info_no_change()
        else:
            # 新增操作
            self.add_conn_executor = AddConnExecutor(self.new_dialog_data, self, self, self.save_post_process)
            self.add_conn_executor.start()

    def save_post_process(self, conn_id, opened_item_record):
        self.new_dialog_data.id = conn_id
        self.conn_saved.emit(self.new_dialog_data, opened_item_record)
        self.close()

    def edit_post_process(self):
        self.conn_changed.emit(self.new_dialog_data, self.name_changed)
        self.close()
