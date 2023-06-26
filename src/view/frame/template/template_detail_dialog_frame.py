# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTabWidget

from src.constant.export_import_constant import OVERRIDE_TEMPLATE_TITLE
from src.constant.help.help_constant import TEMPLATE_DETAIL_HELP
from src.constant.template_dialog_constant import TEMPLATE_INFO_TEXT, TEMPLATE_CONFIG_TEXT, TEMPLATE_FILE_TEXT, \
    TEMPLATE_NAME, TEMPLATE_DESC, EDIT_TEMPLATE_BOX_TITLE, ADD_TEMPLATE_BOX_TITLE, READ_TEMPLATE_BOX_TITLE, \
    TEMPLATE_OUTPUT_DIR_TAB_TEXT, \
    TEMPLATE_VAR_CONFIG_TAB_TEXT, TEMPLATE_FUNC_TEXT
from src.service.async_func.async_template_task import AddTemplateExecutor, EditTemplateExecutor, \
    ReadTemplateExecutor, OverrideTemplateExecutor
from src.service.system_storage.template_sqlite import Template
from src.view.custom_widget.text_editor import TextEditor
from src.view.frame.stacked_dialog_frame import StackedDialogFrame
from src.view.widget.template.template_file_widget import TemplateFileWidget
from src.view.widget.template.template_func_widget import TemplateFuncWidget
from src.view.widget.template.template_ouput_config_widget import TemplateOutputConfigWidget
from src.view.widget.template.template_var_config_widget import TemplateVarConfigWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:29'


