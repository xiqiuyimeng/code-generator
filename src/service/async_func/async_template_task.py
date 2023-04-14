# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.template_config_sqlite import TemplateConfigSqlite
from src.service.system_storage.template_file_sqlite import TemplateFileSqlite
from src.service.system_storage.template_sqlite import TemplateSqlite, Template
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/3/9 9:22'


# ----------------------- 读取模板信息 start ----------------------- #
class ReadTemplateWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(Template)

    def __init__(self, template_id):
        super().__init__()
        self.template_id = template_id

    def do_run(self):
        log.info("开始读取模板详细信息")
        # 查询模板信息
        param = Template()
        param.id = self.template_id
        template = TemplateSqlite().select_one(param)
        if not template:
            raise Exception('未查询到模板信息')
        # 查询模板文件列表
        template.template_files = TemplateFileSqlite().get_by_template_id(self.template_id)
        template_config_list = TemplateConfigSqlite().get_by_template_id(self.template_id)
        template.output_config_list, template.var_config_list = template_config_list
        # 将模板文件按关联的输出路径配置id分组
        if template.template_files and template.output_config_list:
            template_file_dict = dict([(tp_file.output_config_id, tp_file) for tp_file in template.template_files])
            for output_config in template.output_config_list:
                output_config.relevant_file_list = template_file_dict.get(output_config.id, list())
        self.success_signal.emit(template)
        log.info("读取模板详细信息成功")

    def do_exception(self, e: Exception):
        err_msg = '读取模板信息失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ReadTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_id, *args):
        self.template_id = template_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ReadTemplateWorker(self.template_id)


# ----------------------- 读取模板信息 end ----------------------- #


# ----------------------- 添加模板 start ----------------------- #

class AddTemplateWorker(ThreadWorkerABC):

    def __init__(self, template: Template):
        super().__init__()
        self.template = template

    @transactional
    def do_run(self):
        log.info(f'开始保存模板 [{self.template.template_name}]')
        # 保存模板，首先保存模板信息
        TemplateSqlite().save_template(self.template)
        # 保存模板文件信息
        if self.template.template_files:
            TemplateFileSqlite().batch_add_template_files(self.template.id, self.template.template_files)
        # 保存模板配置信息
        if self.template.var_config_list:
            TemplateConfigSqlite().batch_add_config_list(self.template.id, self.template.output_config_list,
                                                         self.template.var_config_list)
        self.success_signal.emit()
        log.info(f'保存模板 [{self.template.template_name}] 成功')

    def do_exception(self, e: Exception):
        err_msg = f'保存 [{self.template.template_name}] 模板信息失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class AddTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template: Template, *args):
        self.template = template
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AddTemplateWorker(self.template)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template.template_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 添加模板 end ----------------------- #


# ----------------------- 编辑模板 start ----------------------- #

class EditTemplateWorker(ThreadWorkerABC):

    def __init__(self, template: Template):
        super().__init__()
        self.template = template

    @transactional
    def do_run(self):
        log.info(f'开始编辑模板信息 [{self.template.template_name}]')
        # 首先更新模板信息
        TemplateSqlite().update(self.template)
        # 处理模板文件列表
        TemplateFileSqlite().batch_edit_template_files(self.template.id, self.template.template_files)
        # 保存模板输入配置信息
        TemplateConfigSqlite().batch_edit_config_list(self.template.id, self.template.output_config_list,
                                                      self.template.var_config_list)
        self.success_signal.emit()
        log.info(f'编辑模板信息 [{self.template.template_name}] 结束')

    def do_exception(self, e: Exception):
        err_msg = f'编辑模板 [{self.template.template_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class EditTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template: Template, *args):
        self.template = template
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return EditTemplateWorker(self.template)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template.template_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 编辑模板 end ----------------------- #


# ----------------------- 删除模板 start ----------------------- #

class DelTemplateWorker(ThreadWorkerABC):

    def __init__(self, template_ids, template_names):
        super().__init__()
        self.template_ids = template_ids
        self.template_names = template_names

    @transactional
    def do_run(self):
        log.info(f'开始删除模板 [{self.template_names}]')
        # 首先删除模板
        TemplateSqlite().batch_delete(self.template_ids)
        TemplateFileSqlite().batch_del_template_files(self.template_ids)
        TemplateConfigSqlite().batch_del_config_list(self.template_ids)
        self.success_signal.emit()
        log.info(f'删除模板 [{self.template_names}] 成功')

    def do_exception(self, e: Exception):
        err_msg = f'删除模板 [{self.template_names}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class DelTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_id, template_name, row_index, *args):
        self.template_id = template_id
        self.template_name = template_name
        self.row_index = row_index
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTemplateWorker((self.template_id, ), (self.template_name, ))

    def success_post_process(self, *args):
        self.success_callback(self.row_index)


class BatchDelTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_ids, template_names, *args):
        self.template_ids = template_ids
        self.template_names = template_names
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTemplateWorker(self.template_ids, self.template_names)


# ----------------------- 删除模板 end ----------------------- #


# ----------------------- 获取模板列表 start ----------------------- #

class ListTemplateWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info("读取模板列表")
        # 读取数据库中缓存的模板列表
        template_list = TemplateSqlite().select_by_order(Template())
        self.success_signal.emit(template_list)
        log.info("读取模板列表成功")

    def do_exception(self, e: Exception):
        err_msg = '读取模板列表失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListTemplateExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateWorker()

# ----------------------- 获取模板列表 end ----------------------- #


# ----------------------- 获取模板配置列表 start ----------------------- #

class ListTemplateConfigWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list, list)

    def __init__(self, template_id):
        super().__init__()
        self.template_id = template_id

    def do_run(self):
        log.info(f"读取模板配置列表：{self.template_id}")
        # 读取数据库中缓存的模板列表
        template_config_list = TemplateConfigSqlite().get_by_template_id(self.template_id)
        self.success_signal.emit(*template_config_list)
        log.info(f"读取模板配置列表成功：{self.template_id}")

    def do_exception(self, e: Exception):
        err_msg = '读取模板配置列表失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListTemplateConfigExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_id, *args):
        self.template_id = template_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateConfigWorker(self.template_id)

# ----------------------- 获取模板配置列表 end ----------------------- #
