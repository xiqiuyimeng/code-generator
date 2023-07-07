# -*- coding: utf-8 -*-
from enum import Enum

_author_ = 'luwt'
_date_ = '2022/12/6 19:49'


class DataTypeEnum(Enum):
    str_type = str, 'string'
    int_type = int, 'int'
    float_type = float, 'float'
    # 复数
    complex_type = complex, 'complex'
    bool_type = bool, 'boolean'
    # 字典映射为对象
    dict_type = dict, 'object'
    # 列表映射为数组类型
    list_type = list, '{} []'


def get_data_type(var):
    var_type = type(var)
    for data_type in DataTypeEnum:
        if data_type.value[0] == var_type:
            return data_type.value[1]
    return DataTypeEnum.dict_type.value[1]
