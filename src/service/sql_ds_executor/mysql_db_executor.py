# -*- coding: utf-8 -*-
from exception.exception import BusinessException
from service.sql_ds_executor.db_executor import InternetDBExecutor
from service.system_storage.conn_type import get_conn_type_by_type
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class MySqlDBExecutor(InternetDBExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def get_dialect_driver(self) -> str:
        return 'mysql+pymysql'

    def check_db(self, db):
        query_db_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_db_sql
        db_records = self.get_data(f'{query_db_sql} like \'{db}\'').all()
        if not db_records:
            raise BusinessException(f'{db}库不存在')

    def do_check_tb(self, tb):
        query_tb_sql = get_conn_type_by_type(self.sql_conn.conn_type).query_tb_sql
        db_records = self.get_data(f'{query_tb_sql} like \'{tb}\'').all()
        if not db_records:
            raise BusinessException(f'{tb}表不存在')

    def change_db(self, db):
        self.db.query(f'use {db};')

    def convert_tb_data(self, db_record):
        table_info = DsTableColInfo()
        table_info.col_name = db_record.get('Field')
        table_info.full_data_type = db_record.get('Type')
        table_info.is_pk = db_record.get('Key') == 'PRI'
        table_info.col_comment = db_record.get('Comment')
        table_info.checked = CheckedEnum.unchecked.value
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info


