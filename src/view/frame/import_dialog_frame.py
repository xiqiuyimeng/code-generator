# -*- coding: utf-8 -*-
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from PyQt5.QtWidgets import QFileDialog

from src.constant.export_import_constant import IMPORT_FILE_PROMPT, IMPORT_FILE_LABEL_TEXT, \
    START_IMPORT_BTN_TEXT, CHOOSE_IMPORT_FILE_TEXT
from src.service.async_func.async_import_export_task import ImportDataExecutor
from src.view.dialog.import_error_data_process_dialog import ImportErrorDataProcessDialog
from src.view.frame.import_export_dialog_frame_abc import ImportExportDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/5/9 17:47'


class ImportDialogFrame(ImportExportDialogFrameABC):
    
    def __init__(self, *args, import_success_callback=None, get_row_data_dialog=None):
        self.import_success_callback = import_success_callback
        self.get_row_data_dialog = get_row_data_dialog
        self.import_error_data_process_dialog: ImportErrorDataProcessDialog = ...
        super().__init__(*args)
        # 接收拖拽事件
        self.setAcceptDrops(True)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_label_text(self):
        self.blank_label.setText(IMPORT_FILE_PROMPT)
        self.file_path_label.setText(IMPORT_FILE_LABEL_TEXT)
        self.start_process_button.setText(START_IMPORT_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def choose_file(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_IMPORT_FILE_TEXT, '')
        if file_url[0]:
            self.file_path_linedit.setText(file_url[0])

    def get_process_data_executor(self) -> ImportDataExecutor:
        return self.get_process_import_data_executor(self.file_path_linedit.text(),
                                                     self, self, self.dialog_title,
                                                     success_callback=self.import_success_callback,
                                                     process_error_data_func=self.process_import_error_data)

    def get_process_import_data_executor(self, *args, **kwargs) -> ImportDataExecutor: ...

    def process_import_error_data(self, *args):
        # 处理异常数据，打开异常数据处理对话框
        self.import_error_data_process_dialog = self.get_process_error_data_dialog(*args)
        self.import_error_data_process_dialog.exec()

    def get_process_error_data_dialog(self, *args) -> ImportErrorDataProcessDialog: ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 操作按钮开始应该是禁用的
        self.start_process_button.setDisabled(True)

    # ------------------------------ 后置处理 end ------------------------------ #

    def dragEnterEvent(self, event: QDragEnterEvent):
        # 有拖拽文件时，设置接受，本地文件是以url类型描述的，
        # 调用acceptProposedAction来设置对应的事件发生flag，
        # 只有设置了这个flag，后面的drop事件才会发生
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                # 只处理一个导入文件
                file_path = urls[0].toLocalFile()
                self.file_path_linedit.setText(file_path)
