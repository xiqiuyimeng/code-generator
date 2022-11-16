# -*- coding: utf-8 -*-
from view.tree.tree_widget.abstract_tree_widget import AbstractTreeWidget

_author_ = 'luwt'
_date_ = '2022/9/15 17:10'


class StructureTreeWidget(AbstractTreeWidget):
    """结构体数据源树结构"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        # 存储结构体名称和id
        self.struct_name_id_dict: dict = dict()
