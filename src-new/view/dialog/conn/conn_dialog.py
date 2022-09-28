# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QFormLayout, QLineEdit, QGridLayout, QPushButton, QAction

from service.async_func.async_conn_task import AddConnExecutor, EditConnExecutor
from service.async_func.async_mysql_task import TestConnLoadingMaskExecutor
from service.read_qrc.read_config import read_qss
from constant.constant import CONN_NAME_TEXT, HOST_TEXT, PORT_TEXT, USERNAME_TEXT, PWD_TEXT, TEST_CONN_BTN_TEXT, \
    OK_BTN_TEXT, CANCEL_BTN_TEXT, DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USER, CONN_NAME_EXISTS, CONN_NAME_AVAILABLE
from service.system_storage.conn_sqlite import SqlConnection
from view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class ConnDialog(DraggableDialog):

    conn_changed = pyqtSignal(SqlConnection)

    def __init__(self, connection, dialog_title, screen_rect, conn_name_dict):
        super().__init__()
        self.dialog_title = dialog_title
        self.connection: SqlConnection = connection
        self.parent_screen_rect = screen_rect
        # 当前连接名称列表字典，key: id, value: name
        self.conn_name_dict = conn_name_dict
        self.name_available = True

        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 当前对话框框架，用于放置所有部件
        self.frame: QFrame = ...
        # 框架布局，分三部分，第一部分为标题部分，第二部分为表单部分，第三部分为按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.body_layout: QFormLayout = ...
        self.title: QLabel = ...
        self.conn_name_label: QLabel = ...
        self.conn_name_value: QLineEdit = ...
        self.conn_name_checker: QLabel = ...
        self.host_label: QLabel = ...
        self.host_value: QLineEdit = ...
        self.port_label: QLabel = ...
        self.port_value: QLineEdit = ...
        self.user_label: QLabel = ...
        self.user_value: QLineEdit = ...
        self.pwd_label: QLabel = ...
        self.pwd_value: QLineEdit = ...
        self.button_layout: QGridLayout = ...
        self.test_conn_button: QPushButton = ...
        self.cancel_button: QPushButton = ...
        self.ok_button: QPushButton = ...
        self.button_blank: QLabel = ...
        self.action = ...

        self.test_conn_executor: TestConnLoadingMaskExecutor = ...
        self.add_conn_executor: AddConnExecutor = ...
        self.edit_conn_executor: EditConnExecutor = ...

        self.setup_ui()
        self.setup_label_text()
        self.setup_lineedit_value()
        self.check_input()
        self.setup_input_limit_rule()
        self.connect_signal()

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

        self.title = QLabel(self.frame)
        self.title.setObjectName("conn_title")
        self.frame_layout.addWidget(self.title)

        # 主体表单布局
        self.body_layout = QFormLayout()
        # 连接名称
        self.conn_name_label = QLabel(self.frame)
        self.conn_name_value = QLineEdit(self.frame)
        self.conn_name_value.setObjectName("conn_name_value")
        self.body_layout.addRow(self.conn_name_label, self.conn_name_value)
        # 连接名称检查器
        self.conn_name_checker = QLabel(self.frame)
        self.conn_name_checker.setFixedHeight(self.conn_name_label.height())
        self.body_layout.addRow("", self.conn_name_checker)
        # 主机地址
        self.host_label = QLabel(self.frame)
        self.host_value = QLineEdit(self.frame)
        self.body_layout.addRow(self.host_label, self.host_value)
        # 端口号
        self.port_label = QLabel(self.frame)
        self.port_value = QLineEdit(self.frame)
        self.body_layout.addRow(self.port_label, self.port_value)
        # 用户名
        self.user_label = QLabel(self.frame)
        self.user_value = QLineEdit(self.frame)
        self.body_layout.addRow(self.user_label, self.user_value)
        # 密码
        self.pwd_label = QLabel(self.frame)
        self.pwd_value = QLineEdit(self.frame)
        self.body_layout.addRow(self.pwd_label, self.pwd_value)
        self.frame_layout.addLayout(self.body_layout)

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
        self.title.setText(self.dialog_title)
        self.conn_name_label.setText(CONN_NAME_TEXT)
        self.host_label.setText(HOST_TEXT)
        self.port_label.setText(PORT_TEXT)
        self.user_label.setText(USERNAME_TEXT)
        self.pwd_label.setText(PWD_TEXT)
        self.test_conn_button.setText(TEST_CONN_BTN_TEXT)
        self.ok_button.setText(OK_BTN_TEXT)
        self.cancel_button.setText(CANCEL_BTN_TEXT)

    def setup_lineedit_value(self):
        if self.connection.id:
            self.conn_name_value.setText(self.connection.name)
            self.host_value.setText(self.connection.host)
            self.port_value.setText(str(self.connection.port))
            self.user_value.setText(self.connection.user)
            self.pwd_value.setText(self.connection.pwd)
            self.set_button_available()
        else:
            self.host_value.setText(DEFAULT_HOST)
            self.port_value.setText(DEFAULT_PORT)
            self.user_value.setText(DEFAULT_USER)

    def init_button_status(self):
        self.test_conn_button.setDisabled(True)
        self.ok_button.setDisabled(True)

    def set_button_available(self):
        self.test_conn_button.setDisabled(False)
        self.ok_button.setDisabled(False)

    def setup_input_limit_rule(self):
        # 设置端口号只能输入数字
        self.port_value.setValidator(QIntValidator())
        # 设置最多可输入字符数
        self.conn_name_value.setMaxLength(100)
        self.host_value.setMaxLength(100)
        self.user_value.setMaxLength(30)
        self.pwd_value.setMaxLength(50)

    def connect_signal(self):
        self.conn_name_value.textEdited.connect(self.check_name_available)
        self.conn_name_value.textEdited.connect(self.check_input)
        self.host_value.textEdited.connect(self.check_input)
        self.port_value.textEdited.connect(self.check_input)
        self.user_value.textEdited.connect(self.check_input)
        self.pwd_value.textEdited.connect(self.check_input)

        self.test_conn_button.clicked.connect(self.test_connection)
        self.ok_button.clicked.connect(self.save_conn)
        self.cancel_button.clicked.connect(self.close)

    def check_name_available(self, conn_name):
        if conn_name:
            if self.check_available(conn_name):
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
            self.action = QAction()
            self.action.setIcon(icon)
            self.conn_name_value.addAction(self.action, QLineEdit.ActionPosition.TrailingPosition)
            self.conn_name_checker.setText(prompt)
            self.conn_name_checker.setStyleSheet(style)
        else:
            self.conn_name_value.setStyleSheet(read_qss())
            self.conn_name_checker.setStyleSheet(read_qss())
            self.conn_name_checker.setText("")
            self.conn_name_value.removeAction(self.action)

    def check_available(self, conn_name):
        conn_names = list(self.conn_name_dict.values())
        if self.connection.id:
            # 如果是修改，排除掉原来的名字
            conn_names.remove(self.connection.name)
        return conn_name not in conn_names

    def check_input(self):
        # 检查是否都有值
        conn = self.get_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if all(conn) and self.name_available:
            self.set_button_available()
        else:
            self.init_button_status()

    def get_input_connection(self):
        return Connection(self.connection.id, *self.get_input())

    def get_input(self):
        conn_name = self.conn_name_value.text()
        host = self.host_value.text()
        port = int(self.port_value.text())
        user = self.user_value.text()
        pwd = self.pwd_value.text()
        return conn_name, host, port, user, pwd

    def test_connection(self):
        new_conn = self.get_input_connection()
        self.test_conn_executor = TestConnLoadingMaskExecutor(new_conn, self, self)
        self.test_conn_executor.start()

    def save_conn(self):
        new_conn = self.get_input_connection()
        # 存在id，说明是编辑
        if self.connection.id:
            self.edit_conn_executor = EditConnExecutor(new_conn, self, self, self.save_post_process)
            self.edit_conn_executor.start()
        else:
            # 新增操作
            self.add_conn_executor = AddConnExecutor(new_conn, self, self, self.save_post_process)
            self.add_conn_executor.start()

    def save_post_process(self, conn_id=None):
        # 如果返回了id，视为添加
        if conn_id:
            new_conn = Connection(conn_id, *self.get_input())
            self.conn_changed.emit(new_conn)
            self.close()
        else:
            # 视为编辑
            new_conn = self.get_input_connection()
            self.conn_changed.emit(new_conn)
            self.close()


