# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from src.constant.constant import ADD_COL_TYPE_LIST_TITLE
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.ds_col_type_sqlite import DsColTypeSqlite
from src.service.system_storage.sqlite_abc import transactional
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/2/13 9:03'


# ----------------------- 添加列类型 start ----------------------- #

class SaveDsColTypeWorker(ThreadWorkerABC):

    def __init__(self, ds_col_type_dict):
        super().__init__()
        self.ds_col_type_dict = ds_col_type_dict

    @transactional
    def do_run(self):
        col_type_sqlite = DsColTypeSqlite()
        # 首先清空数据
        col_type_sqlite.truncate_table()
        # 保存数据源列类型
        ds_types, ds_col_types = list(), list()
        for order, ds_type in enumerate(self.ds_col_type_dict.keys(), start=1):
            # 添加数据源类型
            ds_types.append(col_type_sqlite.add_ds_type(ds_type, order))
        # 批量保存数据源类型
        col_type_sqlite.batch_insert(ds_types)

        for index, col_types in enumerate(self.ds_col_type_dict.values()):
            if col_types:
                ds_col_types.extend(col_type_sqlite.batch_add_ds_col_types(col_types, ds_types[index].id))
        if ds_col_types:
            col_type_sqlite.batch_insert(ds_col_types)
        log.info("保存数据源列类型成功")
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = '保存数据源列类型列表失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class SaveDsColTypeExecutor(LoadingMaskThreadExecutor):

    def __init__(self, ds_col_type_dict, callback, *args):
        self.ds_col_type_dict = ds_col_type_dict
        self.callback = callback
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return SaveDsColTypeWorker(self.ds_col_type_dict)

    def success_post_process(self, *args):
        pop_ok('保存数据源列类型成功', ADD_COL_TYPE_LIST_TITLE, self.window)
        self.callback()

# ----------------------- 添加列类型 end ----------------------- #


# ----------------------- 获取列类型列表 start ----------------------- #

class ListDsColTypeWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(dict)

    def do_run(self):
        log.info("开始读取列类型列表")
        # 读取数据库中缓存的列类型列表
        ds_col_types = DsColTypeSqlite().get_all_ds_col_types()
        if ds_col_types:
            self.success_signal.emit(ds_col_types)
        else:
            self.success_signal.emit(dict())
        log.info("读取列类型列表成功")

    def do_exception(self, e: Exception):
        err_msg = '读取列类型列表失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListDsColTypeExecutor(LoadingMaskThreadExecutor):

    def __init__(self, callback, *args):
        self.callback = callback
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ListDsColTypeWorker()

    def success_post_process(self, *args):
        self.callback(*args)

# ----------------------- 获取列类型列表 end ----------------------- #
