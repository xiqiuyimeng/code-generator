# -*- coding: utf-8 -*-
from src.service.async_func.async_type_mapping_task import ImportTypeMappingExecutor
from src.view.dialog.type_mapping.import_error_type_mapping_process_dialog import ImportErrorTypeMappingProcessDialog
from src.view.frame.import_dialog_frame import ImportDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 10:04'


class ImportTypeMappingDialogFrame(ImportDialogFrame):

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_process_import_data_executor(self, *args, **kwargs) -> ImportTypeMappingExecutor:
        return ImportTypeMappingExecutor(*args, **kwargs)

    def get_process_error_data_dialog(self, *args) -> ImportErrorTypeMappingProcessDialog:
        return ImportErrorTypeMappingProcessDialog(*args, self.import_success_callback,
                                                   self.get_row_data_dialog, self.dialog_title,
                                                   self.parent_dialog.parent_screen_rect)

    # ------------------------------ 信号槽处理 end ------------------------------ #
