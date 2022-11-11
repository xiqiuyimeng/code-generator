# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from service.system_storage.conn_sqlite import ConnSqlite, SqlConnection
from service.system_storage.ds_table_info_sqlite import DsTableInfoSqlite, DsTableInfo
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from service.system_storage.ds_type_sqlite import DatasourceTypeEnum
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, OpenedTreeItem, SqlTreeItemLevel, \
    CurrentEnum, ExpandedEnum
from service.system_storage.sqlite_abc import transactional
from view.box.message_box import pop_ok
from constant.constant import SAVE_CONN_TITLE, SAVE_CONN_SUCCESS_PROMPT, \
    SAVE_CONN_FAIL_PROMPT, DEL_CONN_SUCCESS_PROMPT, DEL_CONN_FAIL_PROMPT, DEL_CONN_TITLE, \
    LIST_ALL_CONN_SUCCESS_PROMPT, LIST_ALL_CONN_FAIL_PROMPT, LIST_ALL_CONN_TITLE
from view.tree.tree_widget.tree_item_func import get_children_opened_ids, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/30 20:31'


# ---------------------------------------- 添加连接 start ---------------------------------------- #

class AddConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(int, OpenedTreeItem)

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    @transactional
    def do_run(self):
        ConnSqlite().add_conn(self.connection)
        # 历史记录中的连接id
        opened_conn = self.add_opened_item(self.connection.item_order, self.connection.conn_name)
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit(self.connection.id, opened_conn)

    def add_opened_item(self, order, conn_name):
        conn_item = OpenedTreeItem()
        conn_item.item_name = conn_name
        conn_item.is_current = CurrentEnum.not_current.value
        conn_item.expanded = ExpandedEnum.collapsed.value
        conn_item.parent_id = self.connection.id
        conn_item.level = SqlTreeItemLevel.conn_level.value
        conn_item.ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        # 顺序保持与连接一致
        conn_item.item_order = order
        OpenedTreeItemSqlite().insert(conn_item)
        return conn_item

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}\n{e}')


class AddConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, masked_widget, window, callback):
        self.connection = connection
        # 回调函数
        self.callback = callback
        super().__init__(masked_widget, window, SAVE_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return AddConnWorker(self.connection)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{SAVE_CONN_SUCCESS_PROMPT}',
               SAVE_CONN_TITLE, self.window)
        self.callback(*args)

# ---------------------------------------- 添加连接 end ---------------------------------------- #


# ---------------------------------------- 编辑连接 start ---------------------------------------- #

class EditConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal()

    def __init__(self, connection: SqlConnection, name_changed: bool):
        super().__init__()
        self.connection = connection
        self.name_changed = name_changed

    @transactional
    def do_run(self):
        ConnSqlite().update(self.connection)
        if self.name_changed:
            self.update_opened_record()
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def update_opened_record(self):
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_param = OpenedTreeItem()
        opened_tree_item_param.parent_id = self.connection.id
        opened_tree_item_param.level = SqlTreeItemLevel.conn_level.value
        opened_tree_item_param.ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        opened_conn_tree_items = opened_tree_item_sqlite.select(opened_tree_item_param)
        if opened_conn_tree_items:
            opened_conn_tree_item = opened_conn_tree_items[0]
            opened_conn_tree_item.item_name = self.connection.conn_name
            opened_tree_item_sqlite.update(opened_conn_tree_item)

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}\n{e}')


class EditConnExecutor(LoadingMaskThreadExecutor):
    
    def __init__(self, connection: SqlConnection, masked_widget, window, callback, name_changed):
        self.connection = connection
        self.callback = callback
        self.name_changed = name_changed
        super().__init__(masked_widget, window, SAVE_CONN_TITLE)
        
    def get_worker(self) -> ThreadWorkerABC:
        return EditConnWorker(self.connection, self.name_changed)
    
    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{SAVE_CONN_SUCCESS_PROMPT}',
               SAVE_CONN_TITLE, self.window)
        self.callback()

# ---------------------------------------- 编辑连接 end ---------------------------------------- #


# ---------------------------------------- 删除连接 start ---------------------------------------- #

class DelConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal()
    
    def __init__(self, conn_id, conn_name, reorder_conns, reorder_items, delete_opened_ids):
        super().__init__()
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.reorder_conns = reorder_conns
        self.reorder_items = reorder_items
        self.delete_opened_ids = delete_opened_ids

    @transactional
    def do_run(self):
        conn_sqlite = ConnSqlite()
        conn_sqlite.delete(self.conn_id)
        # 根据连接id，删除打开记录表中的记录
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.batch_delete(self.delete_opened_ids)
        # 对被影响到的连接项进行重排序
        if self.reorder_conns:
            conn_sqlite.batch_update(self.reorder_conns)
            self.reorder_items[0].is_current = 1
            for item in self.reorder_items[1:]:
                item.is_current = 0
            opened_tree_item_sqlite.batch_update(self.reorder_items)
        log.info(f'[{self.conn_name}]{DEL_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.exception(f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}\n{e}')


class DelConnExecutor(IconMovieThreadExecutor):

    def __init__(self, conn_id, conn_name, item, window, callback,
                 need_reorder_items, reorder_conns, reorder_items):
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.callback = callback
        self.need_reorder_items = need_reorder_items
        self.reorder_conns = reorder_conns
        self.reorder_items = reorder_items
        super().__init__(item, window, DEL_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        # 获取要删除的节点对象
        conn_opened_record = get_item_opened_record(self.item)
        # 获取子节点所有id
        delete_opened_ids = get_children_opened_ids(self.item)
        delete_opened_ids.append(conn_opened_record.id)
        return DelConnWorker(self.conn_id, self.conn_name, self.reorder_conns, self.reorder_items, delete_opened_ids)

    def success_post_process(self, *args):
        self.callback(self.need_reorder_items)

# ---------------------------------------- 删除连接 end ---------------------------------------- #


# ---------------------------------------- 获取所有连接 start ---------------------------------------- #

class ListConnWorker(ThreadWorkerABC):

    # 连接表中查询结果
    conn_list_signal = pyqtSignal(list)
    # 打开表中的查询结果
    opened_items_signal = pyqtSignal(list)
    # tab页表信息查询结果
    tab_info_signal = pyqtSignal(list)

    success_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def do_run(self):
        # 首选读取存储的连接信息
        connections = ConnSqlite().select_by_order(SqlConnection())
        self.conn_list_signal.emit(connections)

        # 查询 OpenedItem
        level = SqlTreeItemLevel.conn_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        for conn in connections:
            # 从打开记录中查询连接，正常来说，一定可以查到，并且应该只有一条数据
            children_generator = OpenedTreeItemSqlite().recursive_get_children(conn.id, level, ds_type)
            for children in children_generator:
                self.opened_items_signal.emit(children)
        # 查找tab页信息
        self.get_tab_cols()
        log.info(LIST_ALL_CONN_SUCCESS_PROMPT)

    def do_finally(self):
        self.success_signal.emit()
        
    def get_tab_cols(self):
        tab_param = DsTableTab()
        tab_param.ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        tab_list = DsTableTabSqlite().select_by_order(tab_param)
        for tab in tab_list:
            col_param = DsTableInfo()
            col_param.parent_tab_id = tab.id
            tab.col_list = DsTableInfoSqlite().select_by_order(col_param)
        self.tab_info_signal.emit(tab_list)

    def do_exception(self, e: Exception):
        log.exception(LIST_ALL_CONN_FAIL_PROMPT)
        self.error_signal.emit(f'{LIST_ALL_CONN_FAIL_PROMPT}\n{e}')


class ListConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, masked_widget, window, conn_list_callback, opened_items_callback,
                 opened_tab_callback, reopen_end_callback):
        self.reopen_end_callback = reopen_end_callback
        super().__init__(masked_widget, window, LIST_ALL_CONN_TITLE)

        self.conn_list_callback = conn_list_callback
        self.opened_items_callback = opened_items_callback
        self.opened_tab_callback = opened_tab_callback

        self.worker.conn_list_signal.connect(self.conn_list_callback)
        self.worker.opened_items_signal.connect(self.opened_items_callback)
        self.worker.tab_info_signal.connect(self.opened_tab_callback)

    def get_worker(self) -> ListConnWorker:
        return ListConnWorker()

    def success_post_process(self):
        self.reopen_end_callback()

    def fail_post_process(self):
        self.reopen_end_callback()

# ---------------------------------------- 获取所有连接 end ---------------------------------------- #

