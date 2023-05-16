# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.import_dialog_frame import ImportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ImportDialog(CustomDialogABC):

    def __init__(self, import_executor_class, duplicate_dialog_title, override_executor_class,
                 override_dialog_title, illegal_dialog_title, import_success_callback,
                 get_row_data_dialog, *args):
        self.import_executor_class = import_executor_class
        self.duplicate_dialog_title = duplicate_dialog_title
        self.override_executor_class = override_executor_class
        self.override_dialog_title = override_dialog_title
        self.illegal_dialog_title = illegal_dialog_title
        self.import_success_callback = import_success_callback
        self.get_row_data_dialog = get_row_data_dialog
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)

    def get_frame(self) -> ImportDialogFrame:
        return ImportDialogFrame(self.import_executor_class, self.duplicate_dialog_title,
                                 self.override_executor_class, self.override_dialog_title,
                                 self.illegal_dialog_title, self.import_success_callback,
                                 self.get_row_data_dialog, self, self.dialog_title)
