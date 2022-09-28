# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt

from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from service.db_operator.db_executor import DBExecutor
from logger.log import logger as log
from service.system_storage.conn_sqlite import SqlConnection
from view.box.message_box import pop_ok
from constant.constant import TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT, TEST_CONN_TITLE, OPEN_CONN_TITLE, \
    OPEN_CONN_SUCCESS_PROMPT, OPEN_CONN_FAIL_PROMPT, OPEN_DB_SUCCESS_PROMPT, OPEN_DB_FAIL_PROMPT, OPEN_DB_TITLE, \
    OPEN_TB_TITLE, OPEN_TB_SUCCESS_PROMPT, OPEN_TB_FAIL_PROMPT

_author_ = 'luwt'
_date_ = '2022/5/31 19:05'


class MysqlIconMovieThreadExecutor(IconMovieThreadExecutor):

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
        with DBExecutor(*self.connection[1:]) as executor:
            executor.test_conn()
            log.info(f'[{self.connection.conn_name}]{TEST_CONN_SUCCESS_PROMPT}')
            self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.error(f'[{self.connection.conn_name}]{TEST_CONN_FAIL_PROMPT} --> {e}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{TEST_CONN_FAIL_PROMPT}\n{e}')


class TestConnLoadingMaskExecutor(LoadingMaskThreadExecutor):

    def __init__(self, connection: SqlConnection, masked_widget, window):
        self.connection = connection
        super().__init__(masked_widget, window, TEST_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(self.connection)

    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{TEST_CONN_SUCCESS_PROMPT}',
               TEST_CONN_TITLE, self.window)


class TestConnIconMovieExecutor(MysqlIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, TEST_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return TestConnWorker(self.item.data(0, Qt.UserRole))

# ---------------------------------------- 测试连接 end ---------------------------------------- #


# ---------------------------------------- 打开连接 start ---------------------------------------- #

class OpenConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(tuple)

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    def do_run(self):
        with DBExecutor(*self.connection[1:]) as executor:
            dbs = executor.open_conn()
            self.success_signal.emit(dbs)
            log.info(f'[{self.connection.conn_name}]{OPEN_CONN_SUCCESS_PROMPT} ==> {dbs}')

    def do_exception(self, e: Exception):
        log.error(f'[{self.connection.conn_name}]{OPEN_CONN_FAIL_PROMPT} --> {e}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{OPEN_CONN_FAIL_PROMPT}\n{e}')


class OpenConnExecutor(MysqlIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_CONN_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenConnWorker(self.item.data(0, Qt.UserRole))

# ---------------------------------------- 打开连接 end ---------------------------------------- #


# ---------------------------------------- 打开数据库 start ---------------------------------------- #

class OpenDBWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(tuple)

    def __init__(self, connection: SqlConnection, db_name):
        super().__init__()
        self.connection = connection
        self.db_name = db_name

    def do_run(self):
        with DBExecutor(*self.connection[1:]) as executor:
            tables = executor.open_db(self.db_name)
            self.success_signal.emit(tables)
            log.info(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_SUCCESS_PROMPT} ==> {tables}')

    def do_exception(self, e: Exception):
        log.error(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_FAIL_PROMPT} --> {e}')
        self.error_signal.emit(f'[{self.connection.conn_name}][{self.db_name}]{OPEN_DB_FAIL_PROMPT}\n{e}')


class OpenDBExecutor(MysqlIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_DB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenDBWorker(self.item.parent().data(0, Qt.UserRole), self.item.text(0))

# ---------------------------------------- 打开数据库 end ---------------------------------------- #


# ---------------------------------------- 打开数据表 start ---------------------------------------- #

class OpenTBWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(tuple)

    def __init__(self, connection: SqlConnection, db_name, tb_name):
        super().__init__()
        self.connection = connection
        self.db_name = db_name
        self.tb_name = tb_name

    def do_run(self):
        with DBExecutor(*self.connection[1:]) as executor:
            columns = executor.open_tb(self.db_name, self.tb_name)
            log.info(f'[{self.connection.conn_name}][{self.db_name}][{self.tb_name}]{OPEN_TB_SUCCESS_PROMPT}'
                     f' ==> {columns}')
            self.success_signal.emit(columns)

    def do_exception(self, e: Exception):
        log.error(f'[{self.connection.conn_name}][{self.db_name}][{self.tb_name}]{OPEN_TB_FAIL_PROMPT} --> {e}')
        self.error_signal.emit(f'[{self.connection.conn_name}][{self.db_name}][{self.tb_name}]{OPEN_TB_FAIL_PROMPT}\n{e}')


class OpenTBExecutor(MysqlIconMovieThreadExecutor):

    def __init__(self, item, window, success_callback, fail_callback):
        super().__init__(item, window, OPEN_TB_TITLE, success_callback, fail_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return OpenTBWorker(self.item.parent().parent().data(0, Qt.UserRole),
                            self.item.parent().text(0), self.item.text(0))

# ---------------------------------------- 打开数据表 end ---------------------------------------- #
