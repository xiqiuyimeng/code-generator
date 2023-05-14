# -*- coding: utf-8 -*-
from src.constant.export_import_constant import SKIP_ILLEGAL_BTN_TEXT, PROCESS_ILLEGAL_BTN_TEXT, \
    MULTI_ILLEGAL_SELECTED_TITLE, MULTI_ILLEGAL_SELECTED_PROMPT
from src.view.box.message_box import pop_msg
from src.view.frame.import_error_data_process.import_error_data_process_dialog_frame_abc import \
    ImportErrorDataProcessDialogFrameABC
from src.view.list_widget.list_item_func import get_import_error_data

_author_ = 'luwt'
_date_ = '2023/5/12 17:35'


class ImportIllegalDataProcessDialogFrame(ImportErrorDataProcessDialogFrameABC):

    def __init__(self, error_data_rows, import_success_callback, get_row_data_dialog, *args):
        self.get_row_data_dialog = get_row_data_dialog
        self.process_illegal_data_dialog = ...
        super().__init__(error_data_rows, import_success_callback, *args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_label_text(self):
        super().setup_other_label_text()
        self.skip_button.setText(SKIP_ILLEGAL_BTN_TEXT)
        self.process_button.setText(PROCESS_ILLEGAL_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        super().connect_other_signal()
        self.list_widget.doubleClicked.connect(self.list_widget_double_clicked_slot)

    def list_widget_double_clicked_slot(self):
        self.open_row_detail_dialog(get_import_error_data(self.list_widget.currentItem()))

    def do_process_data(self, selected_data_list):
        # 检查选中项个数，如果大于1个，则提示，只处理第一个
        if len(selected_data_list) > 1:
            pop_msg(MULTI_ILLEGAL_SELECTED_TITLE, MULTI_ILLEGAL_SELECTED_PROMPT, self)
        first_row_data = selected_data_list[0]
        self.open_row_detail_dialog(first_row_data)

    def open_row_detail_dialog(self, row_data):
        self.process_illegal_data_dialog = self.get_row_detail_dialog(row_data)
        self.process_illegal_data_dialog.override_signal.connect(self.override_callback)
        self.process_illegal_data_dialog.save_signal.connect(self.save_callback)
        self.process_illegal_data_dialog.exec()
        self.allow_close()

    def get_row_detail_dialog(self, row_data): ...

    def override_callback(self, add_data_list, del_data_list):
        # 应该只有一个值，取第一个
        data = add_data_list[0]
        self.list_widget.remove_item_by_name(data)
        self.import_success_callback(add_data_list, del_data_list)

    def save_callback(self, data):
        self.list_widget.remove_item_by_name(data)
        self.import_success_callback((data, ))

    def close(self) -> bool:
        self.parent_dialog.close()
        return super().close()

    # ------------------------------ 信号槽处理 end ------------------------------ #
