# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from enum import Enum

from constant.constant import JSON_TYPE, JSON_DISPLAY_NAME, FOLDER_TYPE, FOLDER_DISPLAY_NAME

_author_ = 'luwt'
_date_ = '2022/11/11 16:06'


def mapping_struct_type(struct_info):
    for struct_type in StructTypeEnum:
        if struct_type.value.type == struct_info.struct_type:
            # 根据匹配到的类型，映射为具体的对象
            struct_info.struct_type_info = struct_type.value


def get_struct_type(display_name):
    for struct_type in StructTypeEnum:
        if struct_type.value.display_name == display_name:
            return struct_type.value
    return StructTypeEnum.json_type.value


def get_struct_dialog(display_name):
    return get_struct_type(display_name).type_dialog


@dataclass
class StructType:

    type: str = field(init=False)
    # 展示名称，也用来标识icon类型
    display_name: str = field(init=False)
    # 对应类型的连接对话框
    type_dialog: str = field(init=False, default=None)
    # 对应的美化器
    beautifier_executor: str = field(init=False, default=None)
    # 对应的内容解析器
    parse_executor: str = field(init=False, default=None)


class FolderTypeEnum(Enum):
    # 默认的值，文件夹
    folder_type = StructType()
    folder_type.type = FOLDER_TYPE
    folder_type.display_name = FOLDER_DISPLAY_NAME


class StructTypeEnum(Enum):

    json_type = StructType()
    json_type.type = JSON_TYPE
    json_type.display_name = JSON_DISPLAY_NAME
    json_type.type_dialog = 'JsonStructDialog'
    json_type.beautifier_executor = 'PrettyJsonExecutor'
    json_type.parse_executor = 'OpenJsonExecutor'

