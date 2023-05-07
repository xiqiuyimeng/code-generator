# -*- coding: utf-8 -*-
import os.path

from PyQt5.QtCore import pyqtSignal
from jinja2 import Template

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, ThreadExecutorABC
from src.service.system_storage.col_type_mapping_sqlite import ColTypeMappingSqlite
from src.service.system_storage.template_file_sqlite import TemplateFileSqlite
from src.service.system_storage.template_func_sqlite import TemplateFuncSqlite
from src.service.util.generate_util import convert_complete_table_cols
from src.service.util.path_util import check_path_legal

_author_ = 'luwt'
_date_ = '2023/4/26 11:16'


# ----------------------- 生成 start ----------------------- #

class GenerateWorker(ThreadWorkerABC):
    # 准备工作相关的信号
    prepare_progress_signal = pyqtSignal(int)
    # 生成相关的信号
    generate_progress_signal = pyqtSignal(int)
    # 文件名称、文件内容、文件目录
    generate_file_signal = pyqtSignal(str, str, str)
    generate_log_signal = pyqtSignal(str)

    def __init__(self, selected_data, type_mapping_id, template, output_config_input_dict,
                 var_config_input_dict, save_file=True, err_msg=None):
        super().__init__()
        self.selected_data = selected_data
        self.type_mapping_id = type_mapping_id
        self.template = template
        self.output_config_input_dict = dict() if output_config_input_dict is Ellipsis else output_config_input_dict
        self.var_config_input_dict = dict() if var_config_input_dict is Ellipsis else var_config_input_dict
        self.save_file = save_file
        self.err_msg = err_msg

    def do_run(self):
        generate_type = '生成到文件' if self.save_file else '预览生成'
        log.info(f'{generate_type} 开始')
        # 1. 首先判断，如果是生成到文件，是否存在模板输出配置，不存在则提示退出
        if self.save_file and not self.template.output_config_list:
            raise Exception('未检测到模板文件输出配置，无法生成到文件，退出！')
        # 2. 获取模板文件
        template_files = TemplateFileSqlite().get_by_template_id(self.template.id)
        # 检测模板文件是否存在，如果不存在，则提示退出
        if not template_files:
            raise Exception('未能获取到模板文件，无法生成代码，退出！')
        self.prepare_progress_signal.emit(20)

        # 3. 获取类型映射列数据
        type_mapping_dict = self.get_type_mapping_dict()
        self.prepare_progress_signal.emit(40)

        # 4. 检查完善选中数据，如果选中数据没有列数据，需要补充列数据
        table_col_dict = convert_complete_table_cols(self.selected_data, type_mapping_dict)
        self.prepare_progress_signal.emit(60)

        # 5. 获取模板方法
        template_func_list = TemplateFuncSqlite().get_all_func()
        template_func_dict = dict()
        for template_func in template_func_list:
            try:
                # 加载方法体
                exec(template_func.func_body)
                # 将方法名放入字典中
                template_func_dict[template_func.func_name] = eval(template_func.func_name)
            except Exception as e:
                # 如果加载方法失败，说明方法本身有问题
                load_func_err_msg = f'方法[{template_func.func_name}]加载失败！请检查方法语法是否正确'
                self.generate_log_signal.emit(load_func_err_msg)
                log.exception(load_func_err_msg, e)
        self.prepare_progress_signal.emit(80)

        # 6. 收集变量配置，k：输出变量名称，v：用户输入值
        output_config_dict = dict(map(lambda x: (x.output_var_name, self.output_config_input_dict.get(x.id)),
                                      self.template.output_config_list))
        var_config_dict = dict(map(lambda x: (x.output_var_name, self.var_config_input_dict.get(x.id)),
                                   self.template.var_config_list))
        self.prepare_progress_signal.emit(100)

        # 7. 准备字段开始生成
        # 需要生成的总文件数为 表数 × 模板文件数
        total_file_count = len(table_col_dict) * len(template_files)
        current_file_index = 0
        for template_file in template_files:
            # 获取当前模板文件，用户输入的输出路径
            file_path = self.output_config_input_dict.get(template_file.output_config_id)
            # 如果没有获取到用户输入路径或路径不合法，跳过
            if not file_path or not check_path_legal(file_path):
                current_file_index += len(table_col_dict)
                self.generate_log_signal.emit(f'模板文件：{template_file.file_name}，'
                                              f'当前输出路径为：{file_path}，输出路径不合法，跳过！')
                # 计算当前进度
                self.generate_progress_signal.emit(current_file_index * 100 // total_file_count)
                continue

            # 如果是保存到文件，提前创建目录
            if self.save_file and not os.path.exists(file_path):
                os.makedirs(file_path)

            # 动态生成文件名的模板，如果不存在文件名称模板，那么取文件名，这样会导致重复
            file_name_template = Template(template_file.file_name_template
                                          if template_file.file_name_template else template_file.file_name,
                                          trim_blocks=True, lstrip_blocks=True)
            # 生成文件内容的模板
            template = Template(template_file.file_content, trim_blocks=True, lstrip_blocks=True)

            for table_name, col_list in table_col_dict.items():
                # 生成文件名只需要表名和方法
                file_name = file_name_template.render(table_name=table_name, template_func=template_func_dict)
                # 拼接完整输出路径
                full_file_path = os.path.join(file_path, file_name)

                # 生成文件，放入所有可用的变量
                generated_content = template.render(table_name=table_name, col_list=col_list,
                                                    template_func=template_func_dict,
                                                    output_config=output_config_dict,
                                                    var_config=var_config_dict)
                current_file_index += 1

                # 计算当前进度
                self.generate_progress_signal.emit(current_file_index * 100 // total_file_count)
                # 日志信号
                self.generate_log_signal.emit(f'数据表：{table_name} 生成路径：{full_file_path}')
                # 如果是预览生成，将文件发送出去；如果是生成到文件模式，直接写入文件
                if self.save_file:
                    with open(full_file_path, 'w', encoding='utf-8')as f:
                        f.write(generated_content)
                else:
                    # 解析路径结构
                    self.generate_file_signal.emit(file_name, generated_content, file_path)
        self.success_signal.emit()
        log.info(f'{generate_type} 结束')

    def get_type_mapping_dict(self):
        col_type_mapping_list = ColTypeMappingSqlite().get_by_parent_id(self.type_mapping_id)
        # 两层字典嵌套，{数据源列类型: {映射列名称: 类型映射对象}}
        type_mapping_dict = dict()
        for type_mapping in col_type_mapping_list:
            type_mapping_group_dict = type_mapping_dict.get(type_mapping.ds_col_type)
            if not type_mapping_group_dict:
                # 以组的维度，再次放入子级字典中
                type_mapping_group_dict = dict()
                type_mapping_dict[type_mapping.ds_col_type] = type_mapping_group_dict
            type_mapping_group_dict[type_mapping.mapping_col_name] = type_mapping
        return type_mapping_dict

    def get_err_msg(self) -> str:
        return self.err_msg


class GenerateExecutorABC(ThreadExecutorABC):

    def __init__(self, selected_data, type_mapping_id, template,
                 output_config_input_dict, var_config_input_dict, button_list,
                 prepare_progress_callback, generate_progress_callback,
                 generate_log_callback, *args, generate_file_callback=None,
                 save_file=True, err_msg=None):
        self.selected_data = selected_data
        self.type_mapping_id = type_mapping_id
        self.template = template
        self.output_config_input_dict = output_config_input_dict
        self.var_config_input_dict = var_config_input_dict
        self.button_list = button_list
        self.prepare_progress_callback = prepare_progress_callback
        self.generate_progress_callback = generate_progress_callback
        self.generate_log_callback = generate_log_callback
        self.generate_file_callback = generate_file_callback
        self.save_file = save_file
        self.err_msg = err_msg
        super().__init__(*args)
        # 连接信号
        self.worker.prepare_progress_signal.connect(self.prepare_progress_callback)
        self.worker.generate_progress_signal.connect(self.generate_progress_callback)
        self.worker.generate_log_signal.connect(self.generate_log_callback)
        if not self.save_file:
            self.worker.generate_file_signal.connect(self.generate_file_callback)

    def pre_process(self):
        # 禁用这些按钮
        [button.setDisabled(True) for button in self.button_list]

    def get_worker(self) -> ThreadWorkerABC:
        return GenerateWorker(self.selected_data, self.type_mapping_id, self.template,
                              self.output_config_input_dict, self.var_config_input_dict,
                              save_file=self.save_file, err_msg=self.err_msg)

    def post_process(self):
        # 恢复按钮状态
        [button.setDisabled(False) for button in self.button_list]


class GenerateExecutor(GenerateExecutorABC):

    def __init__(self, *args):
        super().__init__(*args, err_msg='生成失败')


class PreviewGenerateExecutor(GenerateExecutorABC):

    def __init__(self, *args, generate_file_callback):
        super().__init__(*args, generate_file_callback=generate_file_callback,
                         save_file=False, err_msg='预览生成失败')

# ----------------------- 生成 end ----------------------- #


# ----------------------- 写入文件 start ----------------------- #

class SaveFileWorker(ThreadWorkerABC):
    save_progress_signal = pyqtSignal(int)

    def __init__(self, file_dict):
        super().__init__()
        self.file_dict = file_dict

    def do_run(self):
        file_count = len(self.file_dict)
        for idx, file_item in enumerate(self.file_dict.items(), start=1):
            file_name, file_value = file_item
            file_path, file_content = file_value
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            with open(os.path.join(file_path, file_name), 'w', encoding='utf-8')as f:
                f.write(file_content)
            self.save_progress_signal.emit(idx * 100 // file_count)
        self.success_signal.emit()

    def get_err_msg(self) -> str:
        return '保存到文件失败'


class SaveFileExecutor(ThreadExecutorABC):

    def __init__(self, file_dict, button, save_progress_callback, *args):
        self.file_dict = file_dict
        self.button = button
        super().__init__(*args)
        self.worker.save_progress_signal.connect(save_progress_callback)

    def pre_process(self):
        self.button.setDisabled(True)

    def get_worker(self) -> ThreadWorkerABC:
        return SaveFileWorker(self.file_dict)

    def post_process(self):
        self.button.setDisabled(False)

# ----------------------- 写入文件 end ----------------------- #
