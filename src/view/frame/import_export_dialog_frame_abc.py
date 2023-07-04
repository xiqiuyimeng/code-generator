# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QAction, QPushButton

from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.frame.frame_func import construct_lineedit_file_action

_author_ = 'luwt'
_date_ = '2023/5/10 11:28'


class ImportExportDialogFrameABC(DialogFrameABC):
    """导入导出对话框框架抽象类"""

    def __init__(self, *args):
        self.blank_label: QLabel = ...
        self.form_layout: QFormLayout = ...
        self.file_path_label: QLabel = ...
        self.file_path_linedit: QLineEdit = ...
        self.choose_file_action: QAction = ...
        self.start_process_button: QPushButton = ...
        # 导入导出执行器
        self.process_data_executor: LoadingMaskThreadExecutor = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.blank_label = QLabel(self)
        self.frame_layout.addWidget(self.blank_label)

        self.form_layout = QFormLayout(self)
        self.frame_layout.addLayout(self.form_layout)

        self.file_path_label, self.file_path_linedit, self.choose_file_action = construct_lineedit_file_action()
        self.form_layout.addRow(self.file_path_label, self.file_path_linedit)

        # 允许子类添加组件
        self.setup_child_content()

    def setup_child_content(self):
        ...

    def get_blank_right_buttons(self) -> tuple:
        self.start_process_button = QPushButton(self)
        self.start_process_button.setObjectName('save_button')
        return self.start_process_button,

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.file_path_linedit.textChanged.connect(self.file_path_change)
        self.choose_file_action.triggered.connect(self.choose_file)
        self.start_process_button.clicked.connect(self.process_data)

    def file_path_change(self, file_path):
        # 操作按钮是否禁用应该根据是否存在文件路径决定
        self.start_process_button.setDisabled(not bool(file_path))

    def choose_file(self):
        ...

    def process_data(self):
        self.process_data_executor = self.get_process_data_executor()
        self.process_data_executor.start()

    def get_process_data_executor(self) -> LoadingMaskThreadExecutor: ...

    # ------------------------------ 信号槽处理 end ------------------------------ #
