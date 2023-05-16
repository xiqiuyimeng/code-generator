# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.export_import_constant import SKIP_DUPLICATE_BTN_TEXT, PROCESS_DUPLICATE_BTN_TEXT
from src.service.async_func.async_import_export_task import OverrideDataExecutor
from src.view.frame.import_error_data_process.import_error_data_process_dialog_frame_abc import \
    ImportErrorDataProcessDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/5/12 17:26'


class ImportDuplicateDataProcessDialogFrame(ImportErrorDataProcessDialogFrameABC):
    illegal_rows_signal = pyqtSignal(list)

    def __init__(self, duplicate_rows, duplicate_illegal_rows,
                 override_executor_class, override_title, *args):
        # 这个集合内的数据，不可以直接覆盖，需要转到不合法数据页处理
        self.duplicate_illegal_rows = duplicate_illegal_rows
        self.override_executor_class = override_executor_class
        self.override_title = override_title
        self.override_executor: OverrideDataExecutor = ...
        self.illegal_rows = list()
        super().__init__(duplicate_rows, *args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        super().setup_content_ui()
        self.list_widget.fill_list_widget(self.duplicate_illegal_rows)

    def setup_other_label_text(self):
        super().setup_other_label_text()
        self.skip_button.setText(SKIP_DUPLICATE_BTN_TEXT)
        self.process_button.setText(PROCESS_DUPLICATE_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def do_process_data(self, selected_data_list):
        # 判断数据是否不合法，合法数据可以直接覆盖，不合法数据收集起来
        duplicate_legal_rows = list()
        for data in selected_data_list:
            if data in self.duplicate_illegal_rows:
                self.illegal_rows.append(data)
                self.list_widget.remove_item_by_name(data)
            else:
                duplicate_legal_rows.append(data)
        # 开线程处理
        if duplicate_legal_rows:
            self.override_executor = self.override_executor_class(duplicate_legal_rows, self, self,
                                                                  self.override_title,
                                                                  success_callback=self.override_success_callback)
            self.override_executor.start()
        else:
            self.allow_close()

    def override_success_callback(self, add_data_list, del_data_list):
        self.list_widget.remove_selected_items()
        self.import_success_callback(add_data_list, del_data_list)
        self.allow_close()

    def close(self) -> bool:
        self.illegal_rows_signal.emit(self.illegal_rows)
        return super().close()

    # ------------------------------ 信号槽处理 end ------------------------------ #
