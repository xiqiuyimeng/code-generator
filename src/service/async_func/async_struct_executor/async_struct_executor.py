# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from service.system_storage.sqlite_abc import transactional
from service.system_storage.struct_sqlite import StructInfo, StructSqlite

_author_ = 'luwt'
_date_ = '2022/12/5 15:35'


# ---------------------------------------- 异步美化结构体 start ---------------------------------------- #

class PrettyStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(str)

    def __init__(self, data, struct_type):
        super().__init__()
        self.data = data
        self.struct_type = struct_type

    def do_run(self):
        # 解析美化
        result = self.do_beautify()
        self.success_signal.emit(result)

    def do_beautify(self) -> str: ...

    def do_exception(self, e: Exception):
        err_msg = f'美化{self.struct_type}数据失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class PrettyStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, data, struct_type, masked_widget, window, callback):
        self.data = data
        self.struct_type = struct_type
        self.callback = callback
        super().__init__(masked_widget, window, f'解析{self.struct_type}')

    def success_post_process(self, *args):
        self.callback(*args)


# ---------------------------------------- 异步美化结构体 end ---------------------------------------- #


# ---------------------------------------- 打开结构体 start ---------------------------------------- #

class OpenStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, opened_table_item):
        super().__init__()
        self.opened_table_item = opened_table_item
        self.table_info_sqlite = DsTableColInfoSqlite()
        self.struct_info = ...
        self.table_tab_id = ...

    @transactional
    def do_run(self):
        # 读取结构体内容
        param = StructInfo()
        param.opened_item_id = self.opened_table_item.id
        struct_list = StructSqlite().select(param)
        if struct_list:
            self.modifying_db_task = True
            self.struct_info = struct_list[0]
            # 存储tab信息
            table_tab = DsTableTabSqlite().add_tab(self.opened_table_item)
            self.table_tab_id = table_tab.id
            # 解析转化
            column_list = self.parse()
            table_tab.col_list = column_list
            # 保存列信息
            self.save_cols(column_list, parent_id=0)
            self.modifying_db_task = False
            self.success_signal.emit(table_tab)
        else:
            self.success_signal.emit(DsTableTab())

    def parse(self) -> list: ...

    def save_cols(self, column_list, parent_id):
        # 保存解析后的列数据，首先处理当前的列数据，再考虑子集合
        # 处理当前列数据的 parent_id，item_order，parent_tab_id，checked
        for idx, column in enumerate(column_list, start=1):
            column.parent_id = parent_id
            column.item_order = idx
            column.parent_tab_id = self.table_tab_id
            # 选中状态与树节点保持一致
            column.checked = self.opened_table_item.checked
        self.table_info_sqlite.batch_insert(column_list)

        # 考虑存在子集合的情况
        for col_info in column_list:
            if col_info.children:
                self.save_cols(col_info.children, col_info.id)

    def do_exception(self, e: Exception):
        err_msg = f'打开{self.opened_table_item.item_name}失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class OpenStructExecutor(IconMovieThreadExecutor):

    def __init__(self, item, window, callback, fail_callback):
        self.item = item
        self.callback = callback
        self.fail_callback = fail_callback
        super().__init__(item, window, '打开结构体')

    def success_post_process(self, *args):
        self.callback(*args)

    def fail_post_process(self):
        self.fail_callback()

# ---------------------------------------- 打开结构体 end ---------------------------------------- #
