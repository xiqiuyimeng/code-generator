# -*- coding: utf-8 -*-
"""
初始化数据
"""

from service.system_storage.datasource_type_sqlite import DatasourceTypeSqlite, DatasourceType

_author_ = 'luwt'
_date_ = '2022/9/26 18:54'


datasource_type_dict = [{'id': 1, 'name': 'sql数据源', 'datasource_type_order': 1, 'is_current': 1},
                        {'id': 2, 'name': 'structure数据源', 'datasource_type_order': 2, 'is_current': 0}]


# 初始化datasource type
def init_datasource_type():
    datasource_types = DatasourceTypeSqlite().select(DatasourceType())
    if datasource_types:
        datasource_type = get_current_datasource_type(datasource_types)
        if datasource_type:
            return datasource_type
    return do_init_datasource_type()


def get_current_datasource_type(datasource_types):
    current_datasource_type = tuple(filter(lambda x: x.is_current, datasource_types))
    if current_datasource_type and len(current_datasource_type) == 1:
        return current_datasource_type[0]


def do_init_datasource_type():
    # 上述条件不满足，则进行初始化，将库里原有数据清空，初始化数据
    DatasourceTypeSqlite().drop_table()
    datasource_types = list(map(lambda x: DatasourceType(**x), datasource_type_dict))
    [DatasourceTypeSqlite().insert(datasource_type) for datasource_type in datasource_types]
    return get_current_datasource_type(datasource_types)
