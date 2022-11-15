# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QFrame, QLabel, QFormLayout, QLineEdit, QGridLayout, QPushButton, QAction

from constant.constant import DS_NAME_EXISTS, DS_NAME_AVAILABLE, DS_INFO_NO_CHANGE_PROMPT, SAVE_DS_INFO_TITLE
from service.read_qrc.read_config import read_qss
from view.box.message_box import pop_ok
from view.custom_widget.draggable_widget import DraggableDialog

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class AbstractDsInfoDialog(DraggableDialog):
    """数据源对话框抽象类，整体对话框结构应为四部分：标题区、名称表单区、数据源信息表单区、按钮区"""

    def __init__(self, ds_info, dialog_title, screen_rect, ds_name_id_dict):
        super().__init__()
        self.dialog_title = dialog_title
        # 从数据库中读取到的信息，编辑时使用
        self.ds_info = ds_info

        self.parent_screen_rect = screen_rect
        # 当前数据源名称列表字典，key: name, value: id
        self.ds_name_id_dict: dict = ds_name_id_dict
        self.name_available = True
        self.name_changed = False

        # 当前对话框主布局
        self.dialog_layout: QVBoxLayout = ...
        # 当前对话框框架，用于放置所有部件
        self.frame: QFrame = ...
        # 框架布局，分四部分，第一部分为标题部分，第二部分为数据源名称表单部分，第三部分为数据源内容信息部分、第四部分为按钮部分
        self.frame_layout: QVBoxLayout = ...
        self.ds_name_layout: QFormLayout = ...
        # 数据源内容信息布局
        self.ds_info_layout = ...
        self.title: QLabel = ...
        self.ds_name_label: QLabel = ...
        self.ds_name_value: QLineEdit = ...
        self.ds_name_checker: QLabel = ...
        self.button_layout: QGridLayout = ...
        self.cancel_button: QPushButton = ...
        self.ok_button: QPushButton = ...
        self.button_blank: QLabel = ...
        self.name_check_action = ...

        self.setup_ui()
        self.setup_label_text()
        self.setup_lineedit_value()
        self.check_input()
        self.setup_input_limit_rule()
        self.connect_signal()

    def setup_ui(self):
        # 计算窗口大小
        self.resize_window()
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.dialog_layout = QVBoxLayout(self)
        self.frame = QFrame(self)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("ds_frame")
        self.dialog_layout.addWidget(self.frame)
        self.frame_layout = QVBoxLayout(self.frame)

        # 标题
        self.setup_title_ui()
        # 数据源名称表单
        self.setup_ds_name_ui()
        # 数据源信息
        self.setup_ds_content_info_ui()
        self.frame_layout.addLayout(self.ds_info_layout)
        # 按钮
        self.setup_button_ui()

    def resize_window(self): ...

    def setup_title_ui(self):
        self.title = QLabel(self.frame)
        self.title.setObjectName("ds_title")
        self.frame_layout.addWidget(self.title)

    def setup_ds_name_ui(self):
        self.ds_name_layout = QFormLayout()

        # 数据源名称
        self.ds_name_label = QLabel(self.frame)
        self.ds_name_value = QLineEdit(self.frame)
        self.ds_name_value.setObjectName("ds_name_value")
        self.ds_name_layout.addRow(self.ds_name_label, self.ds_name_value)

        # 数据源名称检查器
        self.ds_name_checker = QLabel(self.frame)
        self.ds_name_checker.setFixedHeight(self.ds_name_label.height())
        self.ds_name_layout.addRow('', self.ds_name_checker)

        self.frame_layout.addLayout(self.ds_name_layout)

    def setup_ds_content_info_ui(self): ...

    def setup_button_ui(self): ...

    def setup_label_text(self): ...

    def setup_lineedit_value(self):
        if self.ds_info.id:
            # 数据回显
            self.setup_ds_info_value_show()
        else:
            # 默认值展示
            self.setup_ds_info_default_value()

    def setup_ds_info_value_show(self): ...

    def setup_ds_info_default_value(self): ...

    def check_input(self):
        # 收集用户输入数据
        self.collect_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if self.button_available():
            self.set_button_available()
        else:
            self.init_button_status()

    def button_available(self) -> bool: ...

    def collect_input(self): ...

    def init_button_status(self):
        self.ok_button.setDisabled(True)
        self.init_other_button_status()

    def init_other_button_status(self): ...

    def set_button_available(self):
        self.ok_button.setDisabled(False)
        self.set_other_button_available()

    def set_other_button_available(self): ...

    def setup_input_limit_rule(self):
        # 设置名称最多可输入字符数
        self.ds_name_value.setMaxLength(100)
        # 数据源信息的输入限制规则
        self.setup_input_ds_info_limit_rule()

    def setup_input_ds_info_limit_rule(self): ...

    def connect_signal(self):
        self.ds_name_value.textEdited.connect(self.check_name_available)
        self.ds_name_value.textEdited.connect(self.check_input)
        self.ok_button.clicked.connect(self.save_ds_info)
        self.cancel_button.clicked.connect(self.close)
        # 数据源信息相关的信号槽连接
        self.connect_ds_other_signal()

    def connect_ds_other_signal(self): ...

    def check_name_available(self, ds_name):
        if ds_name:
            self.name_available = self.check_available(ds_name)
            if self.name_available:
                prompt = DS_NAME_AVAILABLE.format(ds_name)
                style = "color:green"
                # 重载样式表
                self.ds_name_value.setStyleSheet(read_qss())
                icon = QIcon(":/icon/right.png")
            else:
                prompt = DS_NAME_EXISTS.format(ds_name)
                style = "color:red"
                self.ds_name_value.setStyleSheet("#ds_name_value{border-color:red;color:red}")
                icon = QIcon(":/icon/wrong.png")
            self.name_check_action = QAction()
            self.name_check_action.setIcon(icon)
            self.ds_name_value.addAction(self.name_check_action, QLineEdit.ActionPosition.TrailingPosition)
            self.ds_name_checker.setText(prompt)
            self.ds_name_checker.setStyleSheet(style)
        else:
            self.ds_name_value.setStyleSheet(read_qss())
            self.ds_name_checker.setStyleSheet(read_qss())
            self.ds_name_checker.setText("")
            self.ds_name_value.removeAction(self.name_check_action)

    def check_available(self, ds_name):
        # 如果根据name能取到id，判断id是否是当前的id，
        # 如果当前是新增，id为空，取出的id应该为空才证明名称可用不重复
        # 如果当前是编辑，那么id如果是当前数据源的id，证明名称无变化，可用
        ds_id = self.ds_name_id_dict.get(ds_name)
        return (ds_id is None) or (ds_id == self.ds_info.id)

    def save_ds_info(self): ...

    def ds_info_no_change(self):
        # 没有更改任何信息
        pop_ok(DS_INFO_NO_CHANGE_PROMPT, SAVE_DS_INFO_TITLE, self)
        self.close()

