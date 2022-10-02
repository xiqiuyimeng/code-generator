# -*- coding: utf-8 -*-
from service.sql_ds_executor.db_executor import InternetDBExecutor

_author_ = 'luwt'
_date_ = '2022/10/1 12:52'


class MySqlDBExecutor(InternetDBExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def get_dialect_driver(self) -> str:
        return 'mysql+pymysql'
