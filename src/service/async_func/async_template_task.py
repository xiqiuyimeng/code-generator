# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal

from src.constant.export_import_constant import TEMPLATE_DATA_KEY
from src.logger.log import logger as log
from src.service.async_func.async_import_export_task import ExportDataWorker, ExportDataExecutor
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.template_config_sqlite import TemplateConfigSqlite, construct_output_config, \
    ConfigTypeEnum
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
            template_file_dict = dict()
            for tp_file in template.template_files:
                file_list = template_file_dict.get(tp_file.output_config_id, list())
                if not file_list:
                    template_file_dict[tp_file.output_config_id] = file_list
                file_list.append(tp_file)
            for output_config in template.output_config_list:
                output_config.bind_file_list = template_file_dict.get(output_config.id)
        self.success_signal.emit(template)
        log.info("读取模板详细信息成功")

    def get_err_msg(self) -> str:
        return '读取模板信息失败'


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
        # 保存模板配置信息
        TemplateConfigSqlite().batch_add_config_list(self.template.id, self.template.output_config_list,
                                                     self.template.var_config_list)
        # 保存模板文件信息
        if self.template.template_files:
            TemplateFileSqlite().batch_add_template_files(self.template.id, self.template.template_files)
        self.success_signal.emit()
        log.info(f'保存模板 [{self.template.template_name}] 成功')

    def get_err_msg(self) -> str:
        return f'保存 [{self.template.template_name}] 模板信息失败'


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
        # 保存模板输入配置信息
        TemplateConfigSqlite().batch_edit_config_list(self.template.id, self.template.output_config_list,
                                                      self.template.var_config_list)
        # 处理模板文件列表
        TemplateFileSqlite().batch_edit_template_files(self.template.id, self.template.template_files)
        self.success_signal.emit()
        log.info(f'编辑模板信息 [{self.template.template_name}] 结束')

    def get_err_msg(self) -> str:
        return f'编辑模板 [{self.template.template_name}] 失败'


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

    def get_err_msg(self) -> str:
        return f'删除模板 [{self.template_names}] 失败'


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

    def get_err_msg(self) -> str:
        return '读取模板列表失败'


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

    def get_err_msg(self) -> str:
        return '读取模板配置列表失败'


class ListTemplateConfigExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_id, *args):
        self.template_id = template_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateConfigWorker(self.template_id)

# ----------------------- 获取模板配置列表 end ----------------------- #


# ----------------------- 自动生成文件对应的输出配置 start ----------------------- #

class AutoGenerateOutputConfigWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list, list)

    def __init__(self, config_name_list, var_name_list, file_list):
        super().__init__()
        self.config_name_list = config_name_list
        self.var_name_list = var_name_list
        self.file_list = file_list

    def do_run(self):
        success_list, fail_list = list(), list()
        # 每个文件生成一个配置
        for file in self.file_list:
            output_config = construct_output_config(self.config_name_list,
                                                    self.var_name_list, file.file_name)
            if output_config:
                # 顺利生成，添加到成功列表中，绑定关联文件
                output_config.bind_file_list = [file]
                # 给一个虚拟配置id
                file.output_config_id = -1
                success_list.append(output_config)
            else:
                fail_list.append(file.file_name)
        self.success_signal.emit(success_list, fail_list)

    def get_err_msg(self) -> str:
        return '自动生成输出路径配置异常'


class AutoGenerateOutputConfigExecutor(LoadingMaskThreadExecutor):

    def __init__(self, config_name_list, var_name_list, file_list, *args):
        self.config_name_list = config_name_list
        self.var_name_list = var_name_list
        self.file_list = file_list
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AutoGenerateOutputConfigWorker(self.config_name_list, self.var_name_list, self.file_list)

# ----------------------- 自动生成文件对应的输出配置 end ----------------------- #


# ----------------------- 导出类型映射 start ----------------------- #

class ExportTemplateWorker(ExportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TEMPLATE_DATA_KEY

    def export_data(self) -> list[dict]:
        # 1. 查询模板信息
        template_list = TemplateSqlite().export_template_by_ids(self.row_ids)
        if not template_list:
            raise Exception('未获取到模板信息')
        # 2. 查询模板文件
        template_file_list = TemplateFileSqlite().export_files_by_parent_id(self.row_ids)

        def group_template_file(get_group_key):
            template_file_dict = dict()
            for template_file in template_file_list:
                file_list = template_file_dict.get(get_group_key(template_file))
                if file_list is None:
                    file_list = list()
                    template_file_dict[get_group_key(template_file)] = file_list
                file_list.append(template_file)
            return template_file_dict

        # 3. 文件按模板id分组
        template_id_file_dict = group_template_file(lambda x: x.template_id)

        # 4. 文件按output_config_id分组
        template_output_file_dict = group_template_file(lambda x: x.output_config_id)

        # 5. 查询模板配置
        template_config_list = TemplateConfigSqlite().export_config_by_template_ids(self.row_ids)
        # 6. 配置分类，并将文件关联到对应的输出配置上
        template_id_output_config_dict, template_id_var_config_dict = dict(), dict()
        for config in template_config_list:
            if config.config_type == ConfigTypeEnum.output_dir.value:
                output_config_list = template_id_output_config_dict.get(config.template_id)
                if output_config_list is None:
                    output_config_list = list()
                    template_id_output_config_dict[config.template_id] = output_config_list
                output_config_list.append(config)
                # 关联文件
                config.bind_file_list = template_output_file_dict.get(config.id)
            elif config.config_type == ConfigTypeEnum.template_var.value:
                var_config_list = template_id_var_config_dict.get(config.template_id)
                if var_config_list is None:
                    var_config_list = list()
                    template_id_var_config_dict[config.template_id] = var_config_list
                var_config_list.append(config)
        # 将模板配置、模板文件都关联到模板上
        for template in template_list:
            template.template_files = template_id_file_dict.get(template.id)
            template.output_config_list = template_id_output_config_dict.get(template.id)
            template.var_config_list = template_id_var_config_dict.get(template.id)
        return [dataclasses.asdict(x) for x in template_list]

    def get_err_msg(self) -> str:
        return '导出模板失败'


class ExportTemplateExecutor(ExportDataExecutor):

    def get_worker(self) -> ExportTemplateWorker:
        return ExportTemplateWorker(self.row_ids, self.file_path)

# ----------------------- 导出类型映射 end ----------------------- #

