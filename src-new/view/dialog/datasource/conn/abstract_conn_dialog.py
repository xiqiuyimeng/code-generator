# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton

from constant.constant import CONN_NAME_TEXT, TEST_CONN_BTN_TEXT, \
    OK_BTN_TEXT, CANCEL_BTN_TEXT
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
        # 初始化一个新的连接对象
        self.new_connection: SqlConnection = SqlConnection()
        self.conn_type: ConnType = self.get_conn_type()
        self.conn_info: dataclass = ...

        # 连接信息表单布局
        self.test_conn_button: QPushButton = ...

        self.test_conn_executor: TestConnLoadingMaskExecutor = ...
        self.add_conn_executor: AddConnExecutor = ...
        self.edit_conn_executor: EditConnExecutor = ...

        super().__init__(connection, dialog_title, screen_rect, conn_name_id_dict)

    def resize_window(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.4, self.parent_screen_rect.height() * 0.5)

    def get_conn_type(self) -> ConnType: ...

    def setup_ds_content_info_ui(self):
        self.setup_conn_info_ui()

    def setup_conn_info_ui(self): ...

    def setup_button_ui(self):
        # 按钮部分
        self.button_layout = QGridLayout()
        self.test_conn_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.test_conn_button, 0, 0, 1, 1)
        self.button_blank = QLabel(self.frame)
        self.button_layout.addWidget(self.button_blank, 0, 1, 1, 1)
        self.ok_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.ok_button, 0, 2, 1, 1)
        self.cancel_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.cancel_button, 0, 3, 1, 1)
        self.frame_layout.addLayout(self.button_layout)

    def setup_label_text(self):
        self.title.setText(self.dialog_title.format(self.conn_type.display_name))
        self.ds_name_label.setText(CONN_NAME_TEXT)
        # 连接信息
        self.setup_conn_info_label()
        # 按钮文本
        self.test_conn_button.setText(TEST_CONN_BTN_TEXT)
        self.ok_button.setText(OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_BTN_TEXT)

    def setup_conn_info_label(self): ...

    def setup_ds_info_value_show(self):
        self.ds_name_value.setText(self.ds_info.conn_name)
        # 数据回显
        self.setup_conn_info_value_show()

    def setup_ds_info_default_value(self):
        self.setup_conn_info_default_value()

    def setup_conn_info_value_show(self): ...

    def setup_conn_info_default_value(self): ...

    def button_available(self) -> bool:
        return self.new_connection.conn_name \
                and all(dataclasses.astuple(self.conn_info)) \
                and self.name_available

    def collect_input(self):
        self.new_connection.conn_name = self.ds_name_value.text()
        conn_param = self.collect_conn_info_input()
        # 根据参数构建连接信息对象
        self.conn_info = globals()[self.conn_type.type_class](*conn_param)
        self.new_connection.conn_info_type = self.conn_info
        self.new_connection.conn_type = self.conn_type.type

    def collect_conn_info_input(self) -> tuple: ...

    def init_other_button_status(self):
        self.test_conn_button.setDisabled(True)

    def set_other_button_available(self):
        self.test_conn_button.setDisabled(False)

    def setup_input_ds_info_limit_rule(self):
        # 连接信息的输入限制规则
        self.setup_input_conn_info_limit_rule()

    def setup_input_conn_info_limit_rule(self): ...

    def connect_ds_other_signal(self):
        self.test_conn_button.clicked.connect(self.test_connection)
        # 连接信息相关的信号槽连接
        self.connect_conn_info_signal()

    def connect_conn_info_signal(self): ...

    def test_connection(self):
        self.test_conn_executor = TestConnLoadingMaskExecutor(self.new_connection, self, self)
        self.test_conn_executor.start()

    def save_ds_info(self):
        self.new_connection.construct_conn_info()
        # 存在id，说明是编辑
        if self.ds_info.id:
            if self.new_connection != self.ds_info:
                self.new_connection.id = self.ds_info.id
                self.name_changed = self.new_connection.conn_name != self.ds_info.conn_name
                self.edit_conn_executor = EditConnExecutor(self.new_connection, self, self,
                                                           self.edit_post_process, self.name_changed)
                self.edit_conn_executor.start()
            else:
                # 没有更改任何信息
                self.ds_info_no_change()
        else:
            # 新增操作
            self.add_conn_executor = AddConnExecutor(self.new_connection, self, self, self.save_post_process)
            self.add_conn_executor.start()

    def save_post_process(self, conn_id, opened_item_record):
        self.new_connection.id = conn_id
        self.conn_saved.emit(self.new_connection, opened_item_record)
        self.close()

    def edit_post_process(self):
        self.conn_changed.emit(self.new_connection, self.name_changed)
        self.close()


