# -*- coding: utf-8 -*-
from src.constant.export_import_constant import OVERRIDE_TYPE_MAPPING_TITLE
from src.service.async_func.async_type_mapping_task import OverrideTypeMappingExecutor
from src.view.frame.import_error_data_process.import_duplicate_data_process_dialog_frame import \
    ImportDuplicateDataProcessDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 10:32'


class ImportDuplicateTypeMappingProcessDialogFrame(ImportDuplicateDataProcessDialogFrame):

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_override_data_executor(self, row_list, success_callback) -> OverrideTypeMappingExecutor:
        return OverrideTypeMappingExecutor(row_list, self, self, OVERRIDE_TYPE_MAPPING_TITLE,
                                           success_callback=success_callback)

    # ------------------------------ 信号槽处理 end ------------------------------ #
