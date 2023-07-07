# -*- coding: utf-8 -*-

from PyQt6.QtCore import pyqtSignal

from src.constant.ds_dialog_constant import SAVE_CONN_SUCCESS_PROMPT, SAVE_CONN_FAIL_PROMPT
from src.constant.tree_constant import CLOSE_CONN_BOX_TITLE, DEL_CONN_BOX_TITLE, CLOSE_DB_BOX_TITLE, \
    DEL_CONN_SUCCESS_PROMPT, DEL_CONN_FAIL_PROMPT, LIST_ALL_CONN_SUCCESS_PROMPT, LIST_ALL_CONN_FAIL_PROMPT
from src.enum.common_enum import SqlTreeItemLevelEnum
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from src.service.system_storage.conn_sqlite import ConnSqlite, SqlConnection
from src.enum.conn_type_enum import get_conn_type_by_type
from src.enum.ds_category_enum import DsCategoryEnum
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from src.service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, OpenedTreeItem
from src.service.util.system_storage_util import transactional
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

    def get_err_msg(self) -> str:
        return f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}'


class AddConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, *args):
        self.connection = connection
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AddConnWorker(self.connection)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{SAVE_CONN_SUCCESS_PROMPT}',
               self.error_box_title, self.window)
        super().success_post_process(*args)


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
        ConnSqlite().delete_by_id(self.conn_id)
        # 根据连接id，删除打开记录表中的记录
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.delete_by_ids(self.delete_opened_ids)
        # 对被影响到的连接项进行重排序
        if self.reorder_items:
            opened_tree_item_sqlite.reorder_opened_items(self.reorder_items)
        if self.tab_ids:
            # 删除tab
            DsTableTabSqlite().delete_by_ids(self.tab_ids)
            # 删除 数据列信息
            DsTableColInfoSqlite().delete_by_parent_tab_ids(self.tab_ids)
        log.info(f'[{self.conn_name}]{DEL_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def get_err_msg(self) -> str:
        return f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}'


class DelConnExecutor(IconMovieThreadExecutor):

    def __init__(self, conn_id, conn_name, reorder_items,
                 tab_indexes, tab_ids, callback, item, window):
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.reorder_items = reorder_items
        self.tab_indexes = tab_indexes
        self.tab_ids = tab_ids
        self.callback = callback
        super().__init__(item, window, DEL_CONN_BOX_TITLE)

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
        ConnSqlite().update_by_id(self.connection)
        if self.name_changed:
            OpenedTreeItemSqlite().update_conn_opened_record(self.connection.id, self.connection.conn_name)
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def get_err_msg(self) -> str:
        return f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}'


class EditConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, name_changed, *args):
        self.connection = connection
        self.name_changed = name_changed
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return EditConnWorker(self.connection, self.name_changed)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{SAVE_CONN_SUCCESS_PROMPT}',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ---------------------------------------- 编辑连接 end ---------------------------------------- #


# ---------------------------------------- 获取所有连接 start ---------------------------------------- #

class ListConnWorker(ThreadWorkerABC):
    # 打开表中的查询结果
    opened_items_signal = pyqtSignal(list)
    # tab页表信息查询结果
    tab_info_signal = pyqtSignal(list)

    def do_run(self):
        # 首选读取存储的连接，这里需要连表 opened_item_sqlite 获取连接的顺序
        connections = ConnSqlite().get_conn_id_types()

        # 查询 OpenedItem
        level = SqlTreeItemLevelEnum.conn_level.value
        max_level = SqlTreeItemLevelEnum.tb_level.value
        ds_category = DsCategoryEnum.sql_ds_category.get_name()

        opened_item_sqlite = OpenedTreeItemSqlite()
        for conn in connections:
            conn_type = get_conn_type_by_type(conn.conn_type)
            # 深度优先查找
            children_generator = opened_item_sqlite.recursive_get_children(conn.id, level, ds_category, max_level)
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
        tab_list = DsTableTabSqlite().get_ds_category_tabs(DsCategoryEnum.sql_ds_category.get_name())
        col_info_sqlite = DsTableColInfoSqlite()
        for tab in tab_list:
            tab.col_list = col_info_sqlite.get_col_list_by_tab_id(tab.id)
        self.tab_info_signal.emit(tab_list)

    def get_err_msg(self) -> str:
        return LIST_ALL_CONN_FAIL_PROMPT


class ListConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, opened_items_callback, opened_tab_callback, *args):
        super().__init__(*args)

        self.worker.opened_items_signal.connect(opened_items_callback)
        self.worker.tab_info_signal.connect(opened_tab_callback)

    def get_worker(self) -> ListConnWorker:
        return ListConnWorker()


# ---------------------------------------- 获取所有连接 end ---------------------------------------- #


# ---------------------------------------- 获取连接信息 start ---------------------------------------- #

class QueryConnInfoWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(SqlConnection)

    def __init__(self, conn_id):
        super().__init__()
        self.conn_id = conn_id

    def do_run(self):
        self.success_signal.emit(ConnSqlite().get_conn_by_id(self.conn_id))

    def get_err_msg(self) -> str:
        return f'查询连接信息失败，连接id：{self.conn_id}'


class QueryConnInfoExecutor(LoadingMaskThreadExecutor):

    def __init__(self, conn_id, *args):
        self.conn_id = conn_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return QueryConnInfoWorker(self.conn_id)


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
        OpenedTreeItemSqlite().delete_by_ids(self.child_opened_ids)
        if self.tab_ids:
            # 删除tab
            DsTableTabSqlite().delete_by_ids(self.tab_ids)
            # 删除 数据列信息
            DsTableColInfoSqlite().delete_by_parent_tab_ids(self.tab_ids)
        self.success_signal.emit()

    def get_err_msg(self) -> str:
        return self.err_msg


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
        super().__init__(item, window, CLOSE_CONN_BOX_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return CloseConnDBWorker(f'{CLOSE_CONN_BOX_TITLE} [{self.conn_name}] 失败',
                                 self.child_opened_ids, self.tab_ids)

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
        super().__init__(item, window, CLOSE_DB_BOX_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return CloseConnDBWorker(f'{CLOSE_DB_BOX_TITLE} [{self.db_name}] 失败',
                                 self.child_opened_ids, self.tab_ids)

    def success_post_process(self, *args):
        self.callback(self.tab_indexes)

# ---------------------------------------- 关闭数据库 end ---------------------------------------- #
