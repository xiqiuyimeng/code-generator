# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton

from src.constant.template_dialog_constant import SELECT_ALL_BTN_TEXT, UNSELECT_BTN_TEXT, \
    COPY_OTHER_TP_FUNC_BTN_TEXT, CREATE_NEW_FUNC_BTN_TEXT, DEL_FUNC_BTN_TEXT, CREATE_NEW_FUNC_TITLE
from src.view.dialog.template.template_copy_func_dialog import TemplateCopyFuncDialog
from src.view.dialog.template.template_func_detail_dialog import TemplateFuncDetailDialog
from src.view.list_widget.list_item_func import set_template_func_data
from src.view.list_widget.template_func_list_widget import TemplateFuncListWidget

_author_ = 'luwt'
_date_ = '2023/6/25 13:48'


class TemplateFuncWidget(QWidget):
    """模板方法页，嵌入在堆栈式窗口中"""

    def __init__(self, template_id):
        super().__init__()
        self.template_id = template_id
        self._layout: QVBoxLayout = ...
        # 模板方法顶部按钮区
        self.func_list_header_layout: QHBoxLayout = ...
        self.select_button: QPushButton = ...
        self.unselect_button: QPushButton = ...
        self.copy_other_tp_func_button: QPushButton = ...
        self.create_new_func_button: QPushButton = ...
        self.delete_func_button: QPushButton = ...
        # 方法列表
        self.func_list_widget: TemplateFuncListWidget = ...
        # 方法详情
        self.func_detail_dialog: TemplateFuncDetailDialog = ...
        # 复制模板方法对话框
        self.copy_other_tp_func_dialog: TemplateCopyFuncDialog = ...

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()

    def setup_ui(self):
        self._layout = QVBoxLayout(self)
        self.func_list_header_layout = QHBoxLayout(self)
        self._layout.addLayout(self.func_list_header_layout)
        # 全选按钮
        self.select_button = QPushButton(self)
        self.select_button.setObjectName('select_button')
        self.func_list_header_layout.addWidget(self.select_button)
        self.unselect_button = QPushButton()
        self.unselect_button.setObjectName('unselect_button')
        self.func_list_header_layout.addWidget(self.unselect_button)
        # 从其他模板复制方法按钮
        self.copy_other_tp_func_button = QPushButton(self)
        self.copy_other_tp_func_button.setObjectName('copy_row_button')
        self.func_list_header_layout.addWidget(self.copy_other_tp_func_button)
        # 创建新方法按钮
        self.create_new_func_button = QPushButton()
        self.create_new_func_button.setObjectName('create_row_button')
        self.func_list_header_layout.addWidget(self.create_new_func_button)
        # 删除方法按钮
        self.delete_func_button = QPushButton()
        self.delete_func_button.setObjectName('del_row_button')
        self.func_list_header_layout.addWidget(self.delete_func_button)

        # 方法列表
        self.func_list_widget = TemplateFuncListWidget(self.open_create_func_dialog,  self)
        self._layout.addWidget(self.func_list_widget)

    def setup_label_text(self):
        self.select_button.setText(SELECT_ALL_BTN_TEXT)
        self.unselect_button.setText(UNSELECT_BTN_TEXT)
        self.copy_other_tp_func_button.setText(COPY_OTHER_TP_FUNC_BTN_TEXT)
        self.create_new_func_button.setText(CREATE_NEW_FUNC_BTN_TEXT)
        self.delete_func_button.setText(DEL_FUNC_BTN_TEXT)

    def connect_signal(self):
        self.select_button.clicked.connect(self.func_list_widget.select_all_item)
        self.unselect_button.clicked.connect(self.func_list_widget.unselect_all_item)
        # 从其他模板复制方法，需要打开对话框
        self.copy_other_tp_func_button.clicked.connect(self.open_copy_func_dialog)
        self.create_new_func_button.clicked.connect(lambda: self.open_create_func_dialog(CREATE_NEW_FUNC_TITLE))
        self.delete_func_button.clicked.connect(self.func_list_widget.remove_selected_item)

    def open_copy_func_dialog(self):
        self.copy_other_tp_func_dialog = TemplateCopyFuncDialog(self.template_id,
                                                                self.func_list_widget.collect_item_text())
        self.copy_other_tp_func_dialog.copy_func_list_signal.connect(self.copy_template_func)
        self.copy_other_tp_func_dialog.exec()

    def copy_template_func(self, func_list):
        self.func_list_widget.copy_func_list(func_list)

    def open_create_func_dialog(self, dialog_title, template_func=None):
        self.func_detail_dialog = TemplateFuncDetailDialog(self.func_list_widget.collect_item_text(),
                                                           dialog_title, template_func)
        if template_func:
            self.func_detail_dialog.edit_signal.connect(self.edit_template_func)
        else:
            self.func_detail_dialog.save_signal.connect(self.add_template_func)
        self.func_detail_dialog.exec()

    def edit_template_func(self, template_func):
        current_item = self.func_list_widget.currentItem()
        current_item.setText(template_func.func_name)
        set_template_func_data(current_item, template_func)

    def add_template_func(self, template_func):
        func_item = self.func_list_widget.add_item(template_func.func_name)
        self.func_list_widget.setCurrentItem(func_item)
        set_template_func_data(func_item, template_func)

    def collect_template_func_list(self):
        return self.func_list_widget.collect_template_func_list()

    def echo_template_func_list(self, template_func_list):
        self.func_list_widget.fill_list_widget(template_func_list)
        # 找出当前项
        current_func_list = [func for func in template_func_list if func.is_current]
        if current_func_list:
            self.func_list_widget.setCurrentRow(template_func_list.index(current_func_list[0]))
