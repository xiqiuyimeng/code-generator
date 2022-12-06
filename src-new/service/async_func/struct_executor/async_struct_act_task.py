# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
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
        self.error_signal.emit(f'{err_msg}\n{e}')


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
    success_signal = pyqtSignal(list)

    def __init__(self, struct_id, struct_name):
        super().__init__()
        self.struct_id = struct_id
        self.struct_name = struct_name
        self.struct_info = ...

    def do_run(self):
        # 读取结构体内容
        param = StructInfo()
        param.id = self.struct_id
        self.struct_info = StructSqlite().select(param)
        # 解析转化
        result = self.do_parse()
        self.success_signal.emit(result)

    def do_parse(self) -> list: ...

    def do_exception(self, e: Exception):
        err_msg = f'打开{self.struct_name}失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e}')


class OpenStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, struct_id, struct_name, masked_widget, window, callback):
        self.struct_id = struct_id
        self.struct_name = struct_name
        self.callback = callback
        super().__init__(masked_widget, window, f'打开{self.struct_name}')

    def success_post_process(self, *args):
        self.callback(*args)

# ---------------------------------------- 打开结构体 end ---------------------------------------- #
