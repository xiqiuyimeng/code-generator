# -*- coding: utf-8 -*-
from queue import Queue

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, ThreadExecutorABC
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite, DsTableColInfo
from src.service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite
from src.service.util.system_storage_util import transactional, release_connection

_author_ = 'luwt'
_date_ = '2022/10/12 12:10'


class TabChangedWorker(ThreadWorkerABC):

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def do_run(self):
        while True:
            method, data = self.queue.get()
            try:
                if method == 'remove_tab':
                    self.remove_tab(data)
                elif method == 'change_current':
                    DsTableTabSqlite().change_current(data)
                elif method == 'sort_order':
                    DsTableTabSqlite().batch_update(data)
                elif method == 'save_table_data':
                    DsTableColInfoSqlite().update_by_id(data)
                elif method == 'batch_save_data':
                    DsTableColInfoSqlite().batch_update(data)
                elif method == 'update_col_expanded':
                    DsTableColInfoSqlite().update_by_id(data)
            finally:
                # 使用完及时释放数据库连接
                release_connection()
                log.debug(f'{method}: {data}')

    @transactional
    def remove_tab(self, data):
        DsTableTabSqlite().remove_tab(data)
        DsTableColInfoSqlite().delete_by_parent_tab_id(data.id)

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

    def save_table_data(self, modify_data: DsTableColInfo):
        self.queue.put(('save_table_data', modify_data))

    def batch_save_data(self, data):
        self.queue.put(('batch_save_data', data))

    def update_col_expanded(self, col):
        self.queue.put(('update_col_expanded', col))
