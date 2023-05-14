# -*- coding: utf-8 -*-
from src.view.dialog.import_dialog import ImportDialog
from src.view.frame.type_mapping.import_type_mapping_dialog_frame import ImportTypeMappingDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 10:02'


class ImportTypeMappingDialog(ImportDialog):

    def get_frame(self) -> ImportTypeMappingDialogFrame:
        return ImportTypeMappingDialogFrame(self, self.dialog_title,
                                            import_success_callback=self.import_success_callback,
                                            get_row_data_dialog=self.get_row_data_dialog)
