# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import pyqtSignal

from service.async_func.struct_executor.async_struct_act_task import PrettyStructWorker, PrettyStructExecutor, \
    OpenStructWorker, OpenStructExecutor

_author_ = 'luwt'
_date_ = '2022/12/5 10:13'


# ---------------------------------------- 异步美化json文件 start ---------------------------------------- #

class PrettyJsonWorker(PrettyStructWorker):
    success_signal = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)

    def do_beautify(self):
        # 解析美化
        return json.dumps(json.loads(self.data), ensure_ascii=False, indent=4)


class PrettyJsonExecutor(PrettyStructExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def get_worker(self) -> PrettyStructWorker:
        return PrettyJsonWorker(self.data, self.struct_type)


# ---------------------------------------- 异步美化json文件 end ---------------------------------------- #


# ---------------------------------------- 打开json结构体 start ---------------------------------------- #

class OpenJsonWorker(OpenStructWorker):
    success_signal = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)

    def do_parse(self):
        # 解析
        if self.struct_info is not Ellipsis:
            return json.dumps(json.loads(self.struct_info), ensure_ascii=False, indent=4)


class OpenJsonExecutor(OpenStructExecutor):

    def __init__(self, *args):
        super().__init__(*args)

    def get_worker(self) -> OpenStructWorker:
        return OpenJsonWorker(self.struct_id, self.struct_name)

# ---------------------------------------- 打开json结构体 end ---------------------------------------- #
