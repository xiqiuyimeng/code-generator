# -*- coding: utf-8 -*-
from src.view.dialog.export_dialog import ExportDialog
from src.view.frame.type_mapping.export_type_mapping_dialog_frame import ExportTypeMappingDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 9:50'


class ExportTypeMappingDialog(ExportDialog):

    def get_frame(self) -> ExportTypeMappingDialogFrame:
        return ExportTypeMappingDialogFrame(self.row_ids, self, self.dialog_title)