class TemplateDetailDialogFrame(StackedDialogFrame):
    """模板详情对话框框架"""
    save_signal = pyqtSignal(Template)
    edit_signal = pyqtSignal(Template)
    override_signal = pyqtSignal(list, list)

    def __init__(self, parent_dialog, dialog_title, exists_template_names, template_id=None):
        self.dialog_data: Template = ...
        self.new_dialog_data: Template = ...
        # 标记当前是否是用来展示导入错误数据详情页
        self.import_error_data = False

        # 第一个窗口，模板基本信息窗口
        self.template_info_widget: QWidget = ...
        self.template_info_layout: QVBoxLayout = ...
        # 模板说明输入控件
        self.template_desc_label: QLabel = ...
        self.template_desc_text_edit: TextEditor = ...

        # 第二个窗口，模板配置窗口
        self.config_tab_widget: QTabWidget = ...
        self.output_config_widget: TemplateOutputConfigWidget = ...
        self.var_config_widget: TemplateVarConfigWidget = ...

        # 第三个窗口，模板文件页窗口
        self.template_file_widget: TemplateFileWidget = ...

        # 第四个窗口，模板方法窗口
        self.template_func_widget: TemplateFuncWidget = ...

        # 添加模板执行器
        self.add_template_executor: AddTemplateExecutor = ...
        # 编辑模板执行器
        self.edit_template_executor: EditTemplateExecutor = ...
        # 覆盖导入模板执行器
        self.override_data_executor: OverrideTemplateExecutor = ...
        super().__init__(parent_dialog, dialog_title, exists_template_names, template_id)

    def get_new_dialog_data(self) -> Template:
        return Template()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def fill_list_widget(self):
        self.list_widget.addItem(TEMPLATE_INFO_TEXT)
        self.list_widget.addItem(TEMPLATE_CONFIG_TEXT)
        self.list_widget.addItem(TEMPLATE_FILE_TEXT)
        self.list_widget.addItem(TEMPLATE_FUNC_TEXT)

    def fill_stacked_widget(self):
        # 第一个窗口，模板名称、模板说明输入框
        self.template_info_widget = QWidget(self)
        self.stacked_widget.addWidget(self.template_info_widget)
        self.template_info_layout = QVBoxLayout()
        self.template_info_widget.setLayout(self.template_info_layout)
        # 基本信息输入表单
        self.setup_template_info_ui()

        # 第二个窗口，模板配置页
        self.config_tab_widget = QTabWidget(self)
        self.stacked_widget.addWidget(self.config_tab_widget)
        self.setup_template_config_ui()

        # 第三个窗口，模板文件页
        self.template_file_widget = TemplateFileWidget()
        self.stacked_widget.addWidget(self.template_file_widget)

        # 第四个窗口，模板方法窗口
        self.template_func_widget = TemplateFuncWidget(self.dialog_data)
        self.stacked_widget.addWidget(self.template_func_widget)

    def setup_template_info_ui(self):
        # 构建模板名称输入表单
        self.setup_name_form()
        self.template_info_layout.addLayout(self.name_layout)

        # 模板说明文本输入框
        self.template_desc_label = QLabel(self)
        self.template_desc_text_edit = TextEditor(self)
        self.name_layout.addRow(self.template_desc_label, self.template_desc_text_edit)

    def setup_template_config_ui(self):
        # 第一个页面为输出路径配置页
        self.output_config_widget = TemplateOutputConfigWidget(self)
        self.config_tab_widget.addTab(self.output_config_widget, TEMPLATE_OUTPUT_DIR_TAB_TEXT)
        # 第二个页面为模板变量配置页
        self.var_config_widget = TemplateVarConfigWidget()
        self.config_tab_widget.addTab(self.var_config_widget, TEMPLATE_VAR_CONFIG_TAB_TEXT)

    def setup_other_label_text(self):
        self.name_label.setText(TEMPLATE_NAME)
        self.template_desc_label.setText(TEMPLATE_DESC)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_DETAIL_HELP

    def collect_input(self):
        # 收集基本信息数据
        self.new_dialog_data.template_name = self.name_input.text()
        self.new_dialog_data.template_desc = self.template_desc_text_edit.toPlainText()
        # 收集模板配置数据
        self.new_dialog_data.output_config_list = self.output_config_widget.collect_template_config()
        self.new_dialog_data.var_config_list = self.var_config_widget.collect_template_config()
        # 收集模板文件数据
        self.new_dialog_data.template_files = self.template_file_widget.collect_template_files()
        # 收集模板方法数据
        self.new_dialog_data.template_func_list = self.template_func_widget.collect_template_func_list()

    def button_available(self) -> bool:
        return all((self.new_dialog_data.template_name, self.name_available))

    def save_func(self):
        # 手动收集数据
        self.collect_input()
        # 校验模板数据是否完整
        if self.check_template_completable():
            # 如果存在原数据，说明是编辑
            if self.dialog_data and not self.import_error_data:
                self.new_dialog_data.id = self.dialog_data.id
                self.edit_template_executor = EditTemplateExecutor(self.new_dialog_data, self.parent_dialog,
                                                                   self.parent_dialog, EDIT_TEMPLATE_BOX_TITLE,
                                                                   self.edit_post_process)
                self.edit_template_executor.start()
            else:
                # 如果名称存在，那么是覆盖模式
                if self.new_dialog_data.template_name in self.exits_names:
                    self.override_data_executor = OverrideTemplateExecutor((self.new_dialog_data,), self, self,
                                                                           OVERRIDE_TEMPLATE_TITLE,
                                                                           success_callback=self.override_post_process)
                    self.override_data_executor.start()
                else:
                    self.add_template_executor = AddTemplateExecutor(self.new_dialog_data, self.parent_dialog,
                                                                     self.parent_dialog, ADD_TEMPLATE_BOX_TITLE,
                                                                     self.add_post_process)
                    self.add_template_executor.start()

    def check_template_completable(self):
        # 检查配置数据是否正确，主要是针对于回显过来的数据，例如导入的数据，进行校验
        return self.output_config_widget.check_config_completable(self.new_dialog_data.output_config_list) \
            and self.var_config_widget.check_config_completable(self.new_dialog_data.var_config_list) \
            and self.template_file_widget.check_file_completable(self.new_dialog_data.template_files)

    def add_post_process(self):
        self.save_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    def override_post_process(self, add_data_list, del_data_list):
        self.override_signal.emit(add_data_list, del_data_list)
        self.parent_dialog.close()

    def edit_post_process(self):
        self.edit_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_read_storage_executor(self, callback):
        return ReadTemplateExecutor(self.dialog_data, self.parent_dialog, self.parent_dialog,
                                    READ_TEMPLATE_BOX_TITLE, callback)

    def get_old_name(self) -> str:
        return self.dialog_data.template_name

    def setup_echo_other_data(self):
        self.template_desc_text_edit.setPlainText(self.dialog_data.template_desc)
        # 回显模板配置数据
        self.output_config_widget.echo_config_table(self.dialog_data.output_config_list)
        self.var_config_widget.echo_config_table(self.dialog_data.var_config_list)
        # 回显文件列表
        self.template_file_widget.echo_template_files(self.dialog_data.template_files)
        # 回显方法列表
        self.template_func_widget.echo_template_func_list(self.dialog_data.template_func_list)
        # 如果是回显导入的错误数据，那么将保存按钮打开
        if self.import_error_data:
            self.save_button.setDisabled(False)

    # ------------------------------ 后置处理 end ------------------------------ #

    def collect_unbind_config_files(self):
        return self.template_file_widget.collect_unbind_config_files()
