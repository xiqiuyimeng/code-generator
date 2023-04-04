# -*- coding: utf-8 -*-
from src.constant.ds_dialog_constant import MYSQL_DEFAULT_HOST, MYSQL_DEFAULT_PORT, MYSQL_DEFAULT_USER
from src.service.system_storage.conn_type import ConnTypeEnum, ConnType
from src.view.frame.datasource.conn.internet_conn_dialog_frame import InternetConnDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 13:43'


class MysqlConnDialogFrame(InternetConnDialogFrame):
    """mysql连接对话框框架"""

    def get_conn_type(self) -> ConnType:
        return ConnTypeEnum.mysql.value

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_default_value(self):
        self.host_value.setText(MYSQL_DEFAULT_HOST)
        self.port_value.setText(MYSQL_DEFAULT_PORT)
        self.user_value.setText(MYSQL_DEFAULT_USER)

    # ------------------------------ 创建ui界面 end ------------------------------ #
