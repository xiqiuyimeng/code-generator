# -*- coding: utf-8 -*-
import dataclasses
from queue import Queue

from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, ThreadExecutorABC
from service.system_storage.ds_table_info_sqlite import DsTableInfoSqlite, DsTableInfo
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite

_author_ = 'luwt'
_date_ = '2022/10/12 12:10'


class TabChangedWorker(ThreadWorkerABC):

    success_signal = pyqtSignal()

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def do_run(self):
        while True:
            method, data = self.queue.get()
            if method == 'remove_tab':
                DsTableTabSqlite().remove_tab(data)
                DsTableInfoSqlite().delete_by_parent_tab_id(data.id)
            elif method == 'change_current':
                DsTableTabSqlite().change_current(data)
            elif method == 'sort_order':
                DsTableTabSqlite().batch_update(data)
            elif method == 'save_table_data':
                DsTableInfoSqlite().update(data)
            log.debug(f'{method}: {data}')

    def do_exception(self, e: Exception):
        log.exception('更新tab页数据异常')


class AsyncSaveTabObjExecutor(ThreadExecutorABC):

    def __init__(self):
        self.queue = Queue()
        super().__init__(None, None)

    def get_worker(self) -> ThreadWorkerABC:
        return TabChangedWorker(self.queue)

    def remove_tab(self, tab):
        self.queue.put(('remove_tab', tab))

    def change_current(self, current_tab):
        self.queue.put(('change_current', current_tab))

    def sort_order(self, tabs):
        self.queue.put(('sort_order', tabs))

    def save_table_data(self, modify_data: DsTableInfo):
        self.queue.put(('save_table_data', modify_data))
