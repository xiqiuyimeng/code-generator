# -*- coding: utf-8 -*-
from constant.constant import STRUCTURE_CONFIRM_SELECTED_HEADER_TXT
from view.dialog.generator.abstract_generator_dialog import AbstractDisplaySelectedDialog

_author_ = 'luwt'
_date_ = '2022/11/1 10:30'


class StructureConfirmSelectedDialog(AbstractDisplaySelectedDialog):

    def __init__(self, *args):
        super().__init__(*args)

    def get_header_text(self) -> str:
        return STRUCTURE_CONFIRM_SELECTED_HEADER_TXT

    def setup_tree_ui(self): ...
