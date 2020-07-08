﻿# -*- coding: utf-8 -*-
"""
异常枚举
"""
from enum import Enum
_author_ = 'luwt'
_date_ = '2020/6/11 20:29'


class MysqlException(RuntimeError):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)


class ExceptionEnum(Enum):
    param_path_error = "路径参数有误"

    def assert_true(self):
        raise MysqlException(self.value)


