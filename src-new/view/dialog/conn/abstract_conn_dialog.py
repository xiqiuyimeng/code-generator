# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QFormLayout, QLineEdit, QGridLayout, QPushButton, QAction

from constant.constant import CONN_NAME_TEXT, TEST_CONN_BTN_TEXT, \
    OK_BTN_TEXT, CANCEL_BTN_TEXT, CONN_NAME_EXISTS, CONN_NAME_AVAILABLE, CONN_NO_CHANGE_PROMPT, SAVE_CONN_TITLE
from service.async_func.async_sql_conn_task import AddConnExecutor, EditConnExecutor
from service.async_func.async_sql_ds_task import TestConnLoadingMaskExecutor
from service.read_qrc.read_config import read_qss
from service.system_storage.conn_sqlite import SqlConnection
from service.system_storage.conn_type import *
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from view.box.message_box import pop_ok
from view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class AbstractConnDialog(DraggableDialog):
    """连接对话框抽象类，整体对话框结构应为四部分：标题区、连接名表单区、连接信息表单区、按钮区"""

    conn_saved = pyqtSignal(SqlConnection, OpenedTreeItem)

    conn_changed = pyqtSignal(SqlConnection)

    def __init__(self, connection, dialog_title, screen_rect, conn_name_id_dict):
        super().__init__()
        self.dialog_title = dialog_title
        # 从数据库中读取到的信息，用来编辑连接时使用
        self.connection: SqlConnection = connection
        # 初始化一个新的连接对象
        self.new_connection: SqlConnection = SqlConnection()
        self.conn_type: ConnType = self.get_conn_type()
        self.conn_info: dataclass = ...

        self.parent_screen_rect = screen_rect
        # 当前连接名称列表字典，key: name, value: id
        self.conn_name_id_dict: dict = conn_name_id_dict
        self.name_available = True

        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 当前对话框框架，用于放置所有部件
        self.frame: QFrame = ...
        # 框架布局，分四部分，第一部分为标题部分，第二部分为连接名表单部分，第三部分为连接信息表单部分、第四部分为按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.conn_name_layout: QFormLayout = ...
        # 连接信息表单布局
        self.conn_info_layout = ...
        self.title: QLabel = ...
        self.conn_name_label: QLabel = ...
        self.conn_name_value: QLineEdit = ...
        self.conn_name_checker: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.test_conn_button: QPushButton = ...
        self.cancel_button: QPushButton = ...
        self.ok_button: QPushButton = ...
        self.button_blank: QLabel = ...
        self.name_check_action = ...

        self.test_conn_executor: TestConnLoadingMaskExecutor = ...
        self.add_conn_executor: AddConnExecutor = ...
        self.edit_conn_executor: EditConnExecutor = ...

        self.setup_ui()
        self.setup_label_text()
        self.setup_lineedit_value()
        self.check_input()
        self.setup_input_limit_rule()
        self.connect_signal()

    def get_conn_type(self) -> ConnType: ...

    def setup_ui(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.4, self.parent_screen_rect.height() * 0.5)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.dialog_layout = QVBoxLayout(self)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("conn_frame")
        self.dialog_layout.addWidget(self.frame)
        self.frame_layout = QVBoxLayout(self.frame)

        # 标题
        self.setup_title_ui()
        # 连接名
        self.setup_conn_name_ui()
        # 连接信息
        self.setup_conn_info_ui()
        self.frame_layout.addLayout(self.conn_info_layout)
        # 按钮
        self.setup_button_ui()

    def setup_title_ui(self):
        self.title = QLabel(self.frame)
        self.title.setObjectName("conn_title")
        self.frame_layout.addWidget(self.title)

    def setup_conn_name_ui(self):
        self.conn_name_layout = QFormLayout()

        # 连接名称
        self.conn_name_label = QLabel(self.frame)
        self.conn_name_value = QLineEdit(self.frame)
        self.conn_name_value.setObjectName("conn_name_value")
        self.conn_name_layout.addRow(self.conn_name_label, self.conn_name_value)

        # 连接名称检查器
        self.conn_name_checker = QLabel(self.frame)
        self.conn_name_checker.setFixedHeight(self.conn_name_label.height())
        self.conn_name_layout.addRow('', self.conn_name_checker)

        self.frame_layout.addLayout(self.conn_name_layout)

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
        self.conn_name_label.setText(CONN_NAME_TEXT)
        # 连接信息
        self.setup_conn_info_label()
        # 按钮文本
        self.test_conn_button.setText(TEST_CONN_BTN_TEXT)
        self.ok_button.setText(OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_BTN_TEXT)

    def setup_conn_info_label(self): ...

    def setup_lineedit_value(self):
        if self.connection.id:
            self.conn_name_value.setText(self.connection.conn_name)
            # 数据回显
            self.setup_conn_info_value_show()
        else:
            # 默认值展示
            self.setup_conn_info_default_value()

    def setup_conn_info_value_show(self): ...

    def setup_conn_info_default_value(self): ...

    def check_input(self):
        # 收集用户输入数据
        self.collect_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if self.new_connection.conn_name \
                and all(dataclasses.astuple(self.conn_info)) \
                and self.name_available:
            self.set_button_available()
        else:
            self.init_button_status()

    def collect_input(self):
        self.new_connection.conn_name = self.conn_name_value.text()
        conn_param = self.collect_conn_info_input()
        # 根据参数构建连接信息对象
        self.conn_info = globals()[self.conn_type.type_class](*conn_param)
        self.new_connection.conn_info_type = self.conn_info
        self.new_connection.conn_type = self.conn_type.type

    def collect_conn_info_input(self) -> tuple: ...

    def init_button_status(self):
        self.test_conn_button.setDisabled(True)
        self.ok_button.setDisabled(True)

    def set_button_available(self):
        self.test_conn_button.setDisabled(False)
        self.ok_button.setDisabled(False)

    def setup_input_limit_rule(self):
        # 设置最多可输入字符数
        self.conn_name_value.setMaxLength(100)
        # 连接信息的输入限制规则
        self.setup_input_conn_info_limit_rule()

    def setup_input_conn_info_limit_rule(self): ...

    def connect_signal(self):
        self.conn_name_value.textEdited.connect(self.check_name_available)
        self.conn_name_value.textEdited.connect(self.check_input)
        self.test_conn_button.clicked.connect(self.test_connection)
        self.ok_button.clicked.connect(self.save_conn)
        self.cancel_button.clicked.connect(self.close)
        # 连接信息相关的信号槽连接
        self.connect_conn_info_signal()

    def connect_conn_info_signal(self): ...

    def check_name_available(self, conn_name):
        if conn_name:
            self.name_available = self.check_available(conn_name)
            if self.name_available:
                prompt = CONN_NAME_AVAILABLE.format(conn_name)
                style = "color:green"
                # 重载样式表
                self.conn_name_value.setStyleSheet(read_qss())
                icon = QIcon(":/icon/right.png")
            else:
                prompt = CONN_NAME_EXISTS.format(conn_name)
                style = "color:red"
                self.conn_name_value.setStyleSheet("#conn_name_value{border-color:red;color:red}")
                icon = QIcon(":/icon/wrong.png")
            self.name_check_action = QAction()
            self.name_check_action.setIcon(icon)
            self.conn_name_value.addAction(self.name_check_action, QLineEdit.ActionPosition.TrailingPosition)
            self.conn_name_checker.setText(prompt)
            self.conn_name_checker.setStyleSheet(style)
        else:
            self.conn_name_value.setStyleSheet(read_qss())
            self.conn_name_checker.setStyleSheet(read_qss())
            self.conn_name_checker.setText("")
            self.conn_name_value.removeAction(self.name_check_action)

    def check_available(self, conn_name):
        # 如果根据name能取到id，判断id是否是当前的id，
        # 如果当前是新增连接，连接id为空，取出的id应该为空才证明名称可用不重复
        # 如果当前是编辑连接，那么id如果是当前连接的id，证明名称无变化，可用
        conn_id = self.conn_name_id_dict.get(conn_name)
        return (conn_id is None) or (conn_id == self.connection.id)

    def test_connection(self):
        self.test_conn_executor = TestConnLoadingMaskExecutor(self.new_connection, self, self)
        self.test_conn_executor.start()

    def save_conn(self):
        self.new_connection.construct_conn_info()
        # 存在id，说明是编辑
        if self.connection.id:
            if self.new_connection != self.connection:
                self.new_connection.id = self.connection.id
                self.edit_conn_executor = EditConnExecutor(self.new_connection, self, self, self.edit_post_process)
                self.edit_conn_executor.start()
            else:
                # 没有更改任何信息
                pop_ok(CONN_NO_CHANGE_PROMPT, SAVE_CONN_TITLE, self)
                self.close()
        else:
            # 新增操作
            self.add_conn_executor = AddConnExecutor(self.new_connection, self, self, self.save_post_process)
            self.add_conn_executor.start()

    def save_post_process(self, conn_id, opened_item_record):
        self.new_connection.id = conn_id
        self.conn_saved.emit(self.new_connection, opened_item_record)
        self.close()

    def edit_post_process(self):
        self.conn_changed.emit(self.new_connection)
        self.close()


