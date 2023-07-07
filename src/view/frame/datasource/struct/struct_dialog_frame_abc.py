# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QFormLayout, QFileDialog

from src.constant.ds_dialog_constant import STRUCT_NAME_TEXT, STRUCT_FILE_URL_TEXT, STRUCT_CONTENT_TEXT, \
    PRETTY_STRUCT_TEXT, CHOOSE_STRUCT_FILE_TEXT, READ_STRUCT_FILE_BOX_TITLE, PRETTY_STRUCT_BOX_TITLE, \
    EDIT_STRUCT_BOX_TITLE, ADD_STRUCT_BOX_TITLE, QUERY_STRUCT_BOX_TITLE
from src.constant.help.help_constant import STRUCT_DS_HELP
from src.service.async_func.async_struct_task import ReadFileExecutor, PrettyStructExecutor, AddStructExecutor, \
    EditStructExecutor, QueryStructExecutor
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.service.system_storage.struct_sqlite import StructInfo
from src.enum.struct_type_enum import StructType
from src.view.custom_widget.syntax_highlighter.syntax_highlighter_abc import SyntaxHighLighterABC
from src.view.custom_widget.text_editor import TextEditor
from src.view.frame.datasource.ds_dialog_frame_abc import DsDialogFrameABC
from src.view.frame.frame_func import construct_lineedit_file_action

_author_ = 'luwt'
_date_ = '2023/4/3 13:52'


