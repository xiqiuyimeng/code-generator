# -*- coding: utf-8 -*-
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QLabel, QFileDialog

from src.constant.export_import_constant import EXPORT_SELECTED_DATA_LABEL_TEXT, EXPORT_OUTPUT_PATH_LABEL_TEXT, \
    START_EXPORT_BTN_TEXT, EXPORT_SELECTED_DATA_DESC_TEXT, CHOOSE_EXPORT_DIR_TEXT
from src.service.async_func.async_import_export_task import ExportDataExecutor
from src.view.frame.import_export_dialog_frame_abc import ImportExportDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/5/9 17:47'


class ExportDialogFrame(ImportExportDialogFrameABC):
    """导出对话框框架"""

    def __init__(self, row_ids, default_export_file_name, export_executor_class, *args):
        # 选中需要导出的数据id
        self.row_ids = row_ids
        # 默认导出文件名
        self.default_export_file_name = default_export_file_name
        # 导出线程执行器类
        self.export_executor_class = export_executor_class
        self.selected_data_label: QLabel = ...
        self.selected_data_desc_label: QLabel = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_child_content(self):
        self.selected_data_label = QLabel(self)
        self.selected_data_desc_label = QLabel(self)
        self.form_layout.insertRow(0, self.selected_data_label, self.selected_data_desc_label)

    def setup_other_label_text(self):
        self.selected_data_label.setText(EXPORT_SELECTED_DATA_LABEL_TEXT)
        self.selected_data_desc_label.setText(EXPORT_SELECTED_DATA_DESC_TEXT.format(len(self.row_ids)))
        self.file_path_label.setText(EXPORT_OUTPUT_PATH_LABEL_TEXT)
        self.start_process_button.setText(START_EXPORT_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #
    def choose_file(self):
        dir_url = QFileDialog.getSaveFileName(self, CHOOSE_EXPORT_DIR_TEXT, self.file_path_linedit.text())
        if dir_url[0]:
            self.file_path_linedit.setText(dir_url[0])

    def get_process_data_executor(self) -> ExportDataExecutor:
        return self.export_executor_class(self.row_ids, self.file_path_linedit.text(),
                                          self, self, self.dialog_title)

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 给一个默认导出文件地址，当前路径 / 导出文件名
        self.file_path_linedit.setText(f'{QDir().absolutePath()}/{self.default_export_file_name}')

    # ------------------------------ 后置处理 end ------------------------------ #
