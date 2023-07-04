# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QLineEdit, QFileDialog, QFormLayout, QAction

from src.constant.ds_dialog_constant import SQLITE_FILE_URL_TXT, CHOOSE_SQLITE_FILE
from src.service.system_storage.conn_type import ConnType, ConnTypeEnum
from src.view.frame.datasource.conn.conn_dialog_frame_abc import ConnDialogFrameABC
from src.view.frame.frame_func import construct_lineedit_file_action

_author_ = 'luwt'
_date_ = '2023/4/3 13:46'


class SqliteConnDialogFrame(ConnDialogFrameABC):
    """sqlite连接对话框框架"""

    def __init__(self, *args):
        self.file_url_label: QLabel = ...
        self.file_url_value: QLineEdit = ...
        self.file_url_action: QAction = ...
        super().__init__(*args)

    def get_conn_type(self) -> ConnType:
        return ConnTypeEnum.sqlite.value

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ds_content_info_ui(self):
        """sqlite只需要一个数据库文件地址即可"""
        self.frame_layout.addWidget(QLabel())
        self.ds_info_layout = QFormLayout()
        # 数据库文件地址
        self.file_url_label, self.file_url_value, self.file_url_action = construct_lineedit_file_action()
        self.ds_info_layout.addRow(self.file_url_label, self.file_url_value)

    def setup_conn_info_label_text(self):
        self.file_url_label.setText(SQLITE_FILE_URL_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_conn_info_input(self):
        return self.file_url_value.text(),

    def connect_conn_info_signal(self):
        self.file_url_value.textChanged.connect(self.check_input)
        self.file_url_action.triggered.connect(self.path_select)

    def path_select(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_SQLITE_FILE, '')
        if file_url[0]:
            self.file_url_value.setText(file_url[0])

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #
    def setup_echo_other_data(self):
        self.file_url_value.setText(self.dialog_data.conn_info_type.file_url)

    # ------------------------------ 后置处理 end ------------------------------ #