class StructDialogFrameABC(DsDialogFrameABC):
    """结构体对话框框架抽象类"""
    save_signal = pyqtSignal(OpenedTreeItem)
    edit_signal = pyqtSignal(str)

    def __init__(self, parent_dialog, dialog_title, exists_struct_names, opened_struct_id,
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
        self.struct_text_input: TextEditor = ...
        self.struct_text_syntax_highlighter: SyntaxHighLighterABC = ...
        self.pretty_button: QPushButton = ...

        self.read_file_executor: ReadFileExecutor = ...
        self.pretty_executor: PrettyStructExecutor = ...
        self.add_struct_executor: AddStructExecutor = ...
        self.edit_struct_executor: EditStructExecutor = ...

        # 如果是编辑，需要读取数据库中存储的实际的结构体信息，用来回显

        super().__init__(parent_dialog, dialog_title.format(self.struct_type.display_name),
                         exists_struct_names, opened_struct_id, placeholder_blank_width=1)

        # 调整布局比例
        self.frame_layout.setStretch(0, 1)
        self.frame_layout.setStretch(1, 1)
        self.frame_layout.setStretch(2, 4)
        self.frame_layout.setStretch(3, 1)

    def get_struct_type(self) -> StructType:
        ...

    def get_new_dialog_data(self):
        return StructInfo()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_ds_content_info_ui(self):
        # 结构体信息布局
        self.ds_info_layout = QFormLayout()
        # 结构体文件地址
        self.struct_file_url_label, self.struct_file_url_linedit, \
            self.struct_file_action = construct_lineedit_file_action()
        self.ds_info_layout.addRow(self.struct_file_url_label, self.struct_file_url_linedit)

        # 结构体内容文本框
        self.struct_text_label = QLabel(self)
        self.struct_text_label.setObjectName('form_label')
        self.struct_text_input = TextEditor(self)
        # 构建语法高亮器
        self.struct_text_syntax_highlighter = self.get_syntax_highlighter()
        self.struct_text_syntax_highlighter.setDocument(self.struct_text_input.document())
        self.ds_info_layout.addRow(self.struct_text_label, self.struct_text_input)

    def get_syntax_highlighter(self) -> SyntaxHighLighterABC:
        ...

    def get_blank_left_buttons(self) -> tuple:
        # 按钮部分
        self.pretty_button = QPushButton(self)
        self.pretty_button.setObjectName('pretty_button')
        return self.pretty_button,

    def setup_other_label_text(self):
        self.name_label.setText(STRUCT_NAME_TEXT.format(self.struct_type.display_name))
        # 结构体信息
        self.struct_file_url_label.setText(STRUCT_FILE_URL_TEXT.format(self.struct_type.display_name))
        self.struct_text_label.setText(STRUCT_CONTENT_TEXT.format(self.struct_type.display_name))
        self.pretty_button.setText(PRETTY_STRUCT_TEXT.format(self.struct_type.display_name))

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return STRUCT_DS_HELP

    def check_input(self):
        super().check_input()
        # 自定义方法，实现美化按钮是否可用的逻辑
        if self.new_dialog_data.content:
            self.pretty_button.setDisabled(False)
        else:
            self.pretty_button.setDisabled(True)

    def collect_input(self):
        # 根据参数构建结构体信息对象
        self.new_dialog_data = StructInfo()
        self.new_dialog_data.struct_type = self.struct_type.display_name
        self.new_dialog_data.struct_name = self.name_input.text()
        self.new_dialog_data.content = self.struct_text_input.toPlainText()
        file_url = self.struct_file_url_linedit.text()
        self.new_dialog_data.file_url = file_url

    def button_available(self) -> bool:
        return all((self.new_dialog_data.struct_name, self.new_dialog_data.content)) and self.name_available

    def check_data_changed(self) -> bool:
        return self.new_dialog_data != self.dialog_data

    def connect_child_signal(self):
        self.struct_file_action.triggered.connect(self.choose_file)
        self.struct_file_url_linedit.textEdited.connect(self.check_input)
        self.struct_text_input.textChanged.connect(self.check_input)
        self.pretty_button.clicked.connect(self.pretty_func)

    def choose_file(self):
        file_url = QFileDialog.getOpenFileName(self, CHOOSE_STRUCT_FILE_TEXT, '')
        if file_url[0]:
            self.struct_file_url_linedit.setText(file_url[0])
            # 异步读取文件内容，回显到内容区域
            box_title = READ_STRUCT_FILE_BOX_TITLE.format(self.struct_type.display_name)
            self.read_file_executor = ReadFileExecutor(file_url[0], self.struct_type.display_name,
                                                       self.parent_dialog, self.parent_dialog,
                                                       box_title, self.append_plain_text)
            self.read_file_executor.start()

    def append_plain_text(self, index, text):
        if index == 0:
            self.struct_text_input.clear()
        self.struct_text_input.appendPlainText(text)

    def pretty_func(self):
        box_title = PRETTY_STRUCT_BOX_TITLE.format(self.struct_type.display_name)
        self.pretty_executor = PrettyStructExecutor(self.new_dialog_data.content,
                                                    self.struct_type.beautifier_executor,
                                                    self.parent_dialog, self.parent_dialog,
                                                    box_title, self.struct_text_input.setPlainText)
        self.pretty_executor.start()

    def save_func(self):
        # 原数据存在，说明是编辑
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.new_dialog_data.opened_item_id = self.dialog_data.opened_item_id
            self.name_changed = self.new_dialog_data.struct_name != self.dialog_data.struct_name
            title = EDIT_STRUCT_BOX_TITLE.format(self.new_dialog_data.struct_type)
            self.edit_struct_executor = EditStructExecutor(self.new_dialog_data, self.parent_dialog,
                                                           self.parent_dialog, title, self.edit_post_process)
            self.edit_struct_executor.start()
        else:
            # 新增操作
            title = ADD_STRUCT_BOX_TITLE.format(self.new_dialog_data.struct_type)
            self.add_struct_executor = AddStructExecutor(self.new_dialog_data, self.parent_folder_item,
                                                         self.parent_dialog, self.parent_dialog, title,
                                                         self.save_post_process)
            self.add_struct_executor.start()

    def save_post_process(self, opened_item_record):
        self.save_signal.emit(opened_item_record)
        self.parent_dialog.close()

    def edit_post_process(self):
        self.edit_signal.emit(self.new_dialog_data.struct_name)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 清除焦点
        self.dialog_quit_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.save_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pretty_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def get_read_storage_executor(self, callback):
        return QueryStructExecutor(self.dialog_data, self.parent_dialog, self.parent_dialog,
                                   QUERY_STRUCT_BOX_TITLE, callback)

    def get_old_name(self) -> str:
        return self.dialog_data.struct_name

    def setup_echo_other_data(self):
        # 数据回显
        self.struct_file_url_linedit.setText(self.dialog_data.file_url)
        self.struct_text_input.setPlainText(self.dialog_data.content)

    # ------------------------------ 后置处理 end ------------------------------ #
