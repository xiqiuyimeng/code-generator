# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ImportDialog(CustomDialogABC):

    def __init__(self, *args, import_success_callback=None, get_row_data_dialog=None):
        self.import_success_callback = import_success_callback
        self.get_row_data_dialog = get_row_data_dialog
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)
