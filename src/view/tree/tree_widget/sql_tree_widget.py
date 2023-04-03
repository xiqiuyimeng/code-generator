# -*- coding: utf-8 -*-
"""
sql数据源树结构
"""
from src.constant.tree_constant import LIST_ALL_CONN_BOX_TITLE
from src.service.async_func.async_sql_conn_task import ListConnExecutor
from src.service.system_storage.opened_tree_item_sqlite import SqlTreeItemLevel
from src.service.util.tree_node import TreeData
from src.view.tab.tab_widget.tab_widget import TabWidget
from src.view.tree.tree_item.context import get_sql_tree_node
from src.view.tree.tree_item.sql_tree_node.sql_tree_node_abc import SqlTreeNodeABC
from src.view.tree.tree_widget.tree_widget_abc import TreeWidgetABC
from src.view.tree.tree_widget.tree_function import make_conn_tree_items

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class SqlTreeWidget(TreeWidgetABC):
    """sql数据源树部件"""

    def __init__(self, parent, window):
        super().__init__(parent, window)
        self.main_window = window
        self.list_conn_executor = ...
        # 保存 sql tree 选中数据
        self.tree_data = TreeData()

    def reopen_tree(self):
        # 如果还没初始化过，再执行初始化
        if self.list_conn_executor is Ellipsis:
            self.reopening_flag = True
            # 初始化数据
            self.list_conn_executor = ListConnExecutor(self.reopen_items, self.reopen_tab, self.main_window,
                                                       self.main_window, LIST_ALL_CONN_BOX_TITLE,
                                                       self.reopen_end, self.reopen_end)
            self.list_conn_executor.start()

    def get_current_tab_widget(self) -> TabWidget:
        return self.main_window.sql_tab_widget

    def reopen_items(self, opened_items):
        """
        重新打开树节点
        :param opened_items: 打开记录表中元素
        """
        level = opened_items[0].level
        # 如果是连接，单独处理
        if level == SqlTreeItemLevel.conn_level.value:
            make_conn_tree_items(opened_items, self)
        else:
            # 如果是其他类型，按策略来执行
            self.reopen_tree_item(opened_items)

    def get_item_node(self, item) -> SqlTreeNodeABC:
        return get_sql_tree_node(item, self, self.main_window)
