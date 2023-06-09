# -*- coding: utf-8 -*-
import dataclasses
import json
import os

from PyQt5.QtCore import pyqtSignal

from src.constant.export_import_constant import TYPE_KEY, DATA_KEY
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.util.path_util import check_path_legal
from src.service.util.struct_util.json_util import load_json_str
from src.service.util.system_storage_util import transactional
from src.view.box.message_box import pop_ok, pop_question

_author_ = 'luwt'
_date_ = '2023/5/10 14:23'


# ----------------------- 导入数据 start ----------------------- #

class ImportDataWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list, list, list, list)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.data_key: str = ...
        self.exists_names = ...

    def do_run(self):
        if not os.path.exists(self.file_path):
            raise Exception(f'文件路径不存在：{self.file_path}')
        with open(self.file_path, 'r', encoding='utf-8') as f:
            file_data = f.read()
        # 文件格式必须是json
        load_json: dict = load_json_str(file_data, json_type=dict)
        # 校验类型是否支持
        import_data_type = load_json.get(TYPE_KEY)
        if self.data_key != import_data_type:
            raise Exception('不支持的类型')

        # 取出数据
        import_data_list = load_json.get(DATA_KEY)
        if not import_data_list:
            raise Exception('未检测到导入数据')

        # 转为实体
        import_data_model_list: list = self.convert_to_model_list(import_data_list)

        # 数据去重，如果导入的数据内存在重复的，首先去重，再进行下面的处理
        unique_model_list = list({row.get_name(): row
                                  for row in import_data_model_list if row.get_name()}.values())

        # 前置处理，因为下面的校验会涉及数据库操作，允许子类预先将所有需要数据准备好
        self.pre_process_before_check_data()

        # 数据校验，分类
        collect_result = self.collect_check_data(unique_model_list)

        # 校验通过的数据，进行导入
        legal_rows = collect_result[3]
        if legal_rows:
            self.import_data(legal_rows)
        # 返回数据分类的结果
        self.success_signal.emit(*collect_result)

    def convert_to_model_list(self, import_data_list):
        return [self.convert_to_model(import_data) for import_data in import_data_list]

    def convert_to_model(self, import_data):
        ...

    def pre_process_before_check_data(self):
        ...

    def collect_check_data(self, import_data_list):
        duplicate_rows, illegal_rows, duplicate_illegal_rows, legal_rows = list(), list(), list(), list()
        for data_row in import_data_list:
            # 校验数据重复
            duplicate_flag = data_row.get_name() in self.exists_names
            # 校验数据是否正确合法，校验的同时，也应当将一些页面无法体现错误的数据进行修复，例如类型映射中的组号
            if self.check_repair_illegal_data(data_row):
                # 数据不合法，且重复，放入重复不合法数据列表
                if duplicate_flag:
                    duplicate_illegal_rows.append(data_row)
                # 数据不合法，且不重复，放入不合法数据列表
                else:
                    illegal_rows.append(data_row)
            else:
                # 如果数据正确合法，且不重复，放入正确的数据列表
                if not duplicate_flag:
                    legal_rows.append(data_row)
                else:
                    # 数据正确，但重复，放入重复数据列表
                    duplicate_rows.append(data_row)
        return duplicate_rows, illegal_rows, duplicate_illegal_rows, legal_rows

    def check_repair_illegal_data(self, data_row) -> int:
        ...

    def import_data(self, data_list):
        ...


class ImportDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, file_path, *args, process_error_data_func=None, **kwargs):
        # 要导入的文件路径，目前只允许导入一个文件
        self.file_path = file_path
        self.process_error_data_func = process_error_data_func
        super().__init__(*args, **kwargs)

    def success_post_process(self, *args):
        duplicate_rows, illegal_rows, duplicate_illegal_rows, legal_rows = args
        # 首先先在页面添加成功的数据
        if legal_rows:
            # 回调，渲染页面
            self.success_callback(legal_rows)
        success_msg = f'{self.error_box_title} {len(legal_rows)} 条数据成功'
        # 如果存在重复数据，或是异常数据，则弹窗询问是否处理
        if any((duplicate_rows, illegal_rows, duplicate_illegal_rows)):
            reply = pop_question(f'{success_msg}\n'
                                 f'\b\b\b\b{len(duplicate_rows)} 条数据已存在\n'
                                 f'\b\b\b\b{len(illegal_rows)} 条数据异常\n'
                                 f'\b\b\b\b{len(duplicate_illegal_rows)} 条数据已存在且数据异常\n'
                                 f'是否手动处理这些数据？\n'
                                 '选择 [是] 将进入异常文件处理页，选择 [否] 将忽略这些数据',
                                 self.error_box_title, self.window)
            if reply:
                # 进行后续的异常文件处理
                self.process_error_data_func(duplicate_rows, illegal_rows, duplicate_illegal_rows)
        else:
            # 如果都处理成功，提示成功消息
            pop_ok(success_msg, self.error_box_title, self.window)


# ----------------------- 导入数据 end ----------------------- #


# ----------------------- 覆盖数据 start ----------------------- #

class OverrideDataWorker(ThreadWorkerABC):

    def __init__(self, data_list):
        super().__init__()
        self.data_list = data_list

    @transactional
    def do_run(self):
        # 首先删除原有数据
        self.batch_delete_origin_data()
        # 批量插入当前新的数据
        self.batch_insert_data_list()
        self.success_signal.emit()

    def batch_delete_origin_data(self):
        ...

    def batch_insert_data_list(self):
        ...


class OverrideDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, data_list, *args, **kwargs):
        self.data_list = data_list
        super().__init__(*args, **kwargs)

    def success_post_process(self, *args):
        self.success_callback(self.data_list, self.data_list)
        pop_ok(f'覆盖 {len(self.data_list)} 条数据成功', self.error_box_title, self.window)


# ----------------------- 覆盖数据 end ----------------------- #


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
        data_dict_list = [dataclasses.asdict(data) for data in export_data_list]
        # 导出完毕，检查路径是否存在，不存在则创建
        file_dir = os.path.split(self.file_path)[0]
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        # 写入数据，类型、数据
        result_json = {
            TYPE_KEY: self.data_key,
            DATA_KEY: data_dict_list
        }
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(result_json, f, ensure_ascii=False, indent=4)
        self.success_signal.emit()

    def export_data(self) -> list[dataclasses.dataclass]:
        ...


class ExportDataExecutor(LoadingMaskThreadExecutor):

    def __init__(self, row_ids, file_path, *args):
        self.row_ids = row_ids
        self.file_path = file_path
        super().__init__(*args)

    def success_post_process(self):
        pop_ok(f'{self.error_box_title}{len(self.row_ids)} 条数据成功', self.error_box_title, self.window)

# ----------------------- 导出数据 end ----------------------- #
