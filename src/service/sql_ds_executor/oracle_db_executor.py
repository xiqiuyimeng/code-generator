# -*- coding: utf-8 -*-
from src.constant.constant import ORACLE_CHECK_DB_SQL, ORACLE_CHECK_TB_SQL
from src.service.sql_ds_executor.db_executor import InternetDBExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2023/2/7 11:03'


class OracleDBExecutor(InternetDBExecutor):

    def get_sql_connect_url(self) -> str:
        return f'oracle://{self.conn_info.user}:{self.conn_info.pwd}@' \
               f'{self.conn_info.host}:{self.conn_info.port}/?service_name={self.conn_info.service_name}'

    def get_check_db_sql(self) -> str:
        return ORACLE_CHECK_DB_SQL

    def get_check_tb_sql(self) -> str:
        return ORACLE_CHECK_TB_SQL

    def convert_tb_data(self, db_record):
        table_info = DsTableColInfo()
        table_info.col_name = db_record.get('column_name')
        data_type: str = db_record.get('data_type')
        if "(" not in data_type:
            char_used = db_record.get('char_used')
            if char_used:
                data_length = db_record.get('data_length')
                if char_used == "C":
                    data_type = f'{data_type}({data_length >> 2}char)'
                elif char_used == "B":
                    data_type = f'{data_type}({data_length})'
            else:
                data_precision = db_record.get('data_precision')
                if data_precision:
                    data_type = f'{data_type}({data_precision},{db_record.get("data_scale")})'
        table_info.full_data_type = data_type
        table_info.is_pk = db_record.get('primary_key') == 'Y'
        table_info.col_comment = db_record.get('comments')
        table_info.checked = CheckedEnum.unchecked.value
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info
