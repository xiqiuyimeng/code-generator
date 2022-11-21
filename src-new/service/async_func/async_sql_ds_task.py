# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from constant.constant import TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT, TEST_CONN_TITLE, OPEN_CONN_TITLE, \
    OPEN_CONN_SUCCESS_PROMPT, OPEN_CONN_FAIL_PROMPT, OPEN_DB_SUCCESS_PROMPT, OPEN_DB_FAIL_PROMPT, OPEN_DB_TITLE, \
    OPEN_TB_TITLE, OPEN_TB_SUCCESS_PROMPT, OPEN_TB_FAIL_PROMPT
from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from service.sql_ds_executor import *
from service.system_storage.conn_sqlite import SqlConnection
from service.system_storage.conn_type import get_conn_type_by_type
from service.system_storage.ds_table_info_sqlite import DsTableInfoSqlite
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from service.system_storage.ds_type_sqlite import DatasourceTypeEnum
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, SqlTreeItemLevel
from service.system_storage.sqlite_abc import transactional
from view.box.message_box import pop_ok
from view.tree.tree_item.tree_item_func import get_item_sql_conn, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/31 19:05'


class SqlDSIconMovieThreadExecutor(IconMovieThreadExecutor):

    def __init__(self, item, window, error_box_title, success_callback, fail_callback):
        self.success_callback = success_callback
        self.fail_callback = fail_callback
        super().__init__(item, window, error_box_title)

    def success_post_process(self, *args):
        self.success_callback(*args)

    def fail_post_process(self):
        self.fail_callback()


# ---------------------------------------- 测试连接 start ---------------------------------------- #

class TestConnWorker(ThreadWorkerABC):
    success_signal = pyqtSignal()

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    def do_run(self):
        db_executor_class = get_conn_type_by_type(self.connection.conn_type).db_executor
        executor: SqlDBExecutor = globals()[db_executor_class](self.connection)
        executor.test_conn()
        log.info(f'[{self.connection.conn_name}]{TEST_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}]{TEST_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{TEST_CONN_FAIL_PROMPT}\n'
                               f'{e.orig.original_exception.strerror}')


class TestConnLoadingMaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, masked_widget, window):
        self.connection = connection
        super().__init__(masked_widget, window, TEST_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(self.connection)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}',
               TEST_CONN_TITLE, self.window)


class TestConnIconMovieExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, TEST_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(get_item_sql_conn(self.item))


# ---------------------------------------- 测试连接 end ---------------------------------------- #


# ---------------------------------------- 打开连接 start ---------------------------------------- #

class OpenConnWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, connection: SqlConnection, opened_conn_id):
        super().__init__()
        self.connection = connection
        self.opened_conn_id = opened_conn_id

    def do_run(self):
        db_executor_class = get_conn_type_by_type(self.connection.conn_type).db_executor
        executor: SqlDBExecutor = globals()[db_executor_class](self.connection)
        db_names = executor.open_conn()
        db_opened_items = self.save_opened_items(db_names)
        self.success_signal.emit(db_opened_items)
        log.info(f'[{self.connection.conn_name}]{OPEN_CONN_SUCCESS_PROMPT} ==> {db_names}')

    def save_opened_items(self, db_names):
        log.info(f"保存打开连接[{self.connection.conn_name}]下的库名列表")
        # 更新连接节点为展开状态，当前项
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.open_item(self.opened_conn_id)
        # 添加库节点
        db_level = SqlTreeItemLevel.db_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        return opened_tree_item_sqlite.add_opened_child_item(db_names, self.opened_conn_id,
                                                             db_level, ds_type)

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}]{OPEN_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{OPEN_CONN_FAIL_PROMPT}\n'
                               f'{e.orig.original_exception.strerror}')


class OpenConnExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenConnWorker(get_item_sql_conn(self.item), get_item_opened_record(self.item).id)


# ---------------------------------------- 打开连接 end ---------------------------------------- #


# ---------------------------------------- 打开数据库 start ---------------------------------------- #

class OpenDBWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, connection: SqlConnection, db_name, opened_db_id):
        super().__init__()
        self.connection = connection
        self.db_name = db_name
        self.opened_db_id = opened_db_id

    def do_run(self):
        db_executor_class = get_conn_type_by_type(self.connection.conn_type).db_executor
        executor: SqlDBExecutor = globals()[db_executor_class](self.connection)
        tb_names = executor.open_db(self.db_name)
        tb_opened_items = self.save_opened_items(tb_names)
        self.success_signal.emit(tb_opened_items)
        log.info(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_SUCCESS_PROMPT} ==> {tb_names}')

    def save_opened_items(self, tb_names):
        log.info(f"保存打开库[{self.db_name}]下的表名列表")
        # 更新库节点
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.open_item(self.opened_db_id)
        # 添加表节点
        tb_level = SqlTreeItemLevel.tb_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        return opened_tree_item_sqlite.add_opened_child_item(tb_names, self.opened_db_id,
                                                             tb_level, ds_type)

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_FAIL_PROMPT}\n{e}')


class OpenDBExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_DB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenDBWorker(get_item_sql_conn(self.item.parent()), self.item.text(0),
                            get_item_opened_record(self.item).id)


# ---------------------------------------- 打开数据库 end ---------------------------------------- #


# ---------------------------------------- 打开数据表 start ---------------------------------------- #

class OpenTBWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, connection: SqlConnection, db_name, tb_name, opened_table_item, check_state):
        super().__init__()
        self.connection = connection
        self.db_name = db_name
        self.tb_name = tb_name
        self.opened_table_item = opened_table_item
        self.check_state = check_state

    def do_run(self):
        db_executor_class = get_conn_type_by_type(self.connection.conn_type).db_executor
        executor: SqlDBExecutor = globals()[db_executor_class](self.connection)
        columns = executor.open_tb(self.db_name, self.tb_name)
        table_tab = self.save_opened_items(columns)
        log.info(f'[{self.connection.conn_name}][{self.db_name}][{self.tb_name}]{OPEN_TB_SUCCESS_PROMPT}'
                 f' ==> {columns}')
        self.success_signal.emit(table_tab)

    @transactional
    def save_opened_items(self, columns):
        log.info(f"保存打开表[{self.db_name}][{self.tb_name}]下的列信息")
        # 存储tab信息
        table_tab = DsTableTabSqlite().add_tab(self.opened_table_item)
        # 存储列信息
        DsTableInfoSqlite().add_table(columns, table_tab.id, self.check_state)
        table_tab.col_list = columns
        return table_tab

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}][{self.db_name}][{self.tb_name}]{OPEN_TB_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}][{self.db_name}]'
                               f'[{self.tb_name}]{OPEN_TB_FAIL_PROMPT}\n{e}')


class OpenTBExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_TB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenTBWorker(get_item_sql_conn(self.item.parent().parent()),
                            self.item.parent().text(0), self.item.text(0),
                            get_item_opened_record(self.item), self.item.checkState(0))

# ---------------------------------------- 打开数据表 end ---------------------------------------- #
