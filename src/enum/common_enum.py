# -*- coding: utf-8 -*-
"""
项目中使用到的通用枚举类型
"""
from enum import Enum

from PyQt6.QtCore import Qt

_author_ = 'luwt'
_date_ = '2023/7/6 16:27'


class CurrentEnum(Enum):
    is_current = 1
    not_current = 0


def get_checked_enum(checked_value):
    for checked in Qt.CheckState:
        if checked.value == checked_value:
            return checked
    return Qt.CheckState.Unchecked


class ColTypeEnum(Enum):
    col = 'col'
    obj = 'object'
    array = 'array'


class SqlTreeItemLevelEnum(Enum):
    conn_level = 0
    db_level = 1
    tb_level = 2


class ExpandedEnum(Enum):
    expanded = 1
    collapsed = 0


class TabOpenedEnum(Enum):
    opened = 1
    not_opened = 0


class ConfigTypeEnum(Enum):
    # 输出路径
    output_dir = 0
    # 模板变量
    template_var = 1


class RequiredEnum(Enum):
    not_required = 0
    required = 1


def check_required_value_legal(value):
    return value == RequiredEnum.not_required.value or value == RequiredEnum.required.value
