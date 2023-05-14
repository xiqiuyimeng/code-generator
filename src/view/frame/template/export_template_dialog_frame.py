# -*- coding: utf-8 -*-
from src.constant.export_import_constant import EXPORT_TEMPLATE_TITLE
from src.service.async_func.async_template_task import ExportTemplateExecutor
from src.view.frame.export_dialog_frame import ExportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 18:29'


class ExportTemplateDialogFrame(ExportDialogFrame):

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_process_data_executor(self) -> ExportTemplateExecutor:
        return ExportTemplateExecutor(self.row_ids, self.file_path_linedit.text(),
                                      self, self, EXPORT_TEMPLATE_TITLE)

    # ------------------------------ 信号槽处理 end ------------------------------ #
