# -*- coding: utf-8 -*-
from service.local_storage.conn_sqlite import Connection

_author_ = 'luwt'
_date_ = '2022/6/3 15:56'


class TreeNode:

    def __init__(self, parent):
        self.parent: TreeNode = parent
        self.children: dict = dict()
        self.name_text = None
        self.data = None
        self.child_type: str = ...


class Tree:

    # 添加节点数据和删除节点数据都是字典类型，按_keys顺序匹配层次
    _keys = ('conn', 'db', 'tb', 'col')

    def __new__(cls, *args, **kwargs):
        if not hasattr(Tree, '_instance'):
            Tree._instance = object.__new__(cls)
            Tree._instance._root_node = TreeNode(None)
            Tree._instance._root_node.name_text = 'root'
            Tree._instance._root_node.child_type = Tree._keys[0]
        return Tree._instance

    @staticmethod
    def get_node(parent_node: TreeNode, name):
        if parent_node.children:
            return parent_node.children.get(name)

    def add_node(self, add_data, conn_data):
        """
        添加节点
        :param add_data: 要添加的数据
            1. 添加单列情况
            add_data = {
                'conn': 'test_conn',
                'db': 'test_db',
                'tb': 'test_tb',
                'col': 'test_col',
            }
            2. 添加单表或多个表，不存在同时添加多列情况
            add_data = {
                'conn': 'test_conn',
                'db': 'test_db',
                'tb': ['test_tb1', 'test_tb2', 'test_tb3']  or 'test_tb1'
            }
        :param conn_data: 连接信息，Connection
        """
        self._do_add_node(add_data, self._root_node, self._keys.__iter__())
        self._add_conn_data(add_data.get(self._keys[0]), conn_data)

    def _do_add_node(self, add_data: dict, parent_node: TreeNode, keys_iter):
        cur_key = keys_iter.__next__()
        parent_node.child_type = cur_key
        # 从添加数据中获取当前级别的名称
        name = add_data.get(cur_key)
        if isinstance(name, list):
            # 如果是list类型，此时一定是最后一次处理，所以不必获取创建的node
            [self._create_node(parent_node, child_name) for child_name in name]
        else:
            # 如果是字符串，直接处理
            node = self._create_node(parent_node, name)
            # 结束标志位，当遍历到添加数据的最后一个键，停止
            if cur_key == tuple(add_data.keys())[-1]:
                return
            self._do_add_node(add_data, node, keys_iter)

    def _create_node(self, parent_node, name, data=None):
        # 查询node是否存在
        node = self.get_node(parent_node, name)
        # 如果node不存在，创建
        if not node:
            node = TreeNode(parent_node)
            node.name_text = name
            if data:
                node.data = data
            parent_node.children[name] = node
        return node

    def del_node(self, del_data, recursive_del=True):
        """
        删除节点
        :param del_data: 删除的数据
        :param recursive_del: 是否递归删除
        1. 删除单列的情况
            del_data = {
                'conn': 'test_conn',
                'db': 'test_db',
                'tb': "test_tb",
                'col': 'test_col'
            }
        2. 删除多列情况，一般场景是， 表已经选择了一部分列，再次进行全选，那么需要将之前选中列全部删除，
                并不进行递归删除，保留表，这样视为表全选
            del_data = {
                'conn': 'test_conn',
                'db': 'test_db',
                'tb': "test_tb",
                'col': '['test_col', 'test_col2']
            }
        3. 删除单表或多表
            del_data = {
                'conn': 'test_conn',
                'db': 'test_db',
                'tb': ['test_tb1', 'test_tb2']  or 'test_tb1'
            }
        4. 删除库
            del_data = {
                'conn': 'test_conn',
                'db': ['test_db1', 'test_db2']  or 'test_db'
            }
        5. 删除连接
            del_data = {
                'conn': 'test_conn'
            }
        """
        self._do_del_node(del_data, self._root_node, self._keys.__iter__(), recursive_del)

    def _do_del_node(self, del_data: dict, parent_node, keys_iter, recursive_del=True):
        cur_key = keys_iter.__next__()
        # 找出要删的数据
        node_name = del_data.get(cur_key)
        # 如果是多个名称，直接删除
        if isinstance(node_name, list):
            [self._remove_node(parent_node, child_name) for child_name in node_name
             if self.get_node(parent_node, child_name)]
        elif isinstance(node_name, str):
            # 单个名称，递归操作，找出node
            child_node = self.get_node(parent_node, node_name)
            # 如果是删除元素的最后一项，直接进行删除
            if cur_key == tuple(del_data.keys())[-1]:
                self._remove_node(parent_node, node_name)
            else:
                # 如果不是删除元素的最后一项，继续
                if child_node.children:
                    self._do_del_node(del_data, child_node, keys_iter, recursive_del)
                # 如果没有子元素并且指定递归删除，进行删除
                if not child_node.children and recursive_del:
                    self._remove_node(parent_node, node_name)

    @staticmethod
    def _remove_node(parent_node, child_name):
        del parent_node.children[child_name]

    def _add_conn_data(self, conn_name, data):
        conn_node: TreeNode = self.get_node(self._root_node, conn_name)
        if conn_node and not conn_node.data:
            conn_node.data = data

    def clear_tree(self):
        self._root_node.children.clear()
