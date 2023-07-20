# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit

from src.constant.dialog_constant import NAME_MAX_LENGTH_PLACEHOLDER_TEXT
from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.service.system_storage.sqlite_abc import BasicSqliteDTO
from src.view.frame.frame_func import check_name_available
from src.view.frame.save_dialog_frame import SaveDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/3 12:43'


class NameCheckDialogFrame(SaveDialogFrame):
    """具有名称检查功能的对话框框架，内置一个名称输入表单"""

    def __init__(self, parent_dialog, dialog_title, exists_names,
                 dialog_data=None, read_storage=True, **kwargs):
        # 框架布局，分四部分，第一部分：标题部分，第二部分：名称表单，第三部分：其他内容，第四部分：按钮部分
        # 存储当前已经存在的名称列表
        self.exists_names = exists_names
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
        super().__init__(parent_dialog, dialog_title, **kwargs)

    def get_new_dialog_data(self) -> BasicSqliteDTO:
        ...

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.setup_name_form()
        self.frame_layout.addLayout(self.name_layout)
        self.setup_other_content_ui()

    def setup_name_form(self):
        self.name_layout = QFormLayout()

        self.name_label = QLabel(self)
        self.name_label.setObjectName('form_label')

        self.name_input = QLineEdit(self)

        self.name_layout.addRow(self.name_label, self.name_input)

        self.name_checker = QLabel(self)
        self.name_layout.addRow(self.placeholder_blank, self.name_checker)

    def setup_other_content_ui(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.name_input.textEdited.connect(self.check_name_available)
        self.name_input.textEdited.connect(self.check_input)
        self.connect_child_signal()

    def check_name_available(self, name):
        self.name_available = check_name_available(name, self.old_name, self.exists_names,
                                                   self.name_input, self.name_checker)

    def check_input(self):
        # 收集用户输入数据
        self.collect_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if self.button_available():
            # 如果数据变化，应该放开保存按钮
            if self.check_data_changed():
                self.save_button.setDisabled(False)
            else:
                # 否则按钮应该不可用
                self.save_button.setDisabled(True)
        else:
            self.save_button.setDisabled(True)

    def collect_input(self):
        ...

    def button_available(self) -> bool:
        ...

    def check_data_changed(self) -> bool:
        ...

    def connect_child_signal(self):
        ...

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.setup_input_limit_rule()
        self.setup_placeholder_text()
        # 如果读取数据库，那么打开线程执行器
        if self.read_storage:
            self.read_storage_executor = self.get_read_storage_executor(self.set_old_dialog_data)
            self.read_storage_executor.start()
        else:
            self.init_lineedit_button_status()

    def setup_input_limit_rule(self):
        # 设置名称最多可输入50字
        self.name_input.setMaxLength(50)
        self.setup_other_input_limit_rule()

    def setup_other_input_limit_rule(self):
        ...

    def setup_placeholder_text(self):
        self.name_input.setPlaceholderText(NAME_MAX_LENGTH_PLACEHOLDER_TEXT)
        self.setup_other_placeholder_text()

    def setup_other_placeholder_text(self):
        ...

    def get_read_storage_executor(self, callback) -> LoadingMaskThreadExecutor:
        ...

    def set_old_dialog_data(self, dialog_data):
        self.dialog_data = dialog_data
        self.init_lineedit_button_status()

    def init_lineedit_button_status(self):
        self.setup_lineedit_value()
        self.check_input()

    def setup_lineedit_value(self):
        if self.check_edit():
            # 数据回显
            self.setup_echo_data()
        else:
            # 默认值展示
            self.setup_default_value()

    def check_edit(self):
        """判断是否是编辑"""
        return self.dialog_data and self.dialog_data.id

    def setup_echo_data(self):
        self.old_name = self.get_old_name()
        self.name_input.setText(self.old_name)
        self.setup_echo_other_data()

    def get_old_name(self) -> str:
        ...

    def setup_echo_other_data(self):
        ...

    def setup_default_value(self):
        ...

    # ------------------------------ 后置处理 end ------------------------------ #
