# -*- coding: utf-8 -*-

from src.constant.generator_dialog_constant import PREVIEW_TREE_FOLDER_ICON, PREVIEW_TREE_FILE_ICON
from src.constant.icon_enum import get_icon
from src.view.tree.tree_widget.tree_function import make_display_tree_item
from src.view.tree.tree_widget.tree_widget_abc import DisplayTreeWidget

_author_ = 'luwt'
_date_ = '2023/5/5 12:26'


class PreviewGenerateFileTreeWidget(DisplayTreeWidget):

    def __init__(self, parent):
        # 存储item，可以更快定位item，k：path，v：item
        self.file_path_item_dict = dict()
        self.folder_icon = get_icon(PREVIEW_TREE_FOLDER_ICON)
        self.file_icon = get_icon(PREVIEW_TREE_FILE_ICON)
        super().__init__(parent)

    def make_tree_item(self, file_name, file_path):
        # 首先获取父节点，创建子节点
        parent_dir_item = self.get_file_path_item(file_path)
        return make_display_tree_item(parent_dir_item, file_name, self.file_icon)

    def get_file_path_item(self, file_path):
        file_path_item = self.file_path_item_dict.get(file_path)
        # 如果不存在，创建
        if not file_path_item:
            # 创建父节点
            file_path_item = make_display_tree_item(self, file_path, self.folder_icon)
            self.addTopLevelItem(file_path_item)
            # 保存到缓存中
            self.file_path_item_dict[file_path] = file_path_item
        return file_path_item
