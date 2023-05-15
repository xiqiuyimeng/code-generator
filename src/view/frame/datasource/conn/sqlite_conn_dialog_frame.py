# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QGridLayout, QFileDialog

from src.constant.ds_dialog_constant import SQLITE_FILE_URL_TXT, CHOOSE_SQLITE_FILE
from src.service.system_storage.conn_type import ConnType, ConnTypeEnum
from src.view.frame.datasource.conn.conn_dialog_frame_abc import ConnDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/3 13:46'


class SqliteConnDialogFrame(ConnDialogFrameABC):
    """sqlite连接对话框框架"""

    def __init__(self, *args):
        self.file_url_label: QLabel = ...
        self.file_url_value: QLineEdit = ...
        self.file_url_button: QPushButton = ...
        super().__init__(*args)

    def get_conn_type(self) -> ConnType:
        return ConnTypeEnum.sqlite.value

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ds_content_info_ui(self):
        """sqlite只需要一个数据库文件地址即可"""
        self.ds_info_layout = QGridLayout()
        # 数据库文件地址
        self.file_url_label = QLabel(self)
        self.ds_info_layout.addWidget(self.file_url_label, 0, 0, 1, 1)
        self.file_url_value = QLineEdit(self)
        self.ds_info_layout.addWidget(self.file_url_value, 0, 1, 1, 1)
        self.file_url_button = QPushButton(self)
        self.file_url_button.setObjectName('file_url_button')
        self.ds_info_layout.addWidget(self.file_url_button, 0, 2, 1, 1)

    def setup_conn_info_label(self):
        self.file_url_label.setText(SQLITE_FILE_URL_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_conn_info_input(self):
        return self.file_url_value.text(),

    def connect_conn_info_signal(self):
        self.file_url_value.textChanged.connect(self.check_input)
        self.file_url_button.clicked.connect(self.path_select)

    def path_select(self):
        file_url = QFileDialog.getOpenFileName(self.frame, CHOOSE_SQLITE_FILE, '')
        if file_url[0]:
            self.file_url_value.setText(file_url[0])

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #
    def setup_echo_other_data(self):
        self.file_url_value.setText(self.dialog_data.conn_info_type.file_url)

    # ------------------------------ 后置处理 end ------------------------------ #

