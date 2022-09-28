# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton, QFileDialog

from constant.constant import SQLITE_FILE_URL_TXT, CHOOSE_SQLITE_FILE
from service.system_storage.conn_type import ConnTypeEnum
from view.dialog.conn.abstract_conn_dialog import AbstractConnDialog

_author_ = 'luwt'
_date_ = '2022/9/27 19:31'


class SqliteConnDialog(AbstractConnDialog):

    def __init__(self, *args):
        self.file_url_label: QLabel = ...
        self.file_url_value: QLineEdit = ...
        self.file_url_button: QPushButton = ...
        super().__init__(*args)

    def get_conn_type(self):
        return ConnTypeEnum.sqlite.value

    def setup_conn_info_ui(self):
        """sqlite只需要一个数据库文件地址即可"""
        self.conn_info_layout = QGridLayout()
        # 数据库文件地址
        self.file_url_label = QLabel(self.frame)
        self.conn_info_layout.addWidget(self.file_url_label, 0, 0, 1, 1)
        self.file_url_value = QLineEdit(self.frame)
        self.conn_info_layout.addWidget(self.file_url_value, 0, 1, 1, 1)
        self.file_url_button = QPushButton(self.frame)
        self.file_url_button.setObjectName('file_url_button')
        self.conn_info_layout.addWidget(self.file_url_button, 0, 2, 1, 1)

    def setup_conn_info_label(self):
        self.file_url_label.setText(SQLITE_FILE_URL_TXT)

    def setup_conn_info_value_show(self):
        self.file_url_value.setText(self.connection.conn_info_type.file_url)

    def collect_conn_info_input(self):
        file_url = self.file_url_value.text()
        return file_url,

    def connect_conn_info_signal(self):
        self.file_url_value.textChanged.connect(self.check_input)
        self.file_url_button.clicked.connect(self.path_select)

    def path_select(self):
        file_url = QFileDialog.getOpenFileName(self.frame, CHOOSE_SQLITE_FILE, '/')
        self.file_url_value.setText(file_url[0])


