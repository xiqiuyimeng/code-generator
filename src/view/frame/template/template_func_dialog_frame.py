# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QListWidgetItem, QGridLayout, QLabel

from src.constant.export_import_constant import PROCESS_DUPLICATE_TEMPLATE_FUNC_TITLE, OVERRIDE_TEMPLATE_FUNC_TITLE, \
    IMPORT_TEMPLATE_FUNC_TITLE, EXPORT_TEMPLATE_FUNC_FILE_NAME, \
    EXPORT_TEMPLATE_FUNC_TITLE
from src.constant.help.help_constant import TEMPLATE_FUNC_TABLE_HELP
from src.constant.template_dialog_constant import CREATE_NEW_FUNC_BTN_TEXT, CREATE_NEW_FUNC_TITLE, \
    TEMPLATE_FUNC_LIST_TITLE, IMPORT_TEMPLATE_FUNC_BTN_TEXT, EXPORT_TEMPLATE_FUNC_BTN_TEXT
from src.service.async_func.async_template_func_task import ListTemplateFuncExecutor, ImportTemplateFuncExecutor, \
    OverrideTemplateFuncExecutor, ExportTemplateFuncExecutor
from src.view.dialog.export_dialog import ExportDialog
from src.view.dialog.import_dialog import ImportDialog
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
        # 顶部按钮区
        self.top_button_layout: QGridLayout = ...
        self.top_button_blank: QLabel = ...
        self.create_new_func_btn: QPushButton = ...
        self.import_template_func_btn: QPushButton = ...
        self.export_template_func_btn: QPushButton = ...
        # 方法列表区
        self.list_widget: TemplateFuncListWidget = ...
        # 导入数据对话框
        self.import_data_dialog: ImportDialog = ...
        # 导出数据对话框
        self.export_data_dialog: ExportDialog = ...
        self.func_detail_dialog: TemplateFuncDetailDialog = ...
        self.list_func_executor: ListTemplateFuncExecutor = ...
        super().__init__(parent_dialog, title, placeholder_blank_width=1)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 顶部按钮区
        self.top_button_layout = QGridLayout(self)
        self.frame_layout.addLayout(self.top_button_layout)
        self.create_new_func_btn = QPushButton(self)
        self.top_button_layout.addWidget(self.create_new_func_btn, 0, 0, 1, 1)
        self.top_button_blank = QLabel(self)
        self.top_button_layout.addWidget(self.top_button_blank, 0, 1, 1, 1)
        self.import_template_func_btn = QPushButton()
        self.top_button_layout.addWidget(self.import_template_func_btn, 0, 2, 1, 1)
        self.export_template_func_btn = QPushButton(self)
        self.top_button_layout.addWidget(self.export_template_func_btn, 0, 3, 1, 1)
        # 方法区列表
        self.list_widget = TemplateFuncListWidget(self.open_create_func_dialog, self.export_template_func, self)
        self.frame_layout.addWidget(self.list_widget)

    def setup_other_label_text(self):
        self.create_new_func_btn.setText(CREATE_NEW_FUNC_BTN_TEXT)
        self.import_template_func_btn.setText(IMPORT_TEMPLATE_FUNC_BTN_TEXT)
        self.export_template_func_btn.setText(EXPORT_TEMPLATE_FUNC_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_FUNC_TABLE_HELP

    def connect_other_signal(self):
        self.create_new_func_btn.clicked.connect(lambda: self.open_create_func_dialog(CREATE_NEW_FUNC_TITLE))
        self.import_template_func_btn.clicked.connect(self.import_template_func)
        self.export_template_func_btn.clicked.connect(lambda: self.export_template_func())

    def open_create_func_dialog(self, dialog_title, template_func=None):
        self.func_detail_dialog = TemplateFuncDetailDialog(self.list_widget.collect_item_text(),
                                                           dialog_title, template_func)
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

    def import_template_func(self):
        # 因为目前模板方法没有导入数据异常情况，所以异常处理不存在，所以不需要异常处理对话框
        self.import_data_dialog = ImportDialog(ImportTemplateFuncExecutor, PROCESS_DUPLICATE_TEMPLATE_FUNC_TITLE,
                                               OverrideTemplateFuncExecutor, OVERRIDE_TEMPLATE_FUNC_TITLE,
                                               None, self.import_success_callback, None, IMPORT_TEMPLATE_FUNC_TITLE)
        self.import_data_dialog.exec()

    def import_success_callback(self, add_data_list, del_data_list=None):
        if del_data_list:
            self.list_widget.del_duplicate_rows(del_data_list)
        self.list_widget.fill_list_widget(add_data_list)

    def export_template_func(self, row_id=None):
        # 如果指定id，导出指定方法；如果没有，导出所有
        if row_id:
            row_ids = row_id,
        else:
            # 获取所有方法id
            row_ids = self.list_widget.collect_func_ids()
        self.export_data_dialog = ExportDialog(row_ids, EXPORT_TEMPLATE_FUNC_FILE_NAME,
                                               ExportTemplateFuncExecutor, EXPORT_TEMPLATE_FUNC_TITLE)
        self.export_data_dialog.exec()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_func_executor = ListTemplateFuncExecutor(self.parent_dialog, self.parent_dialog,
                                                           TEMPLATE_FUNC_LIST_TITLE,
                                                           self.list_widget.fill_list_widget)
        self.list_func_executor.start()

    # ------------------------------ 后置处理 end ------------------------------ #
