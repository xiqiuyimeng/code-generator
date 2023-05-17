# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal

from src.constant.export_import_constant import TEMPLATE_FUNC_DATA_KEY
from src.logger.log import logger as log
from src.service.async_func.async_import_export_task import ImportDataWorker, ImportDataExecutor, OverrideDataWorker, \
    OverrideDataExecutor, ExportDataWorker, ExportDataExecutor
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.template_func_sqlite import TemplateFunc, TemplateFuncSqlite, ImportExportTemplateFunc
from src.service.util.import_export_util import convert_import_to_model
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/3/28 11:02'


# ----------------------- 添加模板方法 start ----------------------- #

class AddTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func: TemplateFunc):
        super().__init__()
        self.template_func = template_func

    def do_run(self):
        log.info(f'开始保存模板方法 [{self.template_func.func_name}]')
        TemplateFuncSqlite().save_template_func(self.template_func)
        self.success_signal.emit()
        log.info(f'保存模板方法 [{self.template_func.func_name}] 成功')

    def get_err_msg(self) -> str:
        return f'保存 [{self.template_func.func_name}] 模板方法信息失败'


class AddTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func: TemplateFunc, *args):
        self.template_func = template_func
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AddTemplateFuncWorker(self.template_func)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template_func.func_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 添加模板方法 end ----------------------- #


# ----------------------- 编辑模板方法 start ----------------------- #

class EditTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func: TemplateFunc):
        super().__init__()
        self.template_func = template_func

    def do_run(self):
        log.info(f'开始编辑模板方法信息 [{self.template_func.func_name}]')
        TemplateFuncSqlite().update(self.template_func)
        self.success_signal.emit()
        log.info(f'编辑模板方法信息 [{self.template_func.func_name}] 结束')

    def get_err_msg(self) -> str:
        return f'编辑模板方法 [{self.template_func.func_name}] 失败'


class EditTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func: TemplateFunc, *args):
        self.template_func = template_func
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return EditTemplateFuncWorker(self.template_func)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template_func.func_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 编辑模板方法 end ----------------------- #


# ----------------------- 删除模板方法 start ----------------------- #

class DelTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func_id, template_func_name):
        super().__init__()
        self.template_func_id = template_func_id
        self.template_func_name = template_func_name

    def do_run(self):
        log.info(f'开始删除模板方法 [{self.template_func_name}]')
        TemplateFuncSqlite().delete(self.template_func_id)
        self.success_signal.emit()
        log.info(f'删除模板方法 [{self.template_func_name}] 成功')

    def get_err_msg(self) -> str:
        return f'删除模板方法 [{self.template_func_name}] 失败'


class DelTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func_id, template_func_name, *args):
        self.template_func_id = template_func_id
        self.template_func_name = template_func_name
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTemplateFuncWorker(self.template_func_id, self.template_func_name)


# ----------------------- 删除模板方法 end ----------------------- #

# ----------------------- 清空模板方法 start ----------------------- #

class ClearTemplateFuncWorker(ThreadWorkerABC):

    def do_run(self):
        log.info('开始清空模板方法')
        TemplateFuncSqlite().drop_template_func_table()
        self.success_signal.emit()
        log.info('清空模板方法成功')

    def get_err_msg(self) -> str:
        return '清空模板方法失败'


class ClearTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ClearTemplateFuncWorker()


# ----------------------- 清空模板方法 end ----------------------- #


# ----------------------- 获取模板方法列表 start ----------------------- #

class ListTemplateFuncWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info("读取模板方法列表")
        template_list = TemplateFuncSqlite().select_by_order(TemplateFunc())
        self.success_signal.emit(template_list)
        log.info("读取模板方法列表成功")

    def get_err_msg(self) -> str:
        return '读取模板方法列表失败'


class ListTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateFuncWorker()

# ----------------------- 获取模板方法列表 end ----------------------- #


# ----------------------- 导入模板方法 start ----------------------- #

class ImportTemplateFuncWorker(ImportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TEMPLATE_FUNC_DATA_KEY
        self.template_func_sqlite = TemplateFuncSqlite()

    def convert_to_model(self, import_data):
        return convert_import_to_model(ImportExportTemplateFunc, TemplateFunc, import_data)

    def pre_process_before_check_data(self):
        # 查出所有模板方法名称
        self.exists_names = self.template_func_sqlite.get_all_names()

    def check_repair_illegal_data(self, data_row) -> int:
        return 0

    @transactional
    def import_data(self, data_list):
        self.template_func_sqlite.batch_save_template_funcs(data_list)

    def get_err_msg(self) -> str:
        return '导入模板方法失败'


class ImportTemplateFuncExecutor(ImportDataExecutor):

    def get_worker(self) -> ImportTemplateFuncWorker:
        return ImportTemplateFuncWorker(self.file_path)

# ----------------------- 导入模板方法 end ----------------------- #


# ----------------------- 覆盖数据 start ----------------------- #

class OverrideTemplateFuncWorker(OverrideDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.template_func_sqlite = TemplateFuncSqlite()

    def batch_delete_origin_data(self):
        self.template_func_sqlite.batch_delete_by_names(self.data_list)

    def batch_insert_data_list(self):
        self.template_func_sqlite.batch_save_template_funcs(self.data_list)

    def get_err_msg(self) -> str:
        return '覆盖模板方法失败'


class OverrideTemplateFuncExecutor(OverrideDataExecutor):

    def get_worker(self) -> OverrideTemplateFuncWorker:
        return OverrideTemplateFuncWorker(self.data_list)

# ----------------------- 覆盖数据 end ----------------------- #


# ----------------------- 导出模板方法 start ----------------------- #

class ExportTemplateFuncWorker(ExportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TEMPLATE_FUNC_DATA_KEY

    def export_data(self) -> list[dataclasses.dataclass]:
        return TemplateFuncSqlite().export_template_func_by_ids(self.row_ids)

    def get_err_msg(self) -> str:
        return '导出模板方法失败'


class ExportTemplateFuncExecutor(ExportDataExecutor):

    def get_worker(self) -> ExportTemplateFuncWorker:
        return ExportTemplateFuncWorker(self.row_ids, self.file_path)

# ----------------------- 导出模板方法 end ----------------------- #
