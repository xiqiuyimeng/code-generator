# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.import_error_data_process.import_duplicate_data_process_dialog_frame import \
    ImportDuplicateDataProcessDialogFrame
from src.view.frame.import_error_data_process.import_error_data_process_dialog_frame_abc import \
    ImportErrorDataProcessDialogFrameABC
from src.view.frame.import_error_data_process.import_illegal_data_process_dialog_frame import \
    ImportIllegalDataProcessDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/12 11:10'


class ImportErrorDataProcessDialog(CustomDialogABC):

    def __init__(self, duplicate_rows, illegal_rows, duplicate_illegal_rows,
                 duplicate_dialog_title, override_executor_class, override_dialog_title,
                 import_success_callback, get_row_data_dialog, illegal_dialog_title, *args):
        self.duplicate_rows = duplicate_rows
        self.illegal_rows = illegal_rows
        self.duplicate_illegal_rows = duplicate_illegal_rows
        self.duplicate_dialog_title = duplicate_dialog_title
        self.override_executor_class = override_executor_class
        self.override_dialog_title = override_dialog_title
        self.import_success_callback = import_success_callback
        self.get_row_data_dialog = get_row_data_dialog
        self.illegal_dialog_title = illegal_dialog_title
        self.frame = ImportErrorDataProcessDialogFrameABC
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.7)

    def get_frame(self) -> ImportErrorDataProcessDialogFrameABC:
        # 判断重复数据是否存在，如果重复数据存在，则加载处理重复数据页面
        # 判断不合法数据是否存在，如果不合法数据存在，则加载处理不合法数据页面
        if self.duplicate_rows or self.duplicate_illegal_rows:
            duplicate_data_process_frame = ImportDuplicateDataProcessDialogFrame(self.duplicate_rows,
                                                                                 self.duplicate_illegal_rows,
                                                                                 self.override_executor_class,
                                                                                 self.override_dialog_title,
                                                                                 self.import_success_callback,
                                                                                 self, self.duplicate_dialog_title)
            # 在页面关闭时发送
            duplicate_data_process_frame.illegal_rows_signal.connect(self.switch_illegal_data_process_frame)
            return duplicate_data_process_frame
        else:
            return self.get_illegal_data_process_frame()

    def switch_illegal_data_process_frame(self, illegal_rows):
        if illegal_rows:
            self.illegal_rows.extend(illegal_rows)
        if self.illegal_rows:
            illegal_data_process_frame = self.get_illegal_data_process_frame()
            self.dialog_layout.removeWidget(self.frame)
            self.dialog_layout.addWidget(illegal_data_process_frame)
        else:
            self.close()

    def get_illegal_data_process_frame(self) -> ImportIllegalDataProcessDialogFrame:
        return ImportIllegalDataProcessDialogFrame(self.get_row_data_dialog, self.illegal_rows,
                                                   self.import_success_callback, self,
                                                   self.illegal_dialog_title)
