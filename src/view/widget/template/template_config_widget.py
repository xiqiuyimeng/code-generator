# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton

from src.constant.template_dialog_constant import ADD_CONFIG_BTN_TEXT, REMOVE_CONFIG_BTN_TEXT, PREVIEW_CONFIG_BTN_TEXT
from src.service.util.import_export_util import check_template_config
from src.view.box.message_box import pop_fail
from src.view.dialog.template.template_config_dialog import TemplateConfigDialog
from src.view.dialog.template.template_config_preview_dialog import TemplateConfigPreviewDialog
from src.view.table.table_widget.template_table_widget.template_config_table_widget import TemplateConfigTableWidgetABC

_author_ = 'luwt'
_date_ = '2023/3/21 17:06'


class TemplateConfigWidget(QWidget):
    """模板配置页，嵌入在堆栈式窗口中"""

    def __init__(self, config_type):
        super().__init__()
        # 配置类型
        self.config_type = config_type
        self.config_layout: QVBoxLayout = ...
        self.config_btn_layout: QGridLayout = ...
        self.add_config_btn: QPushButton = ...
        self.remove_config_btn: QPushButton = ...
        self.preview_config_btn: QPushButton = ...
        # 预览配置页
        self.preview_config_dialog: TemplateConfigPreviewDialog = ...
        self.config_table: TemplateConfigTableWidgetABC = ...
        self.config_row_dialog: TemplateConfigDialog = ...

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()
        self.post_process()

    def setup_ui(self):
        self.config_layout = QVBoxLayout()
        self.setLayout(self.config_layout)
        # 第一部分，按钮区
        self.config_btn_layout = QGridLayout()
        self.config_layout.addLayout(self.config_btn_layout)
        self.add_config_btn = QPushButton()
        self.config_btn_layout.addWidget(self.add_config_btn, 0, 0, 1, 1)
        self.remove_config_btn = QPushButton()
        self.config_btn_layout.addWidget(self.remove_config_btn, 0, 1, 1, 1)
        self.preview_config_btn = QPushButton()
        self.config_btn_layout.addWidget(self.preview_config_btn, 0, 2, 1, 1)
        self.setup_other_button_ui()

        # 第二部分，表格区
        self.config_table = self.get_table_widget()
        self.config_layout.addWidget(self.config_table)

    def setup_other_button_ui(self):
        ...

    def get_table_widget(self) -> TemplateConfigTableWidgetABC:
        ...

    def setup_label_text(self):
        self.add_config_btn.setText(ADD_CONFIG_BTN_TEXT)
        self.remove_config_btn.setText(REMOVE_CONFIG_BTN_TEXT)
        self.preview_config_btn.setText(PREVIEW_CONFIG_BTN_TEXT)
        self.setup_other_label_text()

    def setup_other_label_text(self):
        ...

    def connect_signal(self):
        self.add_config_btn.clicked.connect(lambda: self.open_config_row_dialog())
        self.remove_config_btn.clicked.connect(self.config_table.remove_rows)
        # 连接表格中行编辑信号
        self.config_table.row_edit_signal.connect(self.open_config_row_dialog)
        # 配置表格中行删除信号
        self.config_table.row_del_signal.connect(lambda row_id, row_index, config_name:
                                                 self.config_table.remove_row(row_index, config_name))
        # 输出配置表头复选框状态变化信号
        self.config_table.header_widget.header_check_changed.connect(self.set_remove_btn_available)
        self.preview_config_btn.clicked.connect(self.preview_template_config)
        self.connect_other_signal()

    def connect_other_signal(self):
        ...

    def open_config_row_dialog(self, config_data=None, row_index=None):
        # 获取配置项名称列表、配置变量名称列表，这两项都不可以重复
        config_names, config_var_names = self.config_table.get_exists_names_and_var_names()
        self.config_row_dialog = TemplateConfigDialog(config_names, config_var_names, self.config_type, config_data)
        if config_data:
            self.config_row_dialog.edit_signal.connect(lambda template_config:
                                                       self.config_table.edit_row(row_index, template_config))
        else:
            self.config_row_dialog.save_signal.connect(self.config_table.add_row)
        self.config_row_dialog.exec()

    def set_remove_btn_available(self, checked):
        # 如果表格存在行，删除按钮状态根据传入状态变化，否则应该置为不可用
        if self.config_table.rowCount():
            self.remove_config_btn.setDisabled(not checked)
        else:
            self.remove_config_btn.setDisabled(True)

    def preview_template_config(self):
        # 预览配置页
        self.preview_config_dialog = TemplateConfigPreviewDialog(self.config_type, self.config_table.collect_data())
        self.preview_config_dialog.exec()

    def collect_template_config(self):
        return self.config_table.collect_data()

    def post_process(self):
        self.set_remove_btn_available(False)

    def echo_config_table(self, config_list):
        self.config_table.fill_table(config_list)

    def check_config_completable(self, config_list) -> bool:
        if config_list:
            error_name_count, error_var_name_count = check_template_config(config_list, self.config_type)
            check_title_prompt = self.get_check_title_prompt()
            if error_name_count:
                pop_fail(check_title_prompt[0], check_title_prompt[1], self)
                return False
            if error_var_name_count:
                pop_fail(check_title_prompt[2], check_title_prompt[3], self)
                return False
        return True

    def get_check_title_prompt(self) -> tuple:
        ...
