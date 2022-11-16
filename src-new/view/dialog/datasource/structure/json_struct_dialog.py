# -*- coding: utf-8 -*-
from service.system_storage.struct_type import StructTypeEnum
from view.dialog.datasource import AbstractStructDialog

_author_ = 'luwt'
_date_ = '2022/11/16 12:37'


class JsonStructDialog(AbstractStructDialog):

    def get_struct_type(self):
        return StructTypeEnum.json_type.value
