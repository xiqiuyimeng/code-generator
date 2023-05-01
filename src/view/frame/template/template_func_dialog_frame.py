# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QListWidgetItem

from src.constant.template_dialog_constant import CREATE_NEW_FUNC_BTN_TEXT, CREATE_NEW_FUNC_TITLE, \
    TEMPLATE_FUNC_LIST_TITLE
from src.service.async_func.async_template_func_task import ListTemplateFuncExecutor
from src.view.dialog.template.template_func_detail_dialog import TemplateFuncDetailDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.list_widget.list_item_func import set_template_func_data
from src.view.list_widget.template_func_list_widget import TemplateFuncListWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:36'


class TemplateFuncDialogFrame(DialogFrameABC):
    """模板方法对话框框架"""

    def __init__(self, parent_dialog, title):
        self.parent_dialog = parent_dialog
        self.list_widget: TemplateFuncListWidget = ...
        self.create_new_func_btn: QPushButton = ...
        self.func_detail_dialog: TemplateFuncDetailDialog = ...
        self.list_func_executor: ListTemplateFuncExecutor = ...
        super().__init__(parent_dialog, title, placeholder_blank_width=1)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 方法区列表
        self.list_widget = TemplateFuncListWidget(self.open_create_func_dialog, self)
        self.frame_layout.addWidget(self.list_widget)

    def get_blank_left_buttons(self) -> tuple:
        self.create_new_func_btn = QPushButton()
        return self.create_new_func_btn,

    def setup_other_label_text(self):
        self.create_new_func_btn.setText(CREATE_NEW_FUNC_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.create_new_func_btn.clicked.connect(lambda: self.open_create_func_dialog(CREATE_NEW_FUNC_TITLE))

    def open_create_func_dialog(self, dialog_title, template_func=None):
        self.func_detail_dialog = TemplateFuncDetailDialog(self.parent_dialog.parent_screen_rect, dialog_title,
                                                           self.list_widget.collect_item_text_list(),
                                                           template_func)
        if template_func:
            self.func_detail_dialog.edit_signal.connect(self.edit_template_func)
        else:
            self.func_detail_dialog.save_signal.connect(self.add_template_func)
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
        self.list_func_executor = ListTemplateFuncExecutor(self.parent_dialog, self.parent_dialog,
                                                           TEMPLATE_FUNC_LIST_TITLE, self.fill_list_widget)
        self.list_func_executor.start()

    def fill_list_widget(self, func_list):
        # 填充列表
        for func in func_list:
            func_item = QListWidgetItem(func.func_name)
            self.list_widget.addItem(func_item)
            set_template_func_data(func_item, func)

    # ------------------------------ 后置处理 end ------------------------------ #
