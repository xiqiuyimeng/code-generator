# -*- coding: utf-8 -*-
from src.service.system_storage.struct_type import StructTypeEnum
from src.view.custom_widget.syntax_highlighter.json_syntax_highlighter import JsonSyntaxHighLighter
from src.view.dialog.datasource.structure import StructDialogABC

_author_ = 'luwt'
_date_ = '2022/11/16 12:37'


class JsonStructDialog(StructDialogABC):

    def get_struct_type(self):
        return StructTypeEnum.json_type.value

    def get_syntax_highlighter(self):
        return JsonSyntaxHighLighter()
