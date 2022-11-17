# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLabel, QFormLayout, QLineEdit, QAction, QFileDialog

from constant.constant import STRUCTURE_NAME_TEXT, STRUCTURE_FILE_URL_TEXT, STRUCTURE_CONTENT_TEXT, \
    CHOOSE_STRUCT_FILE_TEXT
from constant.icon_enum import get_icon
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from service.system_storage.struct_content_sqlite import StructContent, StorageTypeEnum
from service.system_storage.struct_sqlite import StructInfo
from service.system_storage.struct_type import StructType
from view.custom_widget.scrollable_widget import ScrollableTextEdit
from view.dialog.datasource.abstract_ds_dialog import AbstractDsInfoDialog
from view.dialog.datasource.structure.choose_folder_dialog import ChooseFolderDialog

_author_ = 'luwt'
_date_ = '2022/11/11 16:46'


class AbstractStructDialog(AbstractDsInfoDialog):

    struct_saved = pyqtSignal(StructInfo, OpenedTreeItem)
    # 第一个元素为修改后的结构体对象，第二个元素为名称是否变化
    struct_changed = pyqtSignal(StructInfo, bool)

    def __init__(self, struct_info: StructInfo, dialog_title, screen_rect, struct_name_id_dict):
        # 初始化一个新的结构体对象
        self.new_struct: StructInfo = StructInfo()
        self.struct_type: StructType = self.get_struct_type()
        self.struct_info: StructInfo = ...
        self.struct_content: StructContent = ...

        self.struct_file_url_label: QLabel = ...
        self.struct_file_url_linedit: QLineEdit = ...
        self.struct_file_action: QAction = ...
        self.struct_text_label: QLabel = ...
        self.struct_text_input: ScrollableTextEdit = ...

        self.choose_folder_dialog: ChooseFolderDialog = ...

        # 如果是编辑，需要读取数据库中存储的实际的结构体信息，用来回显

        super().__init__(struct_info, dialog_title, screen_rect, struct_name_id_dict)

        # 调整布局比例
        self.frame_layout.setStretch(0, 2)
        self.frame_layout.setStretch(1, 1)
        self.frame_layout.setStretch(2, 4)
        self.frame_layout.setStretch(3, 1)

    def resize_window(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.6, self.parent_screen_rect.height() * 0.8)

    def get_struct_type(self) -> StructType: ...

    def setup_ds_content_info_ui(self):
        # 结构体信息布局
        self.ds_info_layout = QFormLayout()
        # 结构体文件地址
        self.struct_file_url_label = QLabel(self.frame)
        self.struct_file_url_linedit = QLineEdit(self.frame)
        self.struct_file_action = QAction()
        self.struct_file_action.setIcon(get_icon(self.struct_type.display_name))
        self.struct_file_url_linedit.addAction(self.struct_file_action, QLineEdit.ActionPosition.TrailingPosition)
        self.ds_info_layout.addRow(self.struct_file_url_label, self.struct_file_url_linedit)

        # 结构体内容文本框
        self.struct_text_label = QLabel(self.frame)
        self.struct_text_input = ScrollableTextEdit(self.frame)
        self.ds_info_layout.addRow(self.struct_text_label, self.struct_text_input)

    def setup_other_button_ui(self):
        # 按钮部分
        self.button_layout = QGridLayout()
        self.button_blank = QLabel(self.frame)
        self.button_layout.addWidget(self.button_blank, 0, 0, 1, 2)

    def setup_content_label_text(self):
        self.title.setText(self.dialog_title.format(self.struct_type.display_name))
        self.ds_name_label.setText(STRUCTURE_NAME_TEXT.format(self.struct_type.display_name))
        # 结构体信息
        self.struct_file_url_label.setText(STRUCTURE_FILE_URL_TEXT.format(self.struct_type.display_name))
        self.struct_text_label.setText(STRUCTURE_CONTENT_TEXT.format(self.struct_type.display_name))

    def setup_ds_info_value_show(self):
        # 数据回显
        self.ds_name_value.setText(self.ds_info.struct_name)
        if self.struct_content.storage_type:
            self.struct_file_url_linedit.setText(self.struct_content.file_url)
        self.struct_text_input.setPlainText(self.struct_content.content)

    def button_available(self) -> bool:
        return all((self.struct_info.struct_name, self.struct_content.content))

    def collect_input(self):
        self.new_struct.struct_name = self.ds_name_value.text()
        self.collect_structure_info_input()

    def collect_structure_info_input(self):
        # 根据参数构建结构体信息对象
        self.struct_info = StructInfo()
        self.struct_info.struct_type = self.struct_type.display_name
        self.struct_info.struct_name = self.ds_name_value.text()
        self.struct_content = StructContent()
        self.struct_content.content = self.struct_text_input.toPlainText()
        file_url = self.struct_file_url_linedit.text()
        self.struct_content.file_url = file_url
        self.struct_content.storage_type = StorageTypeEnum.file.value \
            if file_url else StorageTypeEnum.text.value

    def connect_ds_other_signal(self):
        self.struct_file_action.triggered.connect(self.choose_file)
        self.struct_file_url_linedit.textEdited.connect(self.check_input)
        self.struct_text_input.textChanged.connect(self.check_input)

    def choose_file(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_STRUCT_FILE_TEXT, '/')
        if file_url[0]:
            self.struct_file_url_linedit.setText(file_url[0])

    def save_ds_info(self):
        # 打开保存文件夹框，选择父级文件夹
        self.choose_folder_dialog = ChooseFolderDialog(self.parent_screen_rect)
        self.choose_folder_dialog.exec()
    #     self.new_connection.construct_conn_info()
    #     # 存在id，说明是编辑
    #     if self.ds_info.id:
    #         if self.new_connection != self.ds_info:
    #             self.new_connection.id = self.ds_info.id
    #             self.name_changed = self.new_connection.conn_name != self.ds_info.conn_name
    #             self.edit_conn_executor = EditConnExecutor(self.new_connection, self, self,
    #                                                        self.edit_post_process, self.name_changed)
    #             self.edit_conn_executor.start()
    #         else:
    #             # 没有更改任何信息
    #             self.ds_info_no_change()
    #     else:
    #         # 新增操作
    #         self.add_conn_executor = AddConnExecutor(self.new_connection, self, self, self.save_post_process)
    #         self.add_conn_executor.start()
    #
    # def save_post_process(self, conn_id, opened_item_record):
    #     self.new_connection.id = conn_id
    #     self.conn_saved.emit(self.new_connection, opened_item_record)
    #     self.close()
    #
    # def edit_post_process(self):
    #     self.conn_changed.emit(self.new_connection, self.name_changed)
    #     self.close()



