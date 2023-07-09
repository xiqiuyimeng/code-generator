# -*- coding: utf-8 -*-
from enum import Enum

from src.constant.bar_constant import SQL_DS_CATEGORY, STRUCT_DS_CATEGORY
from src.service.system_storage.ds_category_sqlite import DsCategory

_author_ = 'luwt'
_date_ = '2023/7/6 16:05'


sql_ds_category_dict = {
    'name': SQL_DS_CATEGORY,
    'item_order': 1,
    'is_current': 1
}
struct_ds_category_dict = {
    'name': STRUCT_DS_CATEGORY,
    'item_order': 2,
    'is_current': 0
}


class DsCategoryEnum(Enum):
    sql_ds_category = DsCategory(**sql_ds_category_dict)
    struct_ds_category = DsCategory(**struct_ds_category_dict)

    def get_name(self):
        return self.value.name


def get_ds_category_list():
    return [ds_category.value for ds_category in DsCategoryEnum]
