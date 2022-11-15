# -*- coding: utf-8 -*-

from constant.constant import DEFAULT_HOST, DEFAULT_PORT, DEFAULT_USER
from service.system_storage.conn_type import ConnTypeEnum
from view.dialog.datasource.conn.internet_conn_dialog import InternetConnDialog

_author_ = 'luwt'
_date_ = '2022/9/27 19:31'


class MysqlConnDialog(InternetConnDialog):

    def __init__(self, *args):
        super().__init__(*args)

    def get_conn_type(self):
        return ConnTypeEnum.mysql.value

    def setup_conn_info_default_value(self):
        self.host_value.setText(DEFAULT_HOST)
        self.port_value.setText(DEFAULT_PORT)
        self.user_value.setText(DEFAULT_USER)
