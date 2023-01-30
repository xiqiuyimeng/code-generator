# -*- coding: utf-8 -*-
from view.tab.tab_bar.tab_bar import TabBar

_author_ = 'luwt'
_date_ = '2022/12/7 12:40'


class StructTabBar(TabBar):

    def partially_checked_table_prompt(self, tab_widget) -> str:
        return f'表：{tab_widget.tree_item.text(0)}'

    def need_change_current(self, current_tab) -> bool:
        # 项目初始化中，或正在打开tab页不处理
        return not self.main_window.struct_tree_widget.reopening_flag \
            and (current_tab
                 and not current_tab.tree_widget.get_item_node(current_tab.tree_item).is_opening)
