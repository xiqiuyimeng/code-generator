# -*- coding: utf-8 -*-
from src.constant.generator_dialog_constant import SAVE_PREVIEW_FILE_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.save_file_dialog_frame import SaveFileDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/6 14:22'


class SaveFileDialog(CustomDialogABC):

    def __init__(self, save_file_dict):
        self.save_file_dict = save_file_dict
        self.frame: SaveFileDialogFrame = ...
        super().__init__(SAVE_PREVIEW_FILE_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() >> 1, self.window_geometry.height() >> 2)

    def get_frame(self) -> SaveFileDialogFrame:
        return SaveFileDialogFrame(self.save_file_dict, self, self.dialog_title)
