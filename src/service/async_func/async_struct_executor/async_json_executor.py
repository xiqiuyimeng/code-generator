# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import pyqtSignal

from service.async_func.async_struct_executor.async_struct_executor import PrettyStructWorker, PrettyStructExecutor, \
    OpenStructWorker, OpenStructExecutor
from service.util.struct_parser import parse_json
from view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/12/5 10:13'


# ---------------------------------------- 异步美化json文件 start ---------------------------------------- #

class PrettyJsonWorker(PrettyStructWorker):
    success_signal = pyqtSignal(str)

    def do_beautify(self):
        # 解析美化
        return json.dumps(json.loads(self.data), ensure_ascii=False, indent=4)


class PrettyJsonExecutor(PrettyStructExecutor):

    def get_worker(self) -> PrettyStructWorker:
        return PrettyJsonWorker(self.data, self.struct_type)


# ---------------------------------------- 异步美化json文件 end ---------------------------------------- #


# ---------------------------------------- 打开json结构体 start ---------------------------------------- #

class OpenJsonWorker(OpenStructWorker):

    def parse(self):
        # 解析
        struct_content_dict = json.loads(self.struct_info.content)
        if not isinstance(struct_content_dict, dict):
            raise Exception('无法解析结构体，因为它不是json格式')
        return parse_json(struct_content_dict)


class OpenJsonExecutor(OpenStructExecutor):

    def get_worker(self) -> OpenStructWorker:
        return OpenJsonWorker(get_item_opened_record(self.item))

# ---------------------------------------- 打开json结构体 end ---------------------------------------- #
