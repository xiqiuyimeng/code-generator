# -*- coding: utf-8 -*-
from src.constant.export_import_constant import EXPORT_TYPE_MAPPING_TITLE
from src.service.async_func.async_type_mapping_task import ExportTypeMappingExecutor
from src.view.frame.export_dialog_frame import ExportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 9:46'


class ExportTypeMappingDialogFrame(ExportDialogFrame):

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_process_data_executor(self) -> ExportTypeMappingExecutor:
        return ExportTypeMappingExecutor(self.row_ids, self.file_path_linedit.text(),
                                         self, self, EXPORT_TYPE_MAPPING_TITLE)

    # ------------------------------ 信号槽处理 end ------------------------------ #
