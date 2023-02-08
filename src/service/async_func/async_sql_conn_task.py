# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from src.constant.constant import SAVE_CONN_TITLE, SAVE_CONN_SUCCESS_PROMPT, \
    SAVE_CONN_FAIL_PROMPT, DEL_CONN_SUCCESS_PROMPT, DEL_CONN_FAIL_PROMPT, DEL_CONN_TITLE, \
    LIST_ALL_CONN_SUCCESS_PROMPT, LIST_ALL_CONN_FAIL_PROMPT, LIST_ALL_CONN_TITLE
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from src.service.system_storage.conn_sqlite import ConnSqlite, SqlConnection
from src.service.system_storage.conn_type import get_conn_type_by_type
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite, DsTableColInfo
from src.service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from src.service.system_storage.ds_type_sqlite import DatasourceTypeEnum
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, OpenedTreeItem, SqlTreeItemLevel
from src.service.system_storage.sqlite_abc import transactional
from src.view.box.message_box import pop_ok
from src.view.tree.tree_item.tree_item_func import get_children_opened_ids, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/30 20:31'


# ---------------------------------------- 添加连接 start ---------------------------------------- #

class AddConnWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(OpenedTreeItem)

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    @transactional
    def do_run(self):
        ConnSqlite().insert(self.connection)
        # 历史记录中的连接id
        opened_conn = OpenedTreeItemSqlite().add_conn_opened_item(self.connection.id,
                                                                  self.connection.conn_name)
        opened_conn.data_type = get_conn_type_by_type(self.connection.conn_type)
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit(opened_conn)

    def do_exception(self, e: Exception):
        err_msg = f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


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


# ---------------------------------------- 删除连接 start ---------------------------------------- #

