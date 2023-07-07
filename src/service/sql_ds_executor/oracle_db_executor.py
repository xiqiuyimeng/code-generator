# -*- coding: utf-8 -*-
import cx_Oracle
from PyQt6.QtCore import Qt

from src.enum.common_enum import ColTypeEnum
from src.service.sql_ds_executor.db_executor import SqlDBExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo

_author_ = 'luwt'
_date_ = '2023/2/7 11:03'


class OracleDBExecutor(SqlDBExecutor):

    def connect_db(self):
        dsn = cx_Oracle.makedsn(host=self.conn_info.host,
                                port=self.conn_info.port,
                                service_name=self.conn_info.service_name)
        conn = cx_Oracle.connect(user=self.conn_info.user,
                                 password=self.conn_info.pwd,
                                 dsn=dsn)
        self.cursor = conn.cursor()

    def parse_db_name(self, row) -> str:
        return row[0]

    def parse_tb_name(self, row) -> str:
        return row[0]

    def parse_col_data(self, row) -> DsTableColInfo:
        """
        row：元祖，每个参数含义
        0 列名
        1 数据类型
        2 数据长度
        3 数据精度
        4 小数点右边的位数
        5 使用的字符类型
        6 备注
        7 是否主键
        """
        table_info = DsTableColInfo()
        table_info.col_name = row[0]
        data_type: str = row[1]
        if "(" not in data_type:
            char_used = row[5]
            if char_used:
                data_length = row[2]
                if char_used == "C":
                    data_type = f'{data_type}({data_length >> 2}char)'
                elif char_used == "B":
                    data_type = f'{data_type}({data_length})'
            else:
                data_precision = row[3]
                if data_precision:
                    data_type = f'{data_type}({data_precision},{row[4]})'
        table_info.full_data_type = data_type
        table_info.is_pk = row[7] == 'Y'
        table_info.col_comment = row[6]
        table_info.checked = Qt.CheckState.Unchecked.value
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info
