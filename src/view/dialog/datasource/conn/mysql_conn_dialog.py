# -*- coding: utf-8 -*-

from src.constant.ds_dialog_constant import MYSQL_DEFAULT_HOST, MYSQL_DEFAULT_PORT, MYSQL_DEFAULT_USER
from src.service.system_storage.conn_type import ConnTypeEnum
from src.view.dialog.datasource.conn.internet_conn_dialog import InternetConnDialog

_author_ = 'luwt'
_date_ = '2022/9/27 19:31'


class MysqlConnDialog(InternetConnDialog):

    def get_conn_type(self):
        return ConnTypeEnum.mysql.value

    def setup_default_value(self):
        self.host_value.setText(MYSQL_DEFAULT_HOST)
        self.port_value.setText(MYSQL_DEFAULT_PORT)
        self.user_value.setText(MYSQL_DEFAULT_USER)
