# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.service.async_func.async_struct_task import AddFolderExecutor, EditFolderExecutor
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.view.dialog.name_check_dialog import NameCheckDialog

_author_ = 'luwt'
_date_ = '2022/11/22 8:06'


class FolderDialog(NameCheckDialog):
    save_folder_signal = pyqtSignal(OpenedTreeItem)
    edit_folder_signal = pyqtSignal(str)

    def __init__(self, screen_rect, dialog_title, folder_name_list,
                 opened_folder_item, parent_folder_item):
        self.parent_folder_item: OpenedTreeItem = parent_folder_item

        self.add_folder_executor: AddFolderExecutor = ...
        self.edit_folder_executor: EditFolderExecutor = ...

        # 框架布局，分四部分，第一部分：标题部分，第二部分：文件夹名称表单，第三部分：按钮部分
        super().__init__(screen_rect, dialog_title, folder_name_list, opened_folder_item, read_storage=False)

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.3, self.parent_screen_rect.height() * 0.3)

    def get_old_name(self) -> str:
        return self.dialog_data.item_name

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available

    def save_func(self):
        new_folder_name = self.name_input.displayText()
        # 存在id，说明是编辑
        if self.dialog_data.id:
            if self.dialog_data.item_name != new_folder_name:
                self.dialog_data.item_name = new_folder_name
                self.edit_folder_executor = EditFolderExecutor(self.dialog_data, self,
                                                               self, self.edit_post_process)
                self.edit_folder_executor.start()
            else:
                # 没有更改任何信息
                self.dialog_data_no_change(self.dialog_title)
        else:
            # 新增操作
            self.add_folder_executor = AddFolderExecutor(new_folder_name, self.parent_folder_item.id,
                                                         self.parent_folder_item.level + 1, self, self,
                                                         self.save_post_process)
            self.add_folder_executor.start()

    def save_post_process(self, opened_item_record):
        self.save_folder_signal.emit(opened_item_record)
        self.close()

    def edit_post_process(self):
        self.edit_folder_signal.emit(self.dialog_data.item_name)
        self.close()
