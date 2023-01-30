# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from constant.constant import TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT, TEST_CONN_TITLE, OPEN_CONN_TITLE, \
    OPEN_CONN_SUCCESS_PROMPT, OPEN_CONN_FAIL_PROMPT, OPEN_DB_SUCCESS_PROMPT, OPEN_DB_FAIL_PROMPT, OPEN_DB_TITLE, \
    OPEN_TB_TITLE, OPEN_TB_SUCCESS_PROMPT, OPEN_TB_FAIL_PROMPT, REFRESH_TB_SUCCESS_PROMPT, REFRESH_TB_FAIL_PROMPT, \
    REFRESH_TB_TITLE, REFRESH_DB_TITLE, REFRESH_DB_SUCCESS_PROMPT, REFRESH_DB_FAIL_PROMPT, REFRESH_CONN_TITLE, \
    REFRESH_CONN_SUCCESS_PROMPT, REFRESH_CONN_FAIL_PROMPT
from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor, \
    IconMovieLoadingMaskThreadExecutor
from service.sql_ds_executor import *
from service.system_storage.conn_sqlite import SqlConnection, ConnSqlite
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from service.system_storage.ds_type_sqlite import DatasourceTypeEnum
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, SqlTreeItemLevel, OpenedTreeItem
from service.system_storage.sqlite_abc import transactional
from service.util.refresh_util import deal_opened_items, refresh_tab_cols
from view.box.message_box import pop_ok
from view.tree.tree_item.tree_item_func import get_item_opened_record, get_item_opened_tab

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


class ConnWorkerABC(ThreadWorkerABC):

    def __init__(self, conn_opened_item: OpenedTreeItem, connection: SqlConnection = None):
        super().__init__()
        self.conn_opened_item = conn_opened_item
        self.connection = connection

    def do_run(self):
        db_executor_class = self.conn_opened_item.data_type.db_executor
        # 获取连接对象，如果没有传进来，从数据库获取
        if not self.connection:
            conn_param = SqlConnection()
            conn_param.id = self.conn_opened_item.parent_id
            self.connection = ConnSqlite().select(conn_param)[0]
        executor: SqlDBExecutor = globals()[db_executor_class](self.connection)
        # 实际的功能实现
        self.do_executor_func(executor)

    def do_executor_func(self, executor: SqlDBExecutor): ...


# ---------------------------------------- 测试连接 start ---------------------------------------- #

class TestConnWorker(ConnWorkerABC):

    def do_executor_func(self, executor):
        executor.test_conn()
        log.info(f'[{self.conn_opened_item.item_name}]{TEST_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}]{TEST_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class TestConnLoadingMaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, conn_type, masked_widget, window):
        self.connection = connection
        # 临时创建一个 opened item 使用
        self.opened_record = OpenedTreeItem()
        self.opened_record.data_type = conn_type
        super().__init__(masked_widget, window, TEST_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(self.opened_record, self.connection)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}',
               TEST_CONN_TITLE, self.window)


class TestConnIconMovieExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, TEST_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(get_item_opened_record(self.item))


# ---------------------------------------- 测试连接 end ---------------------------------------- #


# ---------------------------------------- 打开连接 start ---------------------------------------- #

