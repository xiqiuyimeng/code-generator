# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.ds_dialog_constant import EDIT_FOLDER_BOX_TITLE, ADD_FOLDER_BOX_TITLE
from src.service.async_func.async_struct_task import AddFolderExecutor, EditFolderExecutor
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 13:48'


class FolderDialogFrame(NameCheckDialogFrame):
    """文件夹对话框框架"""
    save_signal = pyqtSignal(OpenedTreeItem)
    edit_signal = pyqtSignal(str)

    def __init__(self, parent_dialog, dialog_title, folder_name_list,
                 opened_folder_item, parent_folder_item):
        self.parent_folder_item: OpenedTreeItem = parent_folder_item

        self.add_folder_executor: AddFolderExecutor = ...
        self.edit_folder_executor: EditFolderExecutor = ...

        # 框架布局，分四部分，第一部分：标题部分，第二部分：文件夹名称表单，第三部分：按钮部分
        super().__init__(parent_dialog, dialog_title, folder_name_list, opened_folder_item, read_storage=False)

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def save_func(self):
        new_folder_name = self.name_input.displayText()
        # 存在id，说明是编辑
        if self.dialog_data.id:
            self.dialog_data.item_name = new_folder_name
            self.edit_folder_executor = EditFolderExecutor(self.dialog_data, self, self,
                                                           EDIT_FOLDER_BOX_TITLE, self.edit_post_process)
            self.edit_folder_executor.start()
        else:
            # 新增操作
            self.add_folder_executor = AddFolderExecutor(new_folder_name, self.parent_folder_item.id,
                                                         self.parent_folder_item.level + 1, self, self,
                                                         ADD_FOLDER_BOX_TITLE, self.save_post_process)
            self.add_folder_executor.start()

    def save_post_process(self, opened_item_record):
        self.save_signal.emit(opened_item_record)
        self.parent_dialog.close()

    def edit_post_process(self):
        self.edit_signal.emit(self.dialog_data.item_name)
        self.parent_dialog.close()

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available

    def check_data_changed(self) -> bool:
        return self.dialog_data.item_name != self.name_input.displayText()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_old_name(self) -> str:
        return self.dialog_data.item_name

    # ------------------------------ 后置处理 end ------------------------------ #

