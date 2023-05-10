# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.import_dialog_frame import ImportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ImportDialog(CustomDialogABC):

    def __init__(self, get_executor_func, *args):
        self.get_executor_func = get_executor_func
        self.frame: ImportDialogFrame = ...
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)

    def get_frame(self) -> ImportDialogFrame:
        return ImportDialogFrame(self.get_executor_func, self, self.dialog_title)
