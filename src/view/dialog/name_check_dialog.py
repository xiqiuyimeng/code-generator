# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel, QFormLayout, QLineEdit, QAction

from constant.constant import NAME_AVAILABLE, NAME_EXISTS, NO_CHANGE_PROMPT
from constant.icon_enum import get_icon
from read_qrc.read_file import read_qss
from service.async_func.async_task_abc import LoadingMaskThreadExecutor
from service.system_storage.sqlite_abc import BasicSqliteDTO
from view.box.message_box import pop_ok
from view.dialog.custom_dialog import CustomDialog

_author_ = 'luwt'
_date_ = '2022/11/22 9:02'


class NameCheckDialog(CustomDialog):

    def __init__(self, screen_rect, dialog_title, name_list, dialog_data=None, read_storage=True):
        # 框架布局，分四部分，第一部分：标题部分，第二部分：名称表单，第三部分：其他内容，第四部分：按钮部分
        # 存储当前名称不允许重复的列表
        self.name_list = name_list
        # 原数据对象，编辑时，回显数据使用
        self.dialog_data = dialog_data
        # 是否读取存储的数据，如果开启，将从数据库异步读取数据，否则将使用 dialog_data 回显数据
        self.read_storage = read_storage
        self.read_storage_executor: LoadingMaskThreadExecutor = ...
        # 新的数据对象，保存编辑使用
        self.new_dialog_data: BasicSqliteDTO = self.get_new_dialog_data()
        self.old_name = ...
        self.name_layout: QFormLayout = ...
        self.name_label: QLabel = ...
        self.name_available: bool = ...
        self.name_changed: bool = ...
        self.name_input: QLineEdit = ...
        self.name_checker: QLabel = ...
        self.name_check_action: QAction = ...

        super().__init__(screen_rect, dialog_title)

    def get_new_dialog_data(self) -> BasicSqliteDTO: ...

    def setup_content_ui(self):
        self.setup_name_form()
        self.setup_other_content_ui()

    def setup_name_form(self):
        self.name_layout = QFormLayout()

        self.name_label = QLabel(self.frame)
        self.name_label.setObjectName('name_label')

        self.name_input = QLineEdit(self.frame)
        self.name_input.setObjectName('name_input')

        self.name_layout.addRow(self.name_label, self.name_input)

        self.name_checker = QLabel(self.frame)

        self.name_layout.addRow(self.placeholder_blank, self.name_checker)

        self.frame_layout.addLayout(self.name_layout)

    def setup_other_content_ui(self): ...

    def connect_other_signal(self):
        self.name_input.textEdited.connect(self.check_name_available)
        self.name_input.textEdited.connect(self.check_input)
        self.connect_child_signal()

    def connect_child_signal(self): ...

    def check_name_available(self, name):
        if name:
            self.name_available = self.check_available(name)
            if self.name_available:
                prompt = NAME_AVAILABLE.format(name)
                style = "color:green"
                # 重载样式表
                self.name_input.setStyleSheet(read_qss())
                icon = get_icon(NAME_AVAILABLE)
            else:
                prompt = NAME_EXISTS.format(name)
                style = "color:red"
                self.name_input.setStyleSheet("#name_input{border-color:red;color:red}")
                icon = get_icon(NAME_EXISTS)
            self.name_check_action = QAction()
            self.name_check_action.setIcon(icon)
            self.name_input.addAction(self.name_check_action, QLineEdit.ActionPosition.TrailingPosition)
            self.name_checker.setText(prompt)
            self.name_checker.setStyleSheet(style)
        else:
            self.name_input.setStyleSheet(read_qss())
            self.name_checker.setStyleSheet(read_qss())
            self.name_checker.setText('')
            self.name_input.removeAction(self.name_check_action)

    def check_available(self, name):
        if self.old_name:
            return (self.old_name != name and name not in self.name_list) or self.old_name == name
        else:
            return name not in self.name_list

    def post_process(self):
        self.setup_input_limit_rule()
        # 如果读取数据库，那么打开线程执行器
        if self.read_storage:
            self.read_storage_executor = self.get_read_storage_executor(self.set_old_dialog_data)
            self.read_storage_executor.start()
        else:
            self.init_lineedit_button_status()

    def get_read_storage_executor(self, callback) -> LoadingMaskThreadExecutor: ...

    def set_old_dialog_data(self, dialog_data):
        self.dialog_data = dialog_data
        self.init_lineedit_button_status()

    def init_lineedit_button_status(self):
        self.setup_lineedit_value()
        self.check_input()

    def setup_input_limit_rule(self):
        # 设置名称最多可输入100字
        self.name_input.setMaxLength(100)
        self.setup_other_input_limit_rule()

    def setup_other_input_limit_rule(self): ...

    def setup_lineedit_value(self):
        if self.dialog_data and self.dialog_data.id:
            # 数据回显
            self.setup_echo_data()
        else:
            # 默认值展示
            self.setup_default_value()

    def setup_echo_data(self):
        self.old_name = self.get_old_name()
        self.name_input.setText(self.old_name)
        self.setup_echo_other_data()

    def get_old_name(self) -> str: ...

    def setup_echo_other_data(self): ...

    def setup_default_value(self): ...

    def check_input(self):
        # 收集用户输入数据
        self.collect_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if self.button_available():
            self.set_button_available()
        else:
            self.init_button_status()

    def collect_input(self): ...

    def button_available(self) -> bool: ...

    def set_button_available(self):
        self.save_button.setDisabled(False)
        self.set_other_button_available()

    def set_other_button_available(self): ...

    def init_button_status(self):
        self.save_button.setDisabled(True)
        self.init_other_button_status()

    def init_other_button_status(self): ...

    def dialog_data_no_change(self, title):
        # 没有更改任何信息
        pop_ok(NO_CHANGE_PROMPT, title, self)
        self.close()
