# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.export_dialog_frame import ExportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ExportDialog(CustomDialogABC):

    def __init__(self, row_ids, *args):
        self.row_ids = row_ids
        self.frame: ExportDialogFrame = ...
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)
