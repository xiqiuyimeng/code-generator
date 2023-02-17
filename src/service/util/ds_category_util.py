# -*- coding: utf-8 -*-
"""
初始化数据
"""

_author_ = 'luwt'
_date_ = '2022/9/26 18:54'


def get_current_ds_category(ds_categories):
    current_ds_category = tuple(filter(lambda x: x.is_current, ds_categories))
    if current_ds_category and len(current_ds_category) == 1:
        return current_ds_category[0]

