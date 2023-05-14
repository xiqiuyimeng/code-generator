# -*- coding: utf-8 -*-
from src.view.dialog.export_dialog import ExportDialog
from src.view.frame.template.export_template_dialog_frame import ExportTemplateDialogFrame

_author_ = 'luwt'
_date_ = '2023/5/14 18:34'


class ExportTemplateDialog(ExportDialog):

    def get_frame(self) -> ExportTemplateDialogFrame:
        return ExportTemplateDialogFrame(self.row_ids, self, self.dialog_title)
