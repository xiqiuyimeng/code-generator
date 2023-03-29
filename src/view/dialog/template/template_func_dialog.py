# -*- coding: utf-8 -*-
"""模板常用方法对话框"""
from PyQt5.QtWidgets import QPushButton, QListWidgetItem

from src.constant.template_dialog_constant import TEMPLATE_FUNC_TITLE, CREATE_NEW_FUNC_BTN_TEXT, \
    CREATE_NEW_FUNC_TITLE, TEMPLATE_FUNC_LIST_TITLE
from src.service.async_func.async_template_func_task import ListTemplateFuncExecutor
from src.view.dialog.custom_dialog import CustomDialog
from src.view.dialog.template.template_func_detail_dialog import TemplateFuncDetailDialog
from src.view.list_widget.list_item_func import set_template_func_data
from src.view.list_widget.template_func_list_widget import TemplateFuncListWidget

_author_ = 'luwt'
_date_ = '2023/3/10 10:51'


class TemplateFuncDialog(CustomDialog):

    def __init__(self, screen_rect):
        self.list_widget: TemplateFuncListWidget = ...
        self.create_new_func_btn: QPushButton = ...
        self.func_detail_dialog: TemplateFuncDetailDialog = ...
        self.list_func_executor: ListTemplateFuncExecutor = ...
        super().__init__(screen_rect, TEMPLATE_FUNC_TITLE)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.5, self.parent_screen_rect.height() * 0.7)

    def setup_content_ui(self):
        # 方法区列表
        self.list_widget = TemplateFuncListWidget(self.open_create_func_dialog, self.frame)
        self.frame_layout.addWidget(self.list_widget)

    def setup_other_button(self):
        self.create_new_func_btn = QPushButton()
        self.button_layout.addWidget(self.create_new_func_btn, 0, 0, 1, 1)

    def setup_other_label_text(self):
        self.create_new_func_btn.setText(CREATE_NEW_FUNC_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.create_new_func_btn.clicked.connect(lambda: self.open_create_func_dialog(CREATE_NEW_FUNC_TITLE))

    def open_create_func_dialog(self, dialog_title, template_func=None):
        self.func_detail_dialog = TemplateFuncDetailDialog(self.parent_screen_rect, dialog_title,
                                                           self.list_widget.collect_item_text_list(),
                                                           template_func)
        if template_func:
            self.func_detail_dialog.edit_func_signal.connect(self.edit_template_func)
        else:
            self.func_detail_dialog.add_func_signal.connect(self.add_template_func)
        self.func_detail_dialog.exec()

    def edit_template_func(self, template_func):
        current_item = self.list_widget.currentItem()
        current_item.setText(template_func.func_name)
        set_template_func_data(current_item, template_func)

    def add_template_func(self, template_func):
        func_item = QListWidgetItem(template_func.func_name)
        self.list_widget.addItem(func_item)
        set_template_func_data(func_item, template_func)

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_func_executor = ListTemplateFuncExecutor(self, self, TEMPLATE_FUNC_LIST_TITLE,
                                                           self.fill_list_widget)
        self.list_func_executor.start()

    def fill_list_widget(self, func_list):
        # 填充列表
        for func in func_list:
            func_item = QListWidgetItem(func.func_name)
            self.list_widget.addItem(func_item)
            set_template_func_data(func_item, func)

    # ------------------------------ 后置处理 end ------------------------------ #
