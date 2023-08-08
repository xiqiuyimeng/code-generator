# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QLabel

from src.constant.help.help_constant import TEMPLATE_COPY_FUNC_HELP
from src.constant.template_dialog_constant import SELECT_ALL_FUNC_BTN_TEXT, UNSELECT_ALL_FUNC_BTN_TEXT, \
    COPY_FUNC_BTN_TEXT, TEMPLATE_FUNC_BOX_TITLE, BACK_TO_TEMPLATE_BTN_TEXT
from src.service.async_func.async_template_task import ListTemplateFuncExecutor
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.list_widget.copy_template_func_list_widget import CopyTemplateFuncListWidget

_author_ = 'luwt'
_date_ = '2023/6/25 18:09'


class TemplateCopyFuncListFrame(DialogFrameABC):
    """复制模板方法列表框架"""

    def __init__(self, template_id, template_frame, copy_template_func, parent_dialog, title):
        self.template_id = template_id
        # 模板frame，在返回模板列表页时使用
        self.template_frame = template_frame
        # 复制模板方法的函数
        self.copy_template_func = copy_template_func
        # 顶部按钮
        self.header_button_layout: QHBoxLayout = ...
        self.select_all_button: QPushButton = ...
        self.unselect_all_button: QPushButton = ...
        self.copy_func_button: QPushButton = ...
        self.back_button: QPushButton = ...
        self.func_list_widget: CopyTemplateFuncListWidget = ...
        self.list_template_func_executor: ListTemplateFuncExecutor = ...
        super().__init__(parent_dialog, title)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.header_button_layout = QHBoxLayout()
        self.frame_layout.addLayout(self.header_button_layout)
        self.select_all_button = QPushButton()
        self.select_all_button.setObjectName('select_button')
        self.header_button_layout.addWidget(self.select_all_button)
        self.unselect_all_button = QPushButton()
        self.unselect_all_button.setObjectName('unselect_button')
        self.header_button_layout.addWidget(self.unselect_all_button)
        # 增加空白label
        self.header_button_layout.addWidget(QLabel())
        self.header_button_layout.addWidget(QLabel())
        self.copy_func_button = QPushButton()
        self.copy_func_button.setObjectName('copy_row_button')
        self.header_button_layout.addWidget(self.copy_func_button)
        # 创建方法列表控件
        self.func_list_widget = CopyTemplateFuncListWidget(self)
        self.frame_layout.addWidget(self.func_list_widget)

    def get_blank_right_buttons(self) -> tuple:
        self.back_button = QPushButton(self)
        self.back_button.setObjectName('to_previous_button')
        return self.back_button,

    def setup_other_label_text(self):
        self.select_all_button.setText(SELECT_ALL_FUNC_BTN_TEXT)
        self.unselect_all_button.setText(UNSELECT_ALL_FUNC_BTN_TEXT)
        self.copy_func_button.setText(COPY_FUNC_BTN_TEXT)
        self.back_button.setText(BACK_TO_TEMPLATE_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_COPY_FUNC_HELP

    def connect_other_signal(self):
        self.select_all_button.clicked.connect(self.func_list_widget.select_all_item)
        self.unselect_all_button.clicked.connect(self.func_list_widget.unselect_all_item)
        self.copy_func_button.clicked.connect(self.copy_func)
        self.back_button.clicked.connect(self.back_to_template_frame)

    def copy_func(self):
        template_func_list = self.func_list_widget.collect_selected_data()
        # 复制到当前模板
        if template_func_list:
            self.copy_template_func(template_func_list)

    def back_to_template_frame(self):
        # 切换页面
        self.parent_dialog.layout().removeWidget(self)
        self.hide()
        self.parent_dialog.layout().addWidget(self.template_frame)
        if self.template_frame.isHidden():
            self.template_frame.show()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 清除焦点
        self.select_all_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.unselect_all_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.copy_func_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.back_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        box_title = TEMPLATE_FUNC_BOX_TITLE.format(self.dialog_title)
        self.list_template_func_executor = ListTemplateFuncExecutor(self.template_id, self.parent_dialog,
                                                                    self.parent_dialog, box_title,
                                                                    self.func_list_widget.fill_list_widget)
        self.list_template_func_executor.start()

    # ------------------------------ 后置处理 end ------------------------------ #
