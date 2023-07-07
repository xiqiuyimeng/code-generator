# -*- coding: utf-8 -*-
import dataclasses

from PyQt6.QtCore import pyqtSignal

from src.constant.export_import_constant import TEMPLATE_DATA_KEY
from src.enum.common_enum import ConfigTypeEnum
from src.logger.log import logger as log
from src.service.async_func.async_import_export_task import ExportDataWorker, ExportDataExecutor, ImportDataWorker, \
    ImportDataExecutor, OverrideDataWorker, OverrideDataExecutor
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.template_config_sqlite import TemplateConfigSqlite, construct_output_config, \
    ImportExportTemplateConfig, TemplateConfig
from src.service.system_storage.template_file_sqlite import TemplateFileSqlite, ImportExportTemplateFile, TemplateFile
from src.service.system_storage.template_func_sqlite import TemplateFuncSqlite, ImportExportTemplateFunc, TemplateFunc
from src.service.system_storage.template_sqlite import TemplateSqlite, Template, ImportExportTemplate
from src.service.util.copy_util import copy_template
from src.service.util.import_export_util import convert_import_to_model, convert_import_to_model_list, \
    group_model_list, check_duplicate_template_file_name, check_template_config, batch_save_template, \
    export_template, check_template_func_name
from src.service.util.system_storage_util import transactional
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
        template = TemplateSqlite().get_template_by_id(self.template_id)
        if not template:
            raise Exception('未查询到模板信息')
        # 查询模板配置
        template_config_list = TemplateConfigSqlite().get_by_template_id(self.template_id)
        template.output_config_list, template.var_config_list = template_config_list
        # 查询模板文件列表
        template.template_files = TemplateFileSqlite().get_by_template_id(self.template_id)
        # 查询模板方法列表
        template.template_func_list = TemplateFuncSqlite().get_by_template_id(self.template_id)

        # 将模板文件按关联的输出路径配置id分组
        if template.template_files and template.output_config_list:
            template_file_dict = group_model_list(template.template_files, lambda x: x.output_config_id)
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
        TemplateFileSqlite().batch_add_template_files(self.template.id, self.template.template_files)
        # 保存模板方法
        TemplateFuncSqlite().batch_add_template_func_list(self.template.id, self.template.template_func_list)
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
        TemplateSqlite().update_by_id(self.template)
        # 保存模板输入配置信息
        TemplateConfigSqlite().batch_edit_config_list(self.template.id, self.template.output_config_list,
                                                      self.template.var_config_list)
        # 处理模板文件列表
        TemplateFileSqlite().batch_edit_template_files(self.template.id, self.template.template_files)
        # 处理模板方法列表
        TemplateFuncSqlite().batch_edit_template_func_list(self.template.id, self.template.template_func_list)
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
        # 删除模板
        TemplateSqlite().delete_by_ids(self.template_ids)
        # 删除模板配置
        TemplateConfigSqlite().batch_del_config_list(self.template_ids)
        # 删除模板文件
        TemplateFileSqlite().batch_del_template_files(self.template_ids)
        # 删除模板方法
        TemplateFuncSqlite().batch_del_template_func_list(self.template_ids)
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
        return DelTemplateWorker((self.template_id,), (self.template_name,))

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


# ----------------------- 复制模板 start ----------------------- #

class CopyTemplateWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, template_ids):
        super().__init__()
        self.template_ids = template_ids

    def do_run(self):
        template_sqlite = TemplateSqlite()
        template_file_sqlite = TemplateFileSqlite()
        template_config_sqlite = TemplateConfigSqlite()
        template_func_sqlite = TemplateFuncSqlite()
        # 根据 template ids 查询模板数据
        templates = export_template(template_sqlite, template_file_sqlite, template_config_sqlite,
                                    template_func_sqlite, self.template_ids)
        # 获取所有模板名称
        template_names = template_sqlite.get_all_names()
        # 复制模板
        copy_templates = [copy_template(template, template_names) for template in templates]
        # 保存模板
        batch_save_template(template_sqlite, template_config_sqlite, template_file_sqlite,
                            template_func_sqlite, copy_templates)
        self.success_signal.emit(copy_templates)

    def get_err_msg(self) -> str:
        return '复制模板失败'


class CopyTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_ids, *args):
        self.template_ids = template_ids
        super().__init__(*args)

    def get_worker(self) -> CopyTemplateWorker:
        return CopyTemplateWorker(self.template_ids)


# ----------------------- 复制模板 end ----------------------- #


# ----------------------- 获取模板列表 start ----------------------- #

class ListTemplateWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info("读取模板列表")
        # 读取数据库中缓存的模板列表
        template_list = TemplateSqlite().select_by_order()
        self.success_signal.emit(template_list)
        log.info("读取模板列表成功")

    def get_err_msg(self) -> str:
        return '读取模板列表失败'


class ListTemplateExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateWorker()


# ----------------------- 获取模板列表 end ----------------------- #


# ----------------------- 获取拥有模板方法的模板列表 start ----------------------- #

class ListHasFuncTemplateWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, excluded_template_id):
        super().__init__()
        self.excluded_template_id = excluded_template_id

    def do_run(self):
        log.info('读取具有模板方法的模板列表')
        templates = list()
        # 查找拥有模板方法的模板id集合
        template_ids = TemplateFuncSqlite().select_distinct_template_ids()
        # 排除模板id
        if self.excluded_template_id in template_ids:
            template_ids.remove(self.excluded_template_id)
        # 查找模板名称
        if template_ids:
            templates = TemplateSqlite().get_template_by_ids(template_ids)
        self.success_signal.emit(templates)
        log.info('读取具有模板方法的模板列表成功')

    def get_err_msg(self) -> str:
        return '读取具有模板方法的模板列表失败'


class ListHasFuncTemplateExecutor(LoadingMaskThreadExecutor):

    def __init__(self, excluded_template_id, *args):
        self.excluded_template_id = excluded_template_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ListHasFuncTemplateWorker(self.excluded_template_id)

# ----------------------- 获取拥有模板方法的模板列表 end ----------------------- #


# ----------------------- 获取模板方法列表 start ----------------------- #

class ListTemplateFuncWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self, template_id):
        super().__init__()
        self.template_id = template_id

    def do_run(self):
        log.info(f'读取模板方法列表：{self.template_id}')
        template_func_list = TemplateFuncSqlite().get_by_template_id(self.template_id)
        self.success_signal.emit(template_func_list)
        log.info(f'读取模板方法列表成功：{self.template_id}')

    def get_err_msg(self) -> str:
        return '读取模板方法列表失败'


class ListTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_id, *args):
        self.template_id = template_id
        super().__init__(*args)

    def get_worker(self) -> ListTemplateFuncWorker:
        return ListTemplateFuncWorker(self.template_id)


# ----------------------- 获取模板方法列表 end ----------------------- #


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
            output_config = construct_output_config(self.config_name_list, self.var_name_list, file.file_name)
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


# ----------------------- 导入模板 start ----------------------- #

