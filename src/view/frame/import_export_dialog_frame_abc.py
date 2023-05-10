# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QAction, QPushButton, QFileDialog

from src.constant.export_import_constant import IMPORT_EXPORT_SELECT_FILE_ICON, CHOOSE_FILE_TEXT
from src.constant.icon_enum import get_icon
from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.frame.dialog_frame_abc import DialogFrameABC

_author_ = 'luwt'
_date_ = '2023/5/10 11:28'


class ImportExportDialogFrameABC(DialogFrameABC):

    def __init__(self, get_executor_func, *args):
        # 获取执行器的方法
        self.get_executor_func = get_executor_func
        self.blank_label: QLabel = ...
        self.form_layout: QFormLayout = ...
        self.file_path_label: QLabel = ...
        self.file_path_linedit: QLineEdit = ...
        self.open_file_dialog_action: QAction = ...
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

        self.file_path_label = QLabel(self)
        self.file_path_linedit = QLineEdit(self)
        self.open_file_dialog_action = QAction()
        self.open_file_dialog_action.setIcon(get_icon(IMPORT_EXPORT_SELECT_FILE_ICON))
        self.file_path_linedit.addAction(self.open_file_dialog_action,
                                         QLineEdit.ActionPosition.TrailingPosition)
        self.form_layout.addRow(self.file_path_label, self.file_path_linedit)

        # 允许子类添加组件
        self.setup_child_content()

    def setup_child_content(self): ...

    def get_blank_right_buttons(self) -> tuple:
        self.start_process_button = QPushButton(self)
        return self.start_process_button,

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.file_path_linedit.textChanged.connect(self.file_path_change)
        self.open_file_dialog_action.triggered.connect(self.choose_file)
        self.start_process_button.clicked.connect(self.process_data)

    def file_path_change(self, file_path):
        # 操作按钮是否禁用应该根据是否存在文件路径决定
        self.start_process_button.setDisabled(not bool(file_path))

    def choose_file(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_FILE_TEXT, '/')
        if file_url[0]:
            self.file_path_linedit.setText(file_url[0])

    def process_data(self):
        self.process_data_executor = self.get_process_data_executor()
        self.process_data_executor.start()

    def get_process_data_executor(self) -> LoadingMaskThreadExecutor: ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 操作按钮开始应该是禁用的
        self.start_process_button.setDisabled(True)

    # ------------------------------ 后置处理 end ------------------------------ #
