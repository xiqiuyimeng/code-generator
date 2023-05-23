# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.dialog.custom_dialog_abc import CustomSaveDialogABC
from src.view.frame.datasource.struct.folder_dialog_frame import FolderDialogFrame
from src.view.frame.datasource.struct.json_struct_dialog_frame import JsonStructDialogFrame
from src.view.frame.datasource.struct.struct_dialog_frame_abc import StructDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/3 16:46'


class FolderDialog(CustomSaveDialogABC):
    """文件夹对话框"""
    save_signal = pyqtSignal(OpenedTreeItem)
    edit_signal = pyqtSignal(str)

    def __init__(self, dialog_title, exists_folder_name_tuple, opened_folder_item, parent_folder_item):
        self.exists_folder_name_tuple = exists_folder_name_tuple
        self.opened_folder_item = opened_folder_item
        self.parent_folder_item = parent_folder_item
        self.frame: FolderDialogFrame = ...
        super().__init__(dialog_title)

    def resize_dialog(self):
        self.resize(self.window_geometry.width() * 0.3, self.window_geometry.height() * 0.3)

    def get_frame(self) -> FolderDialogFrame:
        return FolderDialogFrame(self, self.dialog_title, self.exists_folder_name_tuple,
                                 self.opened_folder_item, self.parent_folder_item)


class StructDialogABC(CustomSaveDialogABC):
    """结构体对话框抽象类"""
    save_signal = pyqtSignal(OpenedTreeItem)
    edit_signal = pyqtSignal(str)

    def __init__(self, dialog_title, exists_struct_name_tuple, opened_struct_id,
                 tree_widget, parent_folder_item):
        self.exists_struct_name_tuple = exists_struct_name_tuple
        self.opened_struct_id = opened_struct_id
        self.tree_widget = tree_widget
        self.parent_folder_item = parent_folder_item
        self.frame: StructDialogFrameABC = ...
        super().__init__(dialog_title)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.window_geometry.width() * 0.6, self.window_geometry.height() * 0.8)


class JsonStructDialog(StructDialogABC):
    """json结构体对话框"""

    def get_frame(self) -> JsonStructDialogFrame:
        return JsonStructDialogFrame(self, self.dialog_title, self.exists_struct_name_tuple,
                                     self.opened_struct_id, self.tree_widget, self.parent_folder_item)