class DelConnWorker(ThreadWorkerABC):

    def __init__(self, conn_id, conn_name, reorder_items, delete_opened_ids, tab_ids):
        super().__init__()
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.reorder_items = reorder_items
        self.delete_opened_ids = delete_opened_ids
        self.tab_ids = tab_ids

    @transactional
    def do_run(self):
        # 删除连接
        ConnSqlite().delete(self.conn_id)
        # 根据连接id，删除打开记录表中的记录
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.batch_delete(self.delete_opened_ids)
        # 对被影响到的连接项进行重排序
        if self.reorder_items:
            opened_tree_item_sqlite.reorder_opened_items(self.reorder_items)
        if self.tab_ids:
            # 删除tab
            DsTableTabSqlite().batch_delete(self.tab_ids)
            # 删除 数据列信息
            DsTableColInfoSqlite().delete_by_parent_tab_ids(self.tab_ids)
        log.info(f'[{self.conn_name}]{DEL_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class DelConnExecutor(IconMovieThreadExecutor):

    def __init__(self, conn_id, conn_name, reorder_items,
                 tab_indexes, tab_ids, callback, item, window):
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.reorder_items = reorder_items
        self.tab_indexes = tab_indexes
        self.tab_ids = tab_ids
        self.callback = callback
        super().__init__(item, window, DEL_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        # 获取要删除的节点对象
        conn_opened_record = get_item_opened_record(self.item)
        # 获取子节点所有id
        delete_opened_ids = get_children_opened_ids(self.item)
        delete_opened_ids.append(conn_opened_record.id)
        return DelConnWorker(self.conn_id, self.conn_name, self.reorder_items,
                             delete_opened_ids, self.tab_ids)

    def success_post_process(self, *args):
        self.callback(self.tab_indexes)


# ---------------------------------------- 删除连接 end ---------------------------------------- #


# ---------------------------------------- 编辑连接 start ---------------------------------------- #

class EditConnWorker(ThreadWorkerABC):

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
        opened_conn_tree_item = opened_tree_item_sqlite.select_one(opened_tree_item_param)
        if opened_tree_item_param:
            opened_conn_tree_item.item_name = self.connection.conn_name
            opened_tree_item_sqlite.update(opened_conn_tree_item)

    def do_exception(self, e: Exception):
        err_msg = f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


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


# ---------------------------------------- 获取所有连接 start ---------------------------------------- #

class ListConnWorker(ThreadWorkerABC):
    # 打开表中的查询结果
    opened_items_signal = pyqtSignal(list)
    # tab页表信息查询结果
    tab_info_signal = pyqtSignal(list)

    def do_run(self):
        # 首选读取存储的连接，这里需要连表 opened_tree_item_sqlite 获取连接的顺序
        connections = ConnSqlite().get_conn_id_types()

        # 查询 OpenedItem
        level = SqlTreeItemLevel.conn_level.value
        max_level = SqlTreeItemLevel.tb_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name

        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        for conn in connections:
            conn_type = get_conn_type_by_type(conn.conn_type)
            # 深度优先查找
            children_generator = opened_tree_item_sqlite.recursive_get_children(conn.id, level,
                                                                                ds_type, max_level)
            for children in children_generator:
                for child in children:
                    child.data_type = conn_type
                self.opened_items_signal.emit(children)
        # 查找tab页信息
        self.get_tab_cols()
        log.info(LIST_ALL_CONN_SUCCESS_PROMPT)

    def do_finally(self):
        # 结束信号
        self.success_signal.emit()

    def get_tab_cols(self):
        tab_param = DsTableTab()
        tab_param.ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        tab_list = DsTableTabSqlite().select_by_order(tab_param)
        for tab in tab_list:
            col_param = DsTableColInfo()
            col_param.parent_tab_id = tab.id
            tab.col_list = DsTableColInfoSqlite().select_by_order(col_param)
        self.tab_info_signal.emit(tab_list)

    def do_exception(self, e: Exception):
        err_msg = LIST_ALL_CONN_FAIL_PROMPT
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, masked_widget, window, opened_items_callback,
                 opened_tab_callback, reopen_end_callback):
        self.reopen_end_callback = reopen_end_callback
        super().__init__(masked_widget, window, LIST_ALL_CONN_TITLE)

        self.worker.opened_items_signal.connect(opened_items_callback)
        self.worker.tab_info_signal.connect(opened_tab_callback)

    def get_worker(self) -> ListConnWorker:
        return ListConnWorker()

    def success_post_process(self):
        self.reopen_end_callback()

    def fail_post_process(self):
        self.reopen_end_callback()

# ---------------------------------------- 获取所有连接 end ---------------------------------------- #


# ---------------------------------------- 获取连接信息 start ---------------------------------------- #

class QueryConnInfoWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(SqlConnection)

    def __init__(self, conn_id):
        super().__init__()
        self.conn_id = conn_id

    def do_run(self):
        conn_param = SqlConnection()
        conn_param.id = self.conn_id
        self.success_signal.emit(ConnSqlite().select_one(conn_param))

    def do_exception(self, e: Exception):
        err_msg = f'查询连接信息失败，连接id：{self.conn_id}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class QueryConnInfoExecutor(LoadingMaskThreadExecutor):

    def __init__(self, conn_id, callback, masked_widget, window):
        self.conn_id = conn_id
        self.callback = callback
        super().__init__(masked_widget, window, '查询连接信息')

    def get_worker(self) -> ThreadWorkerABC:
        return QueryConnInfoWorker(self.conn_id)

    def success_post_process(self, *args):
        self.callback(*args)


# ---------------------------------------- 获取连接信息 end ---------------------------------------- #

# ---------------------------------------- 关闭连接 start ---------------------------------------- #

class CloseConnDBWorker(ThreadWorkerABC):

    def __init__(self, err_msg, child_opened_ids, tab_ids):
        super().__init__()
        self.err_msg = err_msg
        self.child_opened_ids = child_opened_ids
        self.tab_ids = tab_ids

    @transactional
    def do_run(self):
        # 首先删除 opened item 表
        OpenedTreeItemSqlite().batch_delete(self.child_opened_ids)
        if self.tab_ids:
            # 删除tab
            DsTableTabSqlite().batch_delete(self.tab_ids)
            # 删除 数据列信息
            DsTableColInfoSqlite().delete_by_parent_tab_ids(self.tab_ids)
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.exception(self.err_msg)
        self.error_signal.emit(f'{self.error_signal}\n{e.args[0]}')


class CloseConnExecutor(IconMovieThreadExecutor):

    def __init__(self, conn_id, conn_name, child_opened_ids,
                 tab_indexes, tab_ids, close_for_edit, item,
                 window, callback):
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.child_opened_ids = child_opened_ids
        self.tab_indexes = tab_indexes
        self.tab_ids = tab_ids
        self.close_for_edit = close_for_edit
        self.callback = callback
        super().__init__(item, window, '关闭连接')

    def get_worker(self) -> ThreadWorkerABC:
        return CloseConnDBWorker(f'关闭连接 [{self.conn_name}] 失败', self.child_opened_ids, self.tab_ids)

    def success_post_process(self, *args):
        self.callback(self.tab_indexes, self.close_for_edit)

# ---------------------------------------- 关闭连接 end ---------------------------------------- #


# ---------------------------------------- 关闭数据库 start ---------------------------------------- #

class CloseDBExecutor(IconMovieThreadExecutor):

    def __init__(self, db_name, child_opened_ids, tab_indexes,
                 tab_ids, item, window, callback):
        self.db_name = db_name
        self.child_opened_ids = child_opened_ids
        self.tab_indexes = tab_indexes
        self.tab_ids = tab_ids
        self.callback = callback
        super().__init__(item, window, '关闭数据库')

    def get_worker(self) -> ThreadWorkerABC:
        return CloseConnDBWorker(f'关闭数据库 [{self.db_name}] 失败', self.child_opened_ids, self.tab_ids)

    def success_post_process(self, *args):
        self.callback(self.tab_indexes)

# ---------------------------------------- 关闭数据库 end ---------------------------------------- #
