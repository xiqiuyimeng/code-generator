# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.datasource.conn.conn_dialog_frame_abc import ConnDialogFrameABC
from src.view.frame.datasource.conn.mysql_conn_dialog_frame import MysqlConnDialogFrame
from src.view.frame.datasource.conn.oracle_conn_dialog_frame import OracleConnDialogFrame
from src.view.frame.datasource.conn.sqlite_conn_dialog_frame import SqliteConnDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 15:48'


class ConnDialogABC(CustomSaveDialogABC):
    """连接对话框抽象类"""
    save_signal = pyqtSignal(OpenedTreeItem)
    # 修改后的连接名称
    edit_signal = pyqtSignal(str)

    def __init__(self, dialog_title, conn_name_list, conn_id):
        self.conn_name_list = conn_name_list
        self.conn_id = conn_id
        self.frame: ConnDialogFrameABC = ...
        super().__init__(dialog_title)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.window_geometry.width() * 0.4, self.window_geometry.height() * 0.5)


class MysqlConnDialog(ConnDialogABC):
    """mysql连接对话框"""

    def get_frame(self) -> MysqlConnDialogFrame:
        return MysqlConnDialogFrame(self, self.dialog_title,
                                    self.conn_name_list, self.conn_id)


class OracleConnDialog(ConnDialogABC):
    """oracle连接对话框"""

    def get_frame(self) -> OracleConnDialogFrame:
        return OracleConnDialogFrame(self, self.dialog_title,
                                     self.conn_name_list, self.conn_id)


class SqliteConnDialog(ConnDialogABC):
    """sqlite连接对话框"""

    def get_frame(self) -> SqliteConnDialogFrame:
        return SqliteConnDialogFrame(self, self.dialog_title,
                                     self.conn_name_list, self.conn_id)
