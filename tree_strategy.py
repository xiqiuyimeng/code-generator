# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
_author_ = 'luwt'
_date_ = '2020/6/23 16:21'


def tree_node_factory(item):
    # 如果父级为空，那么则为连接
    if item.parent() is None:
        return TreeNodeConn()
    elif item.parent().parent() is None:
        return TreeNodeDB()
    elif item.parent().parent().parent() is None:
        return TreeNodeTable()


class Context:

    def __init__(self, tree_node):
        self.tree_node = tree_node

    def open_item(self):
        return self.tree_node.open_item()


class TreeNodeAbstract(ABC):

    @abstractmethod
    def open_item(self, item):
        pass


class TreeNodeConn(TreeNodeAbstract):

    def open_item(self, item):
        # 仅当子元素不存在时，获取子元素并填充
        if item.childCount() == 0:
            # 连接的id，存在于元素的第一列
            conn_id = int(item.text(1))
            dbs = self.get_conn(conn_id).get_dbs()
            for db in dbs:
                self.make_tree_item(item, db)


class TreeNodeDB(TreeNodeAbstract):

    def open_item(self):
        pass


class TreeNodeTable(TreeNodeAbstract):

    def open_item(self):
        pass

