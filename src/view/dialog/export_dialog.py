# -*- coding: utf-8 -*-
from src.view.dialog.custom_dialog_abc import CustomDialogABC
from src.view.frame.export_dialog_frame import ExportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/9 17:45'


class ExportDialog(CustomDialogABC):

    def __init__(self, row_ids, default_export_file_name, export_executor_class, *args):
        # 选中需要导出的数据id
        self.row_ids = row_ids
        # 默认导出文件名
        self.default_export_file_name = default_export_file_name
        # 导出线程执行器类
        self.export_executor_class = export_executor_class
        self.frame: ExportDialogFrame = ...
        super().__init__(*args)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.4)

    def get_frame(self) -> ExportDialogFrame:
        return ExportDialogFrame(self.row_ids, self.default_export_file_name,
                                 self.export_executor_class, self, self.dialog_title)
