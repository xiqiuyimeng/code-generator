# -*- coding: utf-8 -*-
from src.service.system_storage.conn_type import ConnTypeEnum
from src.service.system_storage.ds_col_type_sqlite import DsColTypeSqlite
from src.service.system_storage.struct_type import StructTypeEnum
from src.service.util.db_id_generator import init_id_generator
from src.service.util.system_storage_util import get_sqlite_sequence, transactional, release_connection

_author_ = 'luwt'
_date_ = '2023/2/27 9:03'


def handle_ds_type_add_update(ds_type_dict, ds_type, item_order, add_ds_types,
                              update_ds_types, ds_col_type_sqlite):
    if ds_type in ds_type_dict:
        exists_ds_type = ds_type_dict.pop(ds_type)
        # 如果数据源类型已经存在，但顺序不同，调整顺序
        if exists_ds_type and exists_ds_type.item_order != item_order:
            exists_ds_type.item_order = item_order
            update_ds_types.append(exists_ds_type)
    else:
        # 如果不存在，需要添加
        add_ds_types.append(ds_col_type_sqlite.assemble_ds_type(ds_type, item_order))


@transactional
def init_ds_type():
    ds_col_type_sqlite = DsColTypeSqlite()
    # 获取数据库中保存的数据源类型
    ds_types = ds_col_type_sqlite.get_ds_types()
    ds_type_dict = {ds_type.ds_col_type: ds_type for ds_type in ds_types}
    # 遍历枚举获取实际的数据源类型
    add_ds_types, update_ds_types = list(), list()
    for item_order, conn_type in enumerate(ConnTypeEnum, start=1):
        handle_ds_type_add_update(ds_type_dict, conn_type.value.display_name, item_order,
                                  add_ds_types, update_ds_types, ds_col_type_sqlite)
    for item_order, struct_type in enumerate(StructTypeEnum, start=len(ConnTypeEnum) + 1):
        handle_ds_type_add_update(ds_type_dict, struct_type.value.display_name, item_order,
                                  add_ds_types, update_ds_types, ds_col_type_sqlite)
    # 处理添加和更新的元素
    if add_ds_types:
        ds_col_type_sqlite.batch_insert(add_ds_types)
    if update_ds_types:
        ds_col_type_sqlite.batch_update(update_ds_types)
    # 最后如果 ds_type_dict 中还有值，那么应当是需要删除的
    if ds_type_dict:
        ds_col_type_sqlite.batch_delete_ds_types([ds_type.id for ds_type in ds_type_dict.values()])


def init_data():
    try:
        # 初始化id生成器
        init_id_generator(get_sqlite_sequence)
        # 初始化类型映射-数据源列类型中保存的数据源类型
        init_ds_type()
    finally:
        # 主线程使用的连接需要手动释放
        release_connection()
