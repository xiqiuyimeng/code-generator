# -*- coding: utf-8 -*-
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from src.service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite
from src.service.system_storage.sqlite_abc import transactional

_author_ = 'luwt'
_date_ = '2023/1/29 20:55'


@transactional
def deal_opened_items(item_names, parent_id, data_type, level, ds_type, changed_signal,
                      init_checked=True, parent_item_order=None):
    tree_item_sqlite = OpenedTreeItemSqlite()
    # 获取本地库中缓存的数据
    child_opened_items = tree_item_sqlite.get_children(parent_id, level, ds_type)
    child_opened_item_dict = dict(map(lambda x: (x.item_name, x), child_opened_items))
    # 组装新的元素
    refreshed_items = tree_item_sqlite.add_opened_child_item(item_names, parent_id, level, ds_type,
                                                             data_type, init_checked, insert_db=False)
    # 将元素进行对比，处理策略：
    # new_items 为之前不存在的新元素，对于这些元素，需要入库
    # exists_items 为之前已经存在的元素，对于这些元素，应该更新为最新的数据
    # delete_items 为之前存在，但是现在不存在的元素，这些元素应当删除
    new_items, exists_items, delete_items = list(), list(), list()
    for opened_item in refreshed_items:
        item_name = opened_item.item_name
        exists_opened_item = child_opened_item_dict.pop(item_name) if item_name in child_opened_item_dict else None
        # 如果当前元素存在且顺序与新的元素不同，那么说明需要更新，将原id赋值给当前新的元素
        if exists_opened_item and exists_opened_item.item_order != opened_item.item_order:
            opened_item.id = exists_opened_item.id
            opened_item.expanded = exists_opened_item.expanded
            # 存储原节点顺序（方便界面定位节点），新节点数据
            exists_items.append((exists_opened_item.item_order, opened_item))
        # 如果元素不存在，则需要插入
        elif not exists_opened_item:
            new_items.append(opened_item)
    [delete_items.append(opened_item) for opened_item in child_opened_item_dict.values()]
    # 对上述集合分别处理
    if new_items:
        tree_item_sqlite.batch_insert(new_items)
    result_exists_items = tuple(map(lambda x: x[1], exists_items))
    if exists_items:
        tree_item_sqlite.batch_update(result_exists_items)
    if delete_items:
        # 倒序排列
        delete_items.sort(key=lambda x: x.item_order, reverse=True)
        delete_item_ids = tuple(map(lambda x: x.id, delete_items))
        tree_item_sqlite.batch_delete(delete_item_ids)
    # 发射信号
    changed_signal.emit({
        'new': new_items,
        'exists': exists_items,
        'delete': delete_items,
        "parent_item_order": parent_item_order
    })
    return result_exists_items


@transactional
def refresh_tab_cols(db_item, executor, exists_items, col_signal, emit_db_order=True):
    db_name = db_item.item_name
    opened_id_item_dict = dict(map(lambda x: (str(x.id), x), exists_items))
    opened_tabs = DsTableTabSqlite().select_by_opened_ids(opened_id_item_dict.keys())
    for tab in opened_tabs:
        tb_item = opened_id_item_dict.get(str(tab.parent_opened_id))
        columns = executor.open_tb(db_name, tb_item.item_name, check=False)
        DsTableColInfoSqlite().refresh_tab_cols(tab.id, columns)
        tab.col_list = columns
        if emit_db_order:
            col_signal.emit((tab, db_item.item_order, tb_item.item_order))
        else:
            col_signal.emit((tab, tb_item.item_order))
