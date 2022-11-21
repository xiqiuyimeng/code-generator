# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from constant.constant import JSON_TYPE, JSON_DISPLAY_NAME

_author_ = 'luwt'
_date_ = '2022/11/11 16:06'


def get_struct_type(display_name):
    for struct_type in StructTypeEnum:
        if struct_type.value.display_name == display_name:
            return struct_type.value
    return StructTypeEnum.json_type.value


def get_struct_dialog(display_name):
    return get_struct_type(display_name).type_dialog


@dataclass
class StructType:

    type: int = field(init=False)
    # 展示名称，也用来标识icon类型
    display_name: str = field(init=False)
    # 对应类型承载实际连接信息的实体类
    type_class: str = field(init=False)
    # 对应类型的连接对话框
    type_dialog: str = field(init=False)


class StructTypeEnum(Enum):

    json_type = StructType()
    json_type.type = JSON_TYPE
    json_type.display_name = JSON_DISPLAY_NAME
    json_type.type_class = 'SqliteConn'
    json_type.type_dialog = 'JsonStructDialog'
