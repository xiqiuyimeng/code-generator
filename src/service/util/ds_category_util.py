# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2022/9/26 18:54'


def get_current_ds_category(ds_categories):
    current_ds_category = [ds_category for ds_category in ds_categories if ds_category.is_current]
    if current_ds_category and len(current_ds_category) == 1:
        return current_ds_category[0]

