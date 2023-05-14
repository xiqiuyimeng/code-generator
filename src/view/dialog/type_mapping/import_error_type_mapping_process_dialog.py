# -*- coding: utf-8 -*-
from src.constant.export_import_constant import PROCESS_DUPLICATE_TYPE_MAPPING_TITLE, \
    PROCESS_ILLEGAL_TYPE_MAPPING_TITLE
from src.view.dialog.import_error_data_process_dialog import ImportErrorDataProcessDialog
from src.view.frame.type_mapping.import_duplicate_type_mapping_process_dialog_frame import \
    ImportDuplicateTypeMappingProcessDialogFrame
from src.view.frame.type_mapping.import_illegal_type_mapping_process_dialog_frame import \
    ImportIllegalTypeMappingProcessDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 10:41'


class ImportErrorTypeMappingProcessDialog(ImportErrorDataProcessDialog):

    def get_duplicate_data_process_frame(self) -> ImportDuplicateTypeMappingProcessDialogFrame:
        return ImportDuplicateTypeMappingProcessDialogFrame(self.duplicate_rows, self.duplicate_illegal_rows,
                                                            self.import_success_callback,
                                                            self, PROCESS_DUPLICATE_TYPE_MAPPING_TITLE)

    def get_illegal_data_process_frame(self) -> ImportIllegalTypeMappingProcessDialogFrame:
        return ImportIllegalTypeMappingProcessDialogFrame(self.illegal_rows, self.import_success_callback,
                                                          self.get_row_data_dialog,
                                                          self, PROCESS_ILLEGAL_TYPE_MAPPING_TITLE)
