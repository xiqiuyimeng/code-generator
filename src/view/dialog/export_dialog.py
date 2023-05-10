# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.export_dialog_frame import ExportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ExportDialog(CustomDialogABC):

    def __init__(self, row_ids, get_executor_func, *args):
        self.row_ids = row_ids
        self.get_executor_func = get_executor_func
        self.frame: ExportDialogFrame = ...
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)

    def get_frame(self) -> ExportDialogFrame:
        return ExportDialogFrame(self.row_ids, self.get_executor_func, self, self.dialog_title)
