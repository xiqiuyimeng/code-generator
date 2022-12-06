# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QAction, QFileDialog, QPushButton

from constant.constant import STRUCTURE_NAME_TEXT, STRUCTURE_FILE_URL_TEXT, STRUCTURE_CONTENT_TEXT, \
    CHOOSE_STRUCT_FILE_TEXT, PRETTY_STRUCT_TEXT
from constant.icon_enum import get_icon
from service.async_func.async_struct_task import ReadFileExecutor, AddStructExecutor, EditStructExecutor, \
    QueryStructExecutor
from service.async_func.struct_executor import *
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from service.system_storage.struct_sqlite import StructInfo
from service.system_storage.struct_type import StructType
from view.custom_widget.scrollable_widget import ScrollableTextEdit
from view.dialog.datasource.abstract_ds_dialog import AbstractDsInfoDialog

_author_ = 'luwt'
_date_ = '2022/11/11 16:46'


class AbstractStructDialog(AbstractDsInfoDialog):
    struct_saved = pyqtSignal(OpenedTreeItem)
    struct_changed = pyqtSignal(str)

    def __init__(self, dialog_title, screen_rect, struct_name_list, opened_struct_id,
                 tree_widget, parent_folder_item):
        self.tree_widget = tree_widget
        # 父节点 opened item
        self.parent_folder_item: OpenedTreeItem = parent_folder_item
        # 初始化一个新的结构体对象
        self.new_dialog_data: StructInfo = ...
        self.struct_type: StructType = self.get_struct_type()
        self.dialog_data: StructInfo = ...

        self.struct_file_url_label: QLabel = ...
        self.struct_file_url_linedit: QLineEdit = ...
        self.struct_file_action: QAction = ...
        self.struct_text_label: QLabel = ...
        self.struct_text_input: ScrollableTextEdit = ...
        self.pretty_button: QPushButton = ...

        self.read_file_executor: ReadFileExecutor = ...
        self.pretty_executor: PrettyStructExecutor = ...
        self.add_struct_executor: AddStructExecutor = ...
        self.edit_struct_executor: EditStructExecutor = ...

        # 如果是编辑，需要读取数据库中存储的实际的结构体信息，用来回显

        super().__init__(dialog_title.format(self.struct_type.display_name), screen_rect,
                         struct_name_list, opened_struct_id)

        # 调整布局比例
        self.frame_layout.setStretch(0, 2)
        self.frame_layout.setStretch(1, 1)
        self.frame_layout.setStretch(2, 4)
        self.frame_layout.setStretch(3, 1)

    def get_new_dialog_data(self):
        return StructInfo()

    def resize_dialog(self):
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

    def setup_other_button(self):
        # 按钮部分
        self.pretty_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.pretty_button, 0, 0, 1, 1)

    def setup_other_label_text(self):
        self.name_label.setText(STRUCTURE_NAME_TEXT.format(self.struct_type.display_name))
        # 结构体信息
        self.struct_file_url_label.setText(STRUCTURE_FILE_URL_TEXT.format(self.struct_type.display_name))
        self.struct_text_label.setText(STRUCTURE_CONTENT_TEXT.format(self.struct_type.display_name))
        self.pretty_button.setText(PRETTY_STRUCT_TEXT.format(self.struct_type.display_name))

    def get_read_storage_executor(self, callback):
        return QueryStructExecutor(self.dialog_data, callback, self, self)

    def setup_echo_other_data(self):
        # 数据回显
        self.struct_file_url_linedit.setText(self.dialog_data.file_url)
        self.struct_text_input.setPlainText(self.dialog_data.content)

    def button_available(self) -> bool:
        return all((self.new_dialog_data.struct_name, self.new_dialog_data.content)) and self.name_available

    def collect_input(self):
        # 根据参数构建结构体信息对象
        self.new_dialog_data = StructInfo()
        self.new_dialog_data.struct_type = self.struct_type.display_name
        self.new_dialog_data.struct_name = self.name_input.text()
        self.new_dialog_data.content = self.struct_text_input.toPlainText()
        file_url = self.struct_file_url_linedit.text()
        self.new_dialog_data.file_url = file_url

    def init_other_button_status(self):
        self.pretty_button.setDisabled(True)

    def set_other_button_available(self):
        self.pretty_button.setDisabled(False)

    def connect_child_signal(self):
        self.struct_file_action.triggered.connect(self.choose_file)
        self.struct_file_url_linedit.textEdited.connect(self.check_input)
        self.struct_text_input.textChanged.connect(self.check_input)
        self.pretty_button.clicked.connect(self.pretty_func)

    def choose_file(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_STRUCT_FILE_TEXT, '/')
        if file_url[0]:
            self.struct_file_url_linedit.setText(file_url[0])
            # 异步读取文件内容，回显到内容区域
            self.read_file_executor = ReadFileExecutor(file_url[0], self.struct_type.display_name,
                                                       self, self, self.append_plain_text)
            self.read_file_executor.start()

    def append_plain_text(self, index, text):
        if index == 0:
            self.struct_text_input.clear()
        self.struct_text_input.appendPlainText(text)

    def pretty_func(self):
        self.pretty_executor = globals()[self.struct_type.beautifier_executor](
            self.new_dialog_data.content, self.struct_type.display_name,
            self, self, self.struct_text_input.setPlainText
        )
        self.pretty_executor.start()

    def get_old_name(self) -> str:
        return self.dialog_data.struct_name

    def save_func(self):
        # 存在id，说明是编辑
        if self.dialog_data:
            if self.new_dialog_data != self.dialog_data:
                self.new_dialog_data.id = self.dialog_data.id
                self.new_dialog_data.opened_item_id = self.dialog_data.opened_item_id
                self.name_changed = self.new_dialog_data.struct_name != self.dialog_data.struct_name
                self.edit_struct_executor = EditStructExecutor(self.new_dialog_data, self, self,
                                                               self.edit_post_process)
                self.edit_struct_executor.start()
            else:
                # 没有更改任何信息
                self.ds_info_no_change()
        else:
            # 新增操作
            self.add_struct_executor = AddStructExecutor(self.new_dialog_data, self.parent_folder_item,
                                                         self, self, self.save_post_process)
            self.add_struct_executor.start()

    def save_post_process(self, opened_item_record):
        self.struct_saved.emit(opened_item_record)
        self.close()

    def edit_post_process(self):
        self.struct_changed.emit(self.new_dialog_data.struct_name)
        self.close()
