# -*- coding: utf-8 -*-
import json
import os

from src.constant.export_import_constant import TYPE_KEY, DATA_KEY
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.util.path_util import check_path_legal
from src.service.util.struct_util.json_util import load_json_str
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/5/10 14:23'


# ----------------------- 导入数据 start ----------------------- #

class ImportDataWorker(ThreadWorkerABC):

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.data_key: str = ...

    def do_run(self):
        if not os.path.exists(self.file_path):
            raise Exception(f'文件路径不存在：{self.file_path}')
        with open(self.file_path, 'r', encoding='utf-8')as f:
            file_data = f.read()
        # 文件格式必须是json
        load_json: dict = load_json_str(file_data)
        # 校验数据
        import_data_type = load_json.get(TYPE_KEY)
        if self.data_key != import_data_type:
            raise Exception('不支持的数据类型')
        # 取出数据
        import_data_list = load_json.get(DATA_KEY)
        # 开始导入
        self.import_data(import_data_list)
        self.success_signal.emit()

    def import_data(self, data_list): ...


class ImportDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, file_path, *args):
        # 要导入的文件路径，目前只允许导入一个文件
        self.file_path = file_path
        super().__init__(*args)

    def success_post_process(self):
        pop_ok(f'{self.error_box_title}成功', self.error_box_title, self.window)


# ----------------------- 导入数据 end ----------------------- #


# ----------------------- 导出数据 start ----------------------- #

class ExportDataWorker(ThreadWorkerABC):

    def __init__(self, row_ids, file_path):
        super().__init__()
        self.row_ids = row_ids
        self.file_path = file_path
        self.data_key: str = ...

    def do_run(self):
        # 检查文件路径是否合法
        if not check_path_legal(self.file_path):
            raise Exception(f'当前路径不合法：{self.file_path}')
        # 根据传入的行id列表，进行导出
        export_data_list = self.export_data()
        # 导出完毕，检查路径是否存在，不存在则创建
        file_dir = os.path.split(self.file_path)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 写入数据，类型、数据
        result_json = {
            TYPE_KEY: self.data_key,
            DATA_KEY: export_data_list
        }
        with open(self.file_path, 'w', encoding='utf-8')as f:
            json.dump(result_json, f, ensure_ascii=False, indent=4)
        self.success_signal.emit()

    def export_data(self) -> list[dict]: ...


class ExportDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, row_ids, file_path, *args):
        self.row_ids = row_ids
        self.file_path = file_path
        super().__init__(*args)

    def success_post_process(self):
        pop_ok(f'{self.error_box_title}成功', self.error_box_title, self.window)

# ----------------------- 导出数据 end ----------------------- #