class OpenConnWorker(ConnWorkerABC):
    success_signal = pyqtSignal(list)

    def do_executor_func(self, executor: SqlDBExecutor):
        db_names = executor.open_conn()
        self.modifying_db_task = True
        db_opened_items = self.save_opened_items(db_names)
        self.modifying_db_task = False
        self.success_signal.emit(db_opened_items)
        log.info(f'[{self.conn_opened_item.item_name}]{OPEN_CONN_SUCCESS_PROMPT} ==> {db_names}')

    @transactional
    def save_opened_items(self, db_names):
        log.info(f"保存打开连接[{self.conn_opened_item.item_name}]下的库名列表")
        # 更新连接节点为展开状态，当前项
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.open_item(self.conn_opened_item.id)
        # 添加库节点
        db_level = SqlTreeItemLevel.db_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        return opened_tree_item_sqlite.add_opened_child_item(db_names, self.conn_opened_item.id, db_level,
                                                             ds_type, self.conn_opened_item.data_type)

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}]{OPEN_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class OpenConnExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenConnWorker(get_item_opened_record(self.item))


# ---------------------------------------- 打开连接 end ---------------------------------------- #

# ---------------------------------------- 刷新连接 start ---------------------------------------- #

class RefreshConnWorker(ConnWorkerABC):
    success_signal = pyqtSignal()
    db_changed_signal = pyqtSignal(dict)
    db_finished_signal = pyqtSignal(int)
    table_changed_signal = pyqtSignal(dict)
    col_signal = pyqtSignal(DsTableTab)

    def __init__(self, conn_opened_item: OpenedTreeItem):
        super().__init__(conn_opened_item)

    def do_executor_func(self, executor: SqlDBExecutor):
        # 读取连接下的库名列表
        db_names = executor.open_conn()
        self.modifying_db_task = True
        data_type = self.conn_opened_item.data_type
        level = SqlTreeItemLevel.db_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        exists_db_items = deal_opened_items(db_names, self.conn_opened_item.id, data_type,
                                            level, ds_type, self.db_changed_signal)

        # 读取库下的表名列表
        if exists_db_items:
            for exists_db_item in exists_db_items:
                self.refresh_db(executor, exists_db_item, data_type)
        self.modifying_db_task = False
        self.success_signal.emit()
        log.info(f'[{self.conn_opened_item.item_name}]{REFRESH_CONN_SUCCESS_PROMPT}')

    def refresh_db(self, executor, db_item, data_type):
        tree_item_sqlite = OpenedTreeItemSqlite()
        # 获取本地库中缓存的数据
        level = SqlTreeItemLevel.tb_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        child_opened_items = tree_item_sqlite.get_children(db_item.id, level, ds_type)
        # 如果之前没有子节点，那么不需要进行刷新处理
        if not child_opened_items:
            return
        tb_names = executor.open_db(db_item.item_name)
        exists_items = deal_opened_items(tb_names, db_item.id, data_type,
                                         level, ds_type, self.table_changed_signal)
        if exists_items:
            refresh_tab_cols(db_item.item_name, executor, exists_items, self.col_signal)
        # 库刷新完成，发射信号
        self.db_finished_signal.emit(db_item.id)

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}]{REFRESH_CONN_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class RefreshConnExecutor(IconMovieLoadingMaskThreadExecutor):

    def __init__(self, item, window, db_changed_callback, tb_changed_callback, col_changed_callback,
                 db_finished_callback, success_callback, fail_callback):
        super().__init__(item, success_callback, fail_callback, window, REFRESH_CONN_TITLE)

        self.worker.db_changed_signal.connect(db_changed_callback)
        self.worker.table_changed_signal.connect(tb_changed_callback)
        self.worker.col_signal.connect(col_changed_callback)
        self.worker.db_finished_signal.connect(db_finished_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return RefreshConnWorker(get_item_opened_record(self.item))

# ---------------------------------------- 刷新连接 end ---------------------------------------- #


# ---------------------------------------- 打开数据库 start ---------------------------------------- #

class OpenDBWorker(ConnWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, conn_opened_item: OpenedTreeItem, db_name, opened_db_id):
        super().__init__(conn_opened_item)
        self.db_name = db_name
        self.opened_db_id = opened_db_id

    def do_executor_func(self, executor: SqlDBExecutor):
        tb_names = executor.open_db(self.db_name)
        tb_opened_items = list()
        if tb_names:
            self.modifying_db_task = True
            tb_opened_items = self.save_opened_items(tb_names)
            self.modifying_db_task = False
        self.success_signal.emit(tb_opened_items)
        log.info(f'[{self.conn_opened_item.item_name}][{self.db_name}]{OPEN_DB_SUCCESS_PROMPT} ==> {tb_names}')

    @transactional
    def save_opened_items(self, tb_names):
        log.info(f"保存打开库[{self.db_name}]下的表名列表")
        # 更新库节点
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.open_item(self.opened_db_id)
        # 添加表节点
        tb_level = SqlTreeItemLevel.tb_level.value
        ds_type = DatasourceTypeEnum.sql_ds_type.value.name
        return opened_tree_item_sqlite.add_opened_child_item(tb_names, self.opened_db_id, tb_level,
                                                             ds_type, self.conn_opened_item.data_type)

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}][{self.db_name}]{OPEN_DB_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class OpenDBExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_DB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenDBWorker(get_item_opened_record(self.item.parent()), self.item.text(0),
                            get_item_opened_record(self.item).id)


# ---------------------------------------- 打开数据库 end ---------------------------------------- #


# ---------------------------------------- 刷新数据库 start ---------------------------------------- #

class RefreshDBWorker(ConnWorkerABC):
    success_signal = pyqtSignal()
    table_changed_signal = pyqtSignal(dict)
    col_signal = pyqtSignal(DsTableTab)

    def __init__(self, conn_opened_item: OpenedTreeItem, db_name, opened_db_id, child_count):
        super().__init__(conn_opened_item)
        self.db_name = db_name
        self.opened_db_id = opened_db_id
        self.child_count = child_count

    def do_executor_func(self, executor: SqlDBExecutor):
        if self.child_count:
            # 读取库下最新的表名列表
            tb_names = executor.open_db(self.db_name)
            self.modifying_db_task = True
            data_type = self.conn_opened_item.data_type
            level = SqlTreeItemLevel.tb_level.value
            ds_type = DatasourceTypeEnum.sql_ds_type.value.name
            exists_items = deal_opened_items(tb_names, self.opened_db_id, data_type,
                                             level, ds_type, self.table_changed_signal)

            # 接下来处理数据表列信息，将每一个打开的数据表列信息进行刷新
            if exists_items:
                refresh_tab_cols(self.db_name, executor, exists_items, self.col_signal)
            self.modifying_db_task = False
            log.info(f'[{self.conn_opened_item.item_name}][{self.db_name}]{REFRESH_DB_SUCCESS_PROMPT} ==> {tb_names}')
        else:
            # 只检查库
            executor.check_db(self.db_name)
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}][{self.db_name}]{REFRESH_DB_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class RefreshDBExecutor(IconMovieLoadingMaskThreadExecutor):

    def __init__(self, item, window, tb_changed_callback, col_changed_callback,
                 success_callback, fail_callback):
        super().__init__(item, success_callback, fail_callback, window, REFRESH_DB_TITLE)

        self.worker.table_changed_signal.connect(tb_changed_callback)
        self.worker.col_signal.connect(col_changed_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return RefreshDBWorker(get_item_opened_record(self.item.parent()), self.item.text(0),
                               get_item_opened_record(self.item).id, self.item.childCount())


# ---------------------------------------- 刷新数据库 end ---------------------------------------- #


# ---------------------------------------- 打开数据表 start ---------------------------------------- #

class OpenTBWorker(ConnWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, conn_opened_item: OpenedTreeItem, db_name, tb_name,
                 opened_table_item, check_state):
        super().__init__(conn_opened_item)
        self.db_name = db_name
        self.tb_name = tb_name
        self.opened_table_item = opened_table_item
        self.check_state = check_state

    def do_executor_func(self, executor: SqlDBExecutor):
        columns = executor.open_tb(self.db_name, self.tb_name)
        table_tab = self.save_opened_items(columns)
        log.info(f'[{self.conn_opened_item.item_name}][{self.db_name}][{self.tb_name}]'
                 f'{OPEN_TB_SUCCESS_PROMPT} ==> {columns}')
        self.success_signal.emit(table_tab)

    @transactional
    def save_opened_items(self, columns):
        log.info(f"保存打开表[{self.db_name}][{self.tb_name}]下的列信息")
        self.modifying_db_task = True
        # 存储tab信息
        table_tab = DsTableTabSqlite().add_tab(self.opened_table_item)
        # 存储列信息
        DsTableColInfoSqlite().save_cols(columns, table_tab.id, self.check_state)
        self.modifying_db_task = False
        table_tab.col_list = columns
        return table_tab

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}][{self.db_name}][{self.tb_name}]' \
                  f'{OPEN_TB_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class OpenTBExecutor(SqlDSIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_TB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenTBWorker(get_item_opened_record(self.item.parent().parent()),
                            self.item.parent().text(0), self.item.text(0),
                            get_item_opened_record(self.item), self.item.checkState(0))

# ---------------------------------------- 打开数据表 end ---------------------------------------- #


# ---------------------------------------- 刷新数据表 start ---------------------------------------- #

class RefreshTBWorker(ConnWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, tab, conn_opened_item: OpenedTreeItem, db_name, tb_name,
                 opened_table_item):
        super().__init__(conn_opened_item)
        self.db_name = db_name
        self.tb_name = tb_name
        self.opened_table_item = opened_table_item
        self.tab = tab

    @transactional
    def do_executor_func(self, executor: SqlDBExecutor):
        # 首先检查表本身是否存在
        executor.check_tb(self.db_name, self.tb_name)
        # 如果表之前tab页已经打开，尝试获取新的列数据
        if self.tab:
            columns = executor.open_tb(self.db_name, self.tb_name, check=False)
            self.tab.col_list = columns
            # 获取成功后，删除原数据
            self.modifying_db_task = True
            # 保存新的数据，并发射信号
            DsTableColInfoSqlite().refresh_tab_cols(self.tab.id, columns)
            self.modifying_db_task = False
            log.info(f'[{self.conn_opened_item.item_name}][{self.db_name}][{self.tb_name}]'
                     f'{REFRESH_TB_SUCCESS_PROMPT} ==> {columns}')
            self.success_signal.emit(self.tab)
        else:
            self.success_signal.emit(DsTableTab())

    def do_exception(self, e: Exception):
        err_msg = f'[{self.conn_opened_item.item_name}][{self.db_name}][{self.tb_name}]' \
                  f'{REFRESH_TB_FAIL_PROMPT}'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class RefreshTBExecutor(IconMovieLoadingMaskThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, success_callback, fail_callback, window, REFRESH_TB_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        tab = get_item_opened_tab(self.item)
        return RefreshTBWorker(tab.table_tab if tab else None,
                               get_item_opened_record(self.item.parent().parent()),
                               self.item.parent().text(0), self.item.text(0),
                               get_item_opened_record(self.item))


# ---------------------------------------- 刷新数据表 end ---------------------------------------- #
