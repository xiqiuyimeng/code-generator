# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel

from src.view.custom_widget.text_editor import TextEditor
from src.view.frame.frame_func import check_text_available
from src.view.frame.save_dialog_frame import SaveDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/19 17:07'


class TableItemInputDelegateDialogFrame(SaveDialogFrame):
    """表格单元格输入框代理对话框框架"""
    save_signal = pyqtSignal(str)
    
    def __init__(self, *args, check_text_duplicate=True, duplicate_prompt=None):
        # 是否校验数据重复问题
        self.check_text_duplicate = check_text_duplicate
        # 当数据重复时，提示语
        self.duplicate_prompt = duplicate_prompt
        # 已存在的数据列表
        self.exists_data_list = ...
        self.text_editor: TextEditor = ...
        self.text_checker: QLabel = ...
        super().__init__(*args, need_help_button=False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 拦截回车键，避免在编辑器内回车触发对话框关闭事件
            ...
        else:
            super().keyPressEvent(event)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.text_editor = TextEditor(self)
        self.frame_layout.addWidget(self.text_editor)

        # 文本内容检测重复提示
        if self.check_text_duplicate:
            self.text_checker = QLabel(self)
            self.frame_layout.addWidget(self.text_checker)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        if self.check_text_duplicate:
            self.text_editor.textChanged.connect(self.check_text_available)

    def check_text_available(self):
        if self.check_text_duplicate:
            text_available = check_text_available(self.text_editor.toPlainText(), self.exists_data_list,
                                                  self.text_checker, self.duplicate_prompt)
            if text_available:
                self.save_button.setDisabled(False)
            else:
                self.save_button.setDisabled(True)

    def save_func(self):
        self.save_signal.emit(self.text_editor.toPlainText())
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    def echo_dialog_data(self, data):
        self.text_editor.setPlainText(data)

    def set_exists_data_list(self, exists_data_list):
        self.exists_data_list = exists_data_list
