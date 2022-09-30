# -*- coding: utf-8 -*-
from view.tree.tree_item.tree_node_conn.tree_node_conn import ConnTreeNode
from view.tree.tree_item.tree_node_db import DBTreeNode
from view.tree.tree_item.tree_node_table import TableTreeNode

_author_ = 'luwt'
_date_ = '2022/7/6 22:03'


def get_tree_node(item, tree_widget, window):
    """
    获取树节点对应的实例化对象。
    树结构：
        树的根：树的顶层
            连接：第一级，父节点为根
                数据库：第二级，父节点为连接
                    表：第三级，父节点为库
    目前树的根节点为空，所以可以根据这一特性发现当前节点的层级，
    从而返回相应的实例
    """
    # 如果父级为空，那么则为连接
    if item.parent() is None:
        return ConnTreeNode(item, tree_widget, window)
    elif item.parent().parent() is None:
        return DBTreeNode(item, tree_widget, window)
    elif item.parent().parent().parent() is None:
        return TableTreeNode(item, tree_widget, window)


class Context:

    def __init__(self, *args):
        self.tree_node = get_tree_node(*args)

    def open_item(self):
        self.tree_node.open_item()

    def close_item(self):
        self.tree_node.close_item()

    def change_check_box(self, check_state):
        self.tree_node.change_check_box(check_state)

    def do_fill_menu(self, menu):
        self.tree_node.do_fill_menu(menu)

    def handle_menu_func(self, func):
        self.tree_node.handle_menu_func(func)
