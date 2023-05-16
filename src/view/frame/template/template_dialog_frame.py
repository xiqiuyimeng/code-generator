# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.export_import_constant import EXPORT_TEMPLATE_TITLE, EXPORT_TEMPLATE_FILE_NAME, \
    PROCESS_DUPLICATE_TEMPLATE_TITLE, OVERRIDE_TEMPLATE_TITLE, PROCESS_ILLEGAL_TEMPLATE_TITLE, IMPORT_TEMPLATE_TITLE
from src.constant.template_dialog_constant import FUNC_DIALOG_BTN_TEXT, ADD_TEMPLATE_BTN_TEXT, \
    DEL_TEMPLATE_BTN_TEXT, DEL_TEMPLATE_PROMPT, DEL_TEMPLATE_BOX_TITLE, BATCH_TEMPLATE_PROMPT, \
    TEMPLATE_LIST_BOX_TITLE, IMPORT_TEMPLATE_BTN_TEXT, EXPORT_TEMPLATE_BTN_TEXT
from src.service.async_func.async_template_task import DelTemplateExecutor, BatchDelTemplateExecutor, \
    ListTemplateExecutor, ExportTemplateExecutor, ImportTemplateExecutor, OverrideTemplateExecutor
from src.view.dialog.export_dialog import ExportDialog
from src.view.dialog.import_dialog import ImportDialog
from src.view.dialog.template.template_detail_dialog import TemplateDetailDialog
from src.view.dialog.template.template_func_dialog import TemplateFuncDialog
from src.view.frame.table_dialog_frame import TableDialogFrame
from src.view.table.table_widget.template_table_widget.template_table_widget import TemplateTableWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:33'


class TemplateDialogFrame(TableDialogFrame):
    """模板列表表格对话框框架"""

    def __init__(self, parent_dialog, dialog_title):
        # 打开常用方法对话框按钮
        self.open_template_func_dialog_btn: QPushButton = ...
        # 常用方法对话框
        self.template_func_dialog: TemplateFuncDialog = ...
        super().__init__(parent_dialog, dialog_title)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def make_table_widget(self):
        self.table_widget = TemplateTableWidget(self.table_frame)

    def setup_first_button(self) -> QPushButton:
        self.open_template_func_dialog_btn = QPushButton(self)
        return self.open_template_func_dialog_btn

    def setup_other_label_text(self):
        self.open_template_func_dialog_btn.setText(FUNC_DIALOG_BTN_TEXT)
        self.add_row_button.setText(ADD_TEMPLATE_BTN_TEXT)
        self.del_row_button.setText(DEL_TEMPLATE_BTN_TEXT)
        self.import_button.setText(IMPORT_TEMPLATE_BTN_TEXT)
        self.export_button.setText(EXPORT_TEMPLATE_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_special_signal(self):
        self.open_template_func_dialog_btn.clicked.connect(self.open_template_func_dialog)

    def open_template_func_dialog(self):
        """打开模板常用方法对话框"""
        self.template_func_dialog = TemplateFuncDialog(self.parent_dialog.parent_screen_rect)
        self.template_func_dialog.exec()

    def do_get_row_data_dialog(self, row_id) -> TemplateDetailDialog:
        template_names = [self.table_widget.item(row, 1).text() for row in range(self.table_widget.rowCount())]
        return TemplateDetailDialog(self.parent_dialog.parent_screen_rect, template_names, row_id)

    def get_del_prompt_title(self):
        return DEL_TEMPLATE_PROMPT, DEL_TEMPLATE_BOX_TITLE

    def get_del_executor(self, row_id, item_name, row_index, del_title) -> DelTemplateExecutor:
        return DelTemplateExecutor(row_id, item_name, row_index, self.parent_dialog, self.parent_dialog,
                                   del_title, self.table_widget.del_row)

    def get_batch_del_prompt_title(self):
        return BATCH_TEMPLATE_PROMPT, DEL_TEMPLATE_BOX_TITLE

    def get_batch_del_executor(self, delete_ids, delete_names, del_title) -> BatchDelTemplateExecutor:
        return BatchDelTemplateExecutor(delete_ids, delete_names, self.parent_dialog, self.parent_dialog,
                                        del_title, self.table_widget.del_rows)

    def get_import_dialog(self, import_success_callback, get_row_data_dialog) -> ImportDialog:
        return ImportDialog(ImportTemplateExecutor, PROCESS_DUPLICATE_TEMPLATE_TITLE,
                            OverrideTemplateExecutor, OVERRIDE_TEMPLATE_TITLE,
                            PROCESS_ILLEGAL_TEMPLATE_TITLE, import_success_callback,
                            get_row_data_dialog, IMPORT_TEMPLATE_TITLE,
                            self.parent_dialog.parent_screen_rect)

    def get_export_dialog(self, row_ids) -> ExportDialog:
        return ExportDialog(row_ids, EXPORT_TEMPLATE_FILE_NAME, ExportTemplateExecutor,
                            EXPORT_TEMPLATE_TITLE, self.parent_dialog.parent_screen_rect)

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_list_table_data_executor(self) -> ListTemplateExecutor:
        return ListTemplateExecutor(self.parent_dialog, self.parent_dialog, TEMPLATE_LIST_BOX_TITLE,
                                    self.table_widget.fill_table)

    # ------------------------------ 后置处理 end ------------------------------ #
