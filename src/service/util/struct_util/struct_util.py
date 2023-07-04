# -*- coding: utf-8 -*-
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from src.service.util.struct_util.data_type import get_data_type

_author_ = 'luwt'
_date_ = '2023/1/31 13:57'


def assemble_col_info(name, value):
    col_info = DsTableColInfo()
    col_info.init_value()
    col_info.col_name = name
    # 获取变量值的数据类型映射值
    data_type = get_data_type(value)
    col_info.data_type = data_type
    col_info.full_data_type = data_type
    return col_info


class StructParser:

    def __init__(self, struct_content):
        self.struct_content = struct_content

    def parse(self):
        load_content = self.load_content()
        return self.do_parse_content(load_content)

    def load_content(self) -> object:
        ...

    def do_parse_content(self, load_content) -> list:
        ...


class StructBeautifier:

    def __init__(self, struct_content):
        self.struct_content = struct_content

    def beautify(self):
        return self.do_beautify()

    def do_beautify(self) -> str:
        ...
