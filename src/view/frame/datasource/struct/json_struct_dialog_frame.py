# -*- coding: utf-8 -*-
from src.enum.struct_type_enum import StructTypeEnum, StructType
from src.view.custom_widget.syntax_highlighter.json_syntax_highlighter import JsonSyntaxHighLighter
from src.view.frame.datasource.struct.struct_dialog_frame_abc import StructDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/3 14:09'


class JsonStructDialogFrame(StructDialogFrameABC):
    """json结构体对话框框架"""

    def get_struct_type(self) -> StructType:
        return StructTypeEnum.json_type.value

    def get_syntax_highlighter(self):
        return JsonSyntaxHighLighter()
