# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.help.help_constant import TEMPLATE_FUNC_DETAIL_HELP
from src.constant.template_dialog_constant import TEMPLATE_FUNC_NAME_PLACEHOLDER_TEXT
from src.service.system_storage.template_func_sqlite import TemplateFunc
from src.view.custom_widget.py_func_editor import PyFuncEditor
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 18:35'


class TemplateFuncDetailDialogFrame(NameCheckDialogFrame):
    """模板方法详情对话框框架"""
    save_signal = pyqtSignal(TemplateFunc)
    edit_signal = pyqtSignal(TemplateFunc)

    def __init__(self, parent_dialog, title, exists_func_names, template_func=None):
        self.dialog_data: TemplateFunc = ...
        self.new_dialog_data: TemplateFunc = ...
        self.text_editor: PyFuncEditor = ...
        super().__init__(parent_dialog, title, exists_func_names, template_func, False)

    def get_new_dialog_data(self) -> TemplateFunc:
        return TemplateFunc()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_content_ui(self):
        self.text_editor = PyFuncEditor(self)
        self.frame_layout.addWidget(self.text_editor)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_FUNC_DETAIL_HELP

    def collect_input(self):
        self.new_dialog_data.func_name = self.name_input.text()
        self.new_dialog_data.func_body = self.text_editor.toPlainText()

    def button_available(self) -> bool:
        return self.name_available

    def check_data_changed(self) -> bool:
        return self.new_dialog_data != self.dialog_data

    def connect_child_signal(self):
        self.name_input.textChanged.connect(self.check_name_available)
        self.text_editor.textChanged.connect(self.parse_func_name)
        self.text_editor.textChanged.connect(self.check_input)

    def parse_func_name(self):
        # 解析方法名，如果存在多个，取第一个
        self.name_input.setText(self.text_editor.parse_func_name())

    def save_func(self):
        # 如果存在原数据，说明是编辑
        if self.dialog_data:
            self.edit_signal.emit(self.new_dialog_data)
        else:
            self.save_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 名称框不可编辑
        self.name_input.setDisabled(True)

    def setup_input_limit_rule(self):
        ...

    def setup_placeholder_text(self):
        self.name_input.setPlaceholderText(TEMPLATE_FUNC_NAME_PLACEHOLDER_TEXT)

    def check_edit(self):
        """判断是否是编辑"""
        return self.dialog_data

    def get_old_name(self) -> str:
        return self.dialog_data.func_name

    def setup_echo_other_data(self):
        self.text_editor.setPlainText(self.dialog_data.func_body)

    # ------------------------------ 后置处理 end ------------------------------ #
