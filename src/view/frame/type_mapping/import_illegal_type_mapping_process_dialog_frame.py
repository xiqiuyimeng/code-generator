# -*- coding: utf-8 -*-
from src.view.frame.import_error_data_process.import_illegal_data_process_dialog_frame import \
    ImportIllegalDataProcessDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 11:00'


class ImportIllegalTypeMappingProcessDialogFrame(ImportIllegalDataProcessDialogFrame):

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_row_detail_dialog(self, row_data):
        return self.get_row_data_dialog(row_data=row_data)

    # ------------------------------ 信号槽处理 end ------------------------------ #
