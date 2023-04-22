# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.template_dialog_constant import AUTO_GENERATE_OUTPUT_CONFIG_BTN_TEXT, MAINTAIN_FILE_CONFIG_BTN_TEXT, \
    NO_IRRELEVANT_FILE_PROMPT, GENERATE_FILE_CONFIG_TITLE, GENERATE_CONFIG_FAIL_PROMPT
from src.service.async_func.async_template_task import AutoGenerateOutputConfigExecutor
from src.service.system_storage.template_config_sqlite import ConfigTypeEnum
from src.view.table.table_widget.template_table_widget.template_config_table_widget import \
    TemplateOutputConfigTableWidget
from src.view.widget.template.template_config_widget import TemplateConfigWidget
from src.view.box.message_box import pop_fail

_author_ = 'luwt'
_date_ = '2023/4/12 14:39'


class TemplateOutputConfigWidget(TemplateConfigWidget):
    """模板输出路径配置表格页面控件"""

    def __init__(self, parent_frame, *args):
        # 父框架
        self.parent_frame = parent_frame
        # 一键生成输出文件对应路径配置按钮
        self.auto_generate_config_btn: QPushButton = ...
        # 维护文件和输出路径配置关系按钮
        self.maintain_file_config_btn: QPushButton = ...
        # 维护文件和输出路径的对话框
        self.maintain_file_config_dialog = ...
        # 自动生成文件对应路径配置执行器
        self.generate_config_executor: AutoGenerateOutputConfigExecutor = ...
        super().__init__(ConfigTypeEnum.output_dir.value, *args)

    def setup_other_button_ui(self):
        # 插入到预览配置页之前
        self.auto_generate_config_btn = QPushButton()
        self.config_btn_layout.addWidget(self.auto_generate_config_btn, 0, 2, 1, 1)
        self.maintain_file_config_btn = QPushButton()
        self.config_btn_layout.addWidget(self.maintain_file_config_btn, 0, 3, 1, 1)

        self.config_btn_layout.addWidget(self.preview_config_btn, 0, 4, 1, 1)

    def get_table_widget(self) -> TemplateOutputConfigTableWidget:
        return TemplateOutputConfigTableWidget(self)

    def setup_other_label_text(self):
        self.auto_generate_config_btn.setText(AUTO_GENERATE_OUTPUT_CONFIG_BTN_TEXT)
        self.maintain_file_config_btn.setText(MAINTAIN_FILE_CONFIG_BTN_TEXT)

    def connect_other_signal(self):
        self.auto_generate_config_btn.clicked.connect(self.auto_generate_config)
        self.maintain_file_config_btn.clicked.connect(self.maintain_file_config)

    def auto_generate_config(self):
        irrelevant_config_files = self.parent_frame.file_list_widget.collect_irrelevant_config_files()
        if not irrelevant_config_files:
            pop_fail(NO_IRRELEVANT_FILE_PROMPT, GENERATE_FILE_CONFIG_TITLE, self)
        else:
            # 生成文件输出配置，并关联文件
            config_names, var_names = self.config_table.get_exists_names_and_var_names()
            self.generate_config_executor = AutoGenerateOutputConfigExecutor(config_names, var_names,
                                                                             irrelevant_config_files,
                                                                             self, self,
                                                                             GENERATE_FILE_CONFIG_TITLE,
                                                                             self.auto_generate_config_callback)
            self.generate_config_executor.start()

    def auto_generate_config_callback(self, success_list, fail_list):
        if success_list:
            # 成功生成的配置，自动添加到表格中
            [self.config_table.add_row(config) for config in success_list]
        if fail_list:
            # 未成功生成配置的文件，提示
            pop_fail(GENERATE_CONFIG_FAIL_PROMPT.format('\n'.join(fail_list)), GENERATE_FILE_CONFIG_TITLE, self)

    def maintain_file_config(self):
        ...