class ImportTemplateWorker(ImportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TEMPLATE_DATA_KEY
        self.template_sqlite = ...

    def convert_to_model(self, import_data):
        template = convert_import_to_model(ImportExportTemplate, Template, import_data)
        # 处理文件
        template_file_dict = dict()
        if template.template_files:
            template.template_files = convert_import_to_model_list(ImportExportTemplateFile,
                                                                   TemplateFile, template.template_files)
            # 这里需要使用最终被赋值到模板中的模板文件对象，否则会和实际的模板文件对象不同，导致最终的保存失败
            template_file_dict = dict([(file.file_name, file) for file in template.template_files])
        # 处理输出路径配置
        if template.output_config_list:
            template.output_config_list = convert_import_to_model_list(ImportExportTemplateConfig,
                                                                       TemplateConfig, template.output_config_list)
            # 处理关联的文件
            for output_config in template.output_config_list:
                bind_file_list = list()
                if output_config.bind_file_list:
                    for bind_file in output_config.bind_file_list:
                        template_file = template_file_dict.get(bind_file.get('file_name'))
                        if template_file:
                            bind_file_list.append(template_file)
                            # 给绑定的文件分配一个虚id
                            template_file.output_config_id = -1
                if bind_file_list:
                    output_config.bind_file_list = bind_file_list
                else:
                    # 如果绑定文件数据不存在，或错误，直接清空
                    output_config.bind_file_list = None
        # 处理变量配置
        if template.var_config_list:
            template.var_config_list = convert_import_to_model_list(ImportExportTemplateConfig,
                                                                    TemplateConfig, template.var_config_list)
        # 处理模板方法
        if template.template_func_list:
            template.template_func_list = convert_import_to_model_list(ImportExportTemplateFunc,
                                                                       TemplateFunc, template.template_func_list)
        return template

    def pre_process_before_check_data(self):
        self.template_sqlite = TemplateSqlite()
        # 查出所有的模板名称
        self.exists_names = self.template_sqlite.get_all_names()

    def check_repair_illegal_data(self, data_row: Template) -> int:
        illegal_data_count = 0
        # 检查模板文件名称是否重复，如果文件名为空，自动修复，添加默认值
        if data_row.template_files:
            illegal_data_count += check_duplicate_template_file_name(data_row.template_files)

        # 检查输出路径配置
        if data_row.output_config_list:
            error_name_count, error_var_name_count = check_template_config(data_row.output_config_list,
                                                                           ConfigTypeEnum.output_dir.value)
            illegal_data_count += error_name_count + error_var_name_count
        else:
            data_row.output_config_list = list()
        # 检查变量配置
        if data_row.var_config_list:
            error_name_count, error_var_name_count = check_template_config(data_row.var_config_list,
                                                                           ConfigTypeEnum.template_var.value)
            illegal_data_count += error_name_count + error_var_name_count
        else:
            data_row.var_config_list = list()
        # 检查模板方法名称
        if data_row.template_func_list:
            illegal_data_count += check_template_func_name(data_row.template_func_list)
        return illegal_data_count

    @transactional
    def import_data(self, data_list):
        # 批量保存模板
        batch_save_template(self.template_sqlite, TemplateConfigSqlite(), TemplateFileSqlite(),
                            TemplateFuncSqlite(), data_list)

    def get_err_msg(self) -> str:
        return '导入模板失败'


class ImportTemplateExecutor(ImportDataExecutor):

    def get_worker(self) -> ImportTemplateWorker:
        return ImportTemplateWorker(self.file_path)


# ----------------------- 导入模板 end ----------------------- #


# ----------------------- 覆盖数据 start ----------------------- #

class OverrideTemplateWorker(OverrideDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.template_sqlite = ...
        self.template_file_sqlite = ...
        self.template_config_sqlite = ...
        self.template_func_sqlite = ...

    def batch_delete_origin_data(self):
        self.template_sqlite = TemplateSqlite()
        self.template_file_sqlite = TemplateFileSqlite()
        self.template_config_sqlite = TemplateConfigSqlite()
        self.template_func_sqlite = TemplateFuncSqlite()

        id_list = self.template_sqlite.get_id_by_names(self.data_list)
        self.template_sqlite.delete_by_ids(id_list)
        self.template_file_sqlite.batch_del_template_files(id_list)
        self.template_config_sqlite.batch_del_config_list(id_list)
        self.template_func_sqlite.batch_del_template_func_list(id_list)

    def batch_insert_data_list(self):
        # 批量保存模板
        batch_save_template(self.template_sqlite, self.template_config_sqlite, self.template_file_sqlite,
                            self.template_func_sqlite, self.data_list)

    def get_err_msg(self) -> str:
        return '覆盖模板数据失败'


class OverrideTemplateExecutor(OverrideDataExecutor):

    def get_worker(self) -> OverrideTemplateWorker:
        return OverrideTemplateWorker(self.data_list)


# ----------------------- 覆盖数据 end ----------------------- #


# ----------------------- 导出类型映射 start ----------------------- #

class ExportTemplateWorker(ExportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TEMPLATE_DATA_KEY

    def export_data(self) -> list[dataclasses.dataclass]:
        return export_template(TemplateSqlite(), TemplateFileSqlite(), TemplateConfigSqlite(),
                               TemplateFuncSqlite(), self.row_ids)

    def get_err_msg(self) -> str:
        return '导出模板失败'


class ExportTemplateExecutor(ExportDataExecutor):

    def get_worker(self) -> ExportTemplateWorker:
        return ExportTemplateWorker(self.row_ids, self.file_path)

# ----------------------- 导出类型映射 end ----------------------- #
