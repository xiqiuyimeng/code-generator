# -*- coding: utf-8 -*-
from service.sql_ds_executor.db_executor import InternetDBExecutor
from service.system_storage.ds_table_info_sqlite import DsTableInfo, CheckedEnum, ColTypeEnum

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class MySqlDBExecutor(InternetDBExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def get_dialect_driver(self) -> str:
        return 'mysql+pymysql'

    def convert_tb_data(self, db_record):
        table_info = DsTableInfo()
        table_info.col_name = db_record.get('Field')
        table_info.full_data_type = db_record.get('Type')
        table_info.is_pk = db_record.get('Key') == 'PRI'
        table_info.col_comment = db_record.get('Comment')
        table_info.checked = CheckedEnum.unchecked.value
        table_info.handle_data_type()
        table_info.col_type = ColTypeEnum.col.value
        return table_info


