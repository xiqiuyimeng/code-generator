# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from service.system_storage.conn_sqlite import ConnSqlite, SqlConnection
from view.box.message_box import pop_ok
from constant.constant import SAVE_CONN_TITLE, SAVE_CONN_SUCCESS_PROMPT, \
    SAVE_CONN_FAIL_PROMPT, DEL_CONN_SUCCESS_PROMPT, DEL_CONN_FAIL_PROMPT, DEL_CONN_TITLE, \
    LIST_ALL_CONN_SUCCESS_PROMPT, LIST_ALL_CONN_FAIL_PROMPT, LIST_ALL_CONN_TITLE

_author_ = 'luwt'
_date_ = '2022/5/30 20:31'


# ---------------------------------------- 添加连接 start ---------------------------------------- #

class AddConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(int)

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    def do_run(self):
        ConnSqlite().insert(self.connection)
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit(self.connection.id)

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

    def __init__(self, connection: SqlConnection):
        super().__init__()
        self.connection = connection

    def do_run(self):
        ConnSqlite().update(self.connection)
        log.info(f'[{self.connection.conn_name}]{SAVE_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.exception(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.connection.conn_name}]{SAVE_CONN_FAIL_PROMPT}\n{e}')


class EditConnExecutor(LoadingMaskThreadExecutor):
    
    def __init__(self, connection: SqlConnection, masked_widget, window, callback):
        self.connection = connection
        self.callback = callback
        super().__init__(masked_widget, window, SAVE_CONN_TITLE)
        
    def get_worker(self) -> ThreadWorkerABC:
        return EditConnWorker(self.connection)
    
    def success_post_process(self, *args):
        pop_ok(f'[{self.connection.conn_name}]\n{SAVE_CONN_SUCCESS_PROMPT}',
               SAVE_CONN_TITLE, self.window)
        self.callback()

# ---------------------------------------- 编辑连接 end ---------------------------------------- #


# ---------------------------------------- 删除连接 start ---------------------------------------- #

class DelConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal()
    
    def __init__(self, conn_id, conn_name):
        super().__init__()
        self.conn_id = conn_id
        self.conn_name = conn_name

    def do_run(self):
        ConnSqlite().delete(self.conn_id)
        log.info(f'[{self.conn_name}]{DEL_CONN_SUCCESS_PROMPT}')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        log.exception(f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}')
        self.error_signal.emit(f'[{self.conn_name}]{DEL_CONN_FAIL_PROMPT}\n{e}')


class DelConnExecutor(IconMovieThreadExecutor):

    def __init__(self, conn_id, conn_name, item, window, callback):
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.callback = callback
        super().__init__(item, window, DEL_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return DelConnWorker(self.conn_id, self.conn_name)

    def success_post_process(self, *args):
        self.callback()

# ---------------------------------------- 删除连接 end ---------------------------------------- #


# ---------------------------------------- 获取所有连接 start ---------------------------------------- #

class ListConnWorker(ThreadWorkerABC):

    success_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def do_run(self):
        connections = ConnSqlite().select(SqlConnection())
        log.info(LIST_ALL_CONN_SUCCESS_PROMPT)
        self.success_signal.emit(connections)

    def do_exception(self, e: Exception):
        log.exception(LIST_ALL_CONN_FAIL_PROMPT)
        self.error_signal.emit(f'{LIST_ALL_CONN_FAIL_PROMPT}\n{e}')


class ListConnExecutor(LoadingMaskThreadExecutor):

    def __init__(self, masked_widget, window, callback):
        self.callback = callback
        super().__init__(masked_widget, window, LIST_ALL_CONN_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return ListConnWorker()

    def success_post_process(self, *args):
        self.callback(*args)

# ---------------------------------------- 获取所有连接 end ---------------------------------------- #

