# -*- coding: utf-8 -*-
from src.constant.generator_dialog_constant import PREVIEW_GENERATE_FILE_TITLE
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.generator.preview_file_dialog_frame import PreviewFileDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/5 11:17'


class PreviewFileDialog(CustomDialogABC):
    """预览生成，预览文件对话框"""

    def __init__(self, preview_data_dict: dict):
        self.preview_data_dict = preview_data_dict
        self.frame: PreviewFileDialogFrame = ...
        super().__init__(PREVIEW_GENERATE_FILE_TITLE)

    def resize_dialog(self):
        self.resize(self.window_geometry.width(), self.window_geometry.height())
        # 窗口位置保持和主窗口一致
        self.setGeometry(self.window_geometry)

    def get_frame(self) -> PreviewFileDialogFrame:
        return PreviewFileDialogFrame(self.preview_data_dict, self, self.dialog_title)
