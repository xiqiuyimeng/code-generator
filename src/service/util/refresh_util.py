# -*- coding: utf-8 -*-
import copy

from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from src.service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite
from src.service.util.system_storage_util import transactional

_author_ = 'luwt'
_date_ = '2023/1/29 20:55'


@transactional
def deal_opened_items(item_names, parent_id, data_type, level, ds_category, changed_signal,
                      init_checked=True, parent_item_order=None):
    tree_item_sqlite = OpenedTreeItemSqlite()
    # 获取本地库中缓存的数据
    child_opened_records = tree_item_sqlite.get_children(parent_id, level, ds_category)
    child_opened_record_dict = {item.item_name: item for item in child_opened_records}
    # 组装新的元素
    refreshed_item_records = tree_item_sqlite.add_opened_child_item(item_names, parent_id, level, ds_category,
                                                                    data_type, init_checked, insert_db=False)
    # 将元素进行对比，处理策略：
    # new_item_records 为之前不存在的新元素，对于这些元素，需要入库
    # update_item_records 为之前已经存在的元素，对于这些元素，应该更新为最新的数据
    # exists_item_records 仅仅记录已经存在的元素，不关心是否变化，将作为方法的返回结果，供其他方法使用
    # unchanged_item_records 没有变化的元素
    # delete_item_records 为之前存在，但是现在不存在的元素，这些元素应当删除
    new_item_records, update_item_records, exists_item_records, = list(), list(), list()
    unchanged_item_records, delete_item_records = list(), list()
    sort_order = False

    for opened_record in refreshed_item_records:
        item_name = opened_record.item_name
        exists_opened_record = child_opened_record_dict.pop(item_name) \
            if item_name in child_opened_record_dict else None
        # 如果当前元素存在且顺序或选中状态与新的元素不同，那么说明需要更新，将原id赋值给当前新的元素
        if exists_opened_record:
            if exists_opened_record.item_order != opened_record.item_order \
                    or exists_opened_record.checked != opened_record.checked:
                opened_record.id = exists_opened_record.id
                opened_record.expanded = exists_opened_record.expanded
                # 存储原节点顺序（方便界面定位节点），新节点数据
                update_item_records.append((exists_opened_record.item_order, opened_record))
            else:
                # 记录没有变化的元素
                unchanged_item_records.append(exists_opened_record)
            # 如果顺序不同，需要排序
            if exists_opened_record.item_order != opened_record.item_order:
                sort_order = True
            # 记录已经存在的元素（需要进行深拷贝，否则会影响其他对象），并记录新的元素顺序
            exists_opened_record_copy = copy.deepcopy(exists_opened_record)
            exists_opened_record_copy.item_order = opened_record.item_order
            exists_item_records.append(exists_opened_record_copy)
        else:
            # 如果元素不存在，则需要插入
            new_item_records.append(opened_record)
    delete_item_records = [opened_item for opened_item in child_opened_record_dict.values()]
    # 对上述集合分别处理
    if new_item_records:
        sort_order = True
        tree_item_sqlite.batch_insert(new_item_records)
    if update_item_records:
        tree_item_sqlite.batch_update([update_record_tuple[1] for update_record_tuple in update_item_records])
    if delete_item_records:
        sort_order = True
        delete_item_ids = [del_item.id for del_item in delete_item_records]
        # 倒序排列
        delete_item_records.sort(key=lambda x: x.item_order, reverse=True)
        tree_item_sqlite.delete_by_ids(delete_item_ids)
    # 发射信号
    changed_signal.emit({
        'new': new_item_records,
        'exists': update_item_records,
        'delete': delete_item_records,
        'unchanged': unchanged_item_records,
        'sort': sort_order,
        "parent_item_order": parent_item_order
    })
    return exists_item_records


@transactional
def refresh_tab_cols(db_item_record, executor, exists_records, col_signal, ds_type, emit_db_order=True):
    db_name = db_item_record.item_name
    opened_id_record_dict = {str(record.id): record for record in exists_records}
    opened_tabs = DsTableTabSqlite().select_by_opened_ids(opened_id_record_dict.keys())
    col_info_sqlite = DsTableColInfoSqlite()
    for tab in opened_tabs:
        tb_item_record = opened_id_record_dict.get(str(tab.parent_opened_id))
        columns = executor.open_tb(db_name, tb_item_record.item_name, check=False)
        col_info_sqlite.refresh_tab_cols(tab.id, columns, ds_type)
        tab.col_list = columns
        if emit_db_order:
            col_signal.emit((tab, db_item_record.item_order, tb_item_record.item_order))
        else:
            col_signal.emit((tab, tb_item_record.item_order))
