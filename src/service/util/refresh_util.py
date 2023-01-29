# -*- coding: utf-8 -*-
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite
from service.system_storage.sqlite_abc import transactional

_author_ = 'luwt'
_date_ = '2023/1/29 20:55'


@transactional
def deal_opened_items(item_names, parent_id, data_type, level, ds_type, changed_signal):
    tree_item_sqlite = OpenedTreeItemSqlite()
    # 获取本地库中缓存的数据
    child_opened_items = tree_item_sqlite.get_children(parent_id, level, ds_type)
    child_opened_item_dict = dict(map(lambda x: (x.item_name, x), child_opened_items))
    # 组装新的元素
    refreshed_items = tree_item_sqlite.add_opened_child_item(item_names, parent_id, level,
                                                             ds_type, data_type, insert_db=False)
    # 将元素进行对比，处理策略：
    # new_items 为之前不存在的新元素，对于这些元素，需要入库
    # exists_items 为之前已经存在的元素，对于这些元素，应该更新为最新的数据
    # delete_items 为之前存在，但是现在不存在的元素，这些元素应当删除
    new_items, exists_items, delete_items = list(), list(), list()
    for opened_item in refreshed_items:
        item_name = opened_item.item_name
        exists_opened_item = child_opened_item_dict.pop(item_name) if item_name in child_opened_item_dict else None
        # 如果当前元素存在，将原id赋值给当前新的元素
        if exists_opened_item:
            opened_item.id = exists_opened_item.id
            opened_item.expanded = exists_opened_item.expanded
            exists_items.append(opened_item)
        else:
            new_items.append(opened_item)
    [delete_items.append(opened_item) for opened_item in child_opened_item_dict.values()]
    # 对上述集合分别处理
    if new_items:
        tree_item_sqlite.batch_insert(new_items)
    if exists_items:
        tree_item_sqlite.batch_update(exists_items)
    if delete_items:
        delete_item_ids = tuple(map(lambda x: x.id, delete_items))
        tree_item_sqlite.batch_delete(delete_item_ids)
    # 发射信号
    changed_signal.emit({
        'new': new_items,
        'exists': exists_items,
        'delete': delete_items,
        "parent_id": parent_id
    })
    return exists_items


@transactional
def refresh_tab_cols(db_name, executor, exists_items, col_signal):
    opened_id_name_dict = dict(map(lambda x: (str(x.id), x.item_name), exists_items))
    opened_tabs = DsTableTabSqlite().select_by_opened_ids(opened_id_name_dict.keys())
    for tab in opened_tabs:
        columns = executor.open_tb(db_name,
                                   opened_id_name_dict.get(str(tab.parent_opened_id)),
                                   check=False)
        DsTableColInfoSqlite().refresh_tab_cols(tab.id, columns)
        tab.col_list = columns
        col_signal.emit(tab)
