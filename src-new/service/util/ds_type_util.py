# -*- coding: utf-8 -*-
"""
初始化数据
"""

_author_ = 'luwt'
_date_ = '2022/9/26 18:54'


def get_current_datasource_type(datasource_types):
    current_datasource_type = tuple(filter(lambda x: x.is_current, datasource_types))
    if current_datasource_type and len(current_datasource_type) == 1:
        return current_datasource_type[0]

