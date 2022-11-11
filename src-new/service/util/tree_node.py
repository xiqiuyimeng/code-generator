# -*- coding: utf-8 -*-
from service.system_storage.ds_table_info_sqlite import DsTableInfo
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem

_author_ = 'luwt'
_date_ = '2022/6/3 15:56'


class TreeDataNode:

    def __init__(self, parent):
        self.parent: TreeDataNode = parent
        self.children: dict = dict()
        self.name_text = ...
        self.data = ...
        self.top_level_data = ...
        self.child_type: str = ...


class TreeData:

    # 添加节点数据和删除节点数据都是字典类型，按_keys顺序匹配层次
    _keys = ('conn', 'db', 'tb', 'col')

    def __new__(cls, *args, **kwargs):
        if not hasattr(TreeData, '_instance'):
            TreeData._instance = object.__new__(cls)
            TreeData._instance._root_node = TreeDataNode(None)
            TreeData._instance._root_node.name_text = 'root'
            TreeData._instance._root_node.child_type = TreeData._keys[0]
        return TreeData._instance

    def __bool__(self):
        return bool(self._root_node.children)

    def root_children(self):
        return self._root_node.children

    def iterator(self):
        current_node = self._root_node
        generator = self._iterate_node(current_node)
        while True:
            try:
                yield generator.__next__()
            except StopIteration:
                break

    def _iterate_node(self, node):
        if node.children:
            for value in node.children.values():
                current_node = value
                yield current_node
                yield from self._iterate_node(current_node)

    @staticmethod
    def _get_node(parent_node: TreeDataNode, name):
        if parent_node.children:
            return parent_node.children.get(name)

    def add_node(self, add_data, conn_data):
        """
        添加节点
        :param add_data: 要添加的数据
            1. 添加单列情况
            add_data = {
                'conn': test_conn: OpenedTreeItem,
                'db': test_db: OpenedTreeItem,
                'tb': test_tb: OpenedTreeItem,
                'col': 'test_col',
            }
            2. 添加单表或多个表，不存在同时添加多列情况
            add_data = {
                'conn': test_conn: OpenedTreeItem,
                'db': test_db: OpenedTreeItem,
                'tb': [test_tb1: OpenedTreeItem, test_tb2: OpenedTreeItem] or test_tb1: OpenedTreeItem
            }
        :param conn_data: 连接信息，Connection
        """
        self._do_add_node(add_data, self._root_node, self._keys.__iter__())
        self._add_conn_data(add_data.get(self._keys[0]).item_name, conn_data)

    def _do_add_node(self, add_data: dict, parent_node: TreeDataNode, keys_iter):
        cur_key = keys_iter.__next__()
        parent_node.child_type = cur_key
        # 从添加数据中获取当前级别的名称
        node_data = add_data.get(cur_key)
        if isinstance(node_data, list):
            # 如果是list类型，此时一定是最后一次处理，所以不必获取创建的node
            [self._create_node(parent_node, child_node_data) for child_node_data in node_data]
        else:
            # 如果是单独的元素，直接处理
            node = self._create_node(parent_node, node_data)
            # 结束标志位，当遍历到添加数据的最后一个键，停止
            if cur_key == tuple(add_data.keys())[-1]:
                return
            self._do_add_node(add_data, node, keys_iter)

    def _create_node(self, parent_node, node_data):
        data, node_name = ..., ...
        # 列对象将以 DsTableInfo 对象的形式传入，所以需要将名称和数据分开处理
        if isinstance(node_data, DsTableInfo):
            node_name = node_data.col_name
            data = node_data
        elif isinstance(node_data, OpenedTreeItem):
            node_name = node_data.item_name
            data = node_data
        # 查询node是否存在
        node = self._get_node(parent_node, node_name)
        # 如果node不存在，创建
        if not node:
            node = TreeDataNode(parent_node)
            node.name_text = node_name
            node.data = data
            parent_node.children[node_name] = node
            # 重排序
            parent_node.children = dict(sorted(parent_node.children.items(), key=lambda x: x[1].data.item_order))
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
        node_data = del_data.get(cur_key)
        # 如果是列对象，直接删除
        if isinstance(node_data, DsTableInfo):
            self._remove_node(parent_node, node_data)
        # 如果是多个名称，直接删除
        elif isinstance(node_data, list):
            [self._remove_node(parent_node, child_node) for child_node in node_data
             if self._get_node(parent_node, child_node)]
        elif isinstance(node_data, str):
            # 单个名称，递归操作，找出node
            child_node = self._get_node(parent_node, node_data)
            if not child_node:
                return
            # 如果是删除元素的最后一项，直接进行删除
            if cur_key == tuple(del_data.keys())[-1]:
                self._remove_node(parent_node, node_data)
            else:
                # 如果不是删除元素的最后一项，继续
                if child_node.children:
                    self._do_del_node(del_data, child_node, keys_iter, recursive_del)
                # 如果没有子元素并且指定递归删除，进行删除
                if not child_node.children and recursive_del:
                    self._remove_node(parent_node, node_data)

    @staticmethod
    def _remove_node(parent_node, child_data):
        child_name = child_data
        if isinstance(child_data, DsTableInfo):
            child_name = child_data.col_name
        if parent_node.children.get(child_name):
            del parent_node.children[child_name]

    def _add_conn_data(self, conn_name, data):
        conn_node: TreeDataNode = self._get_node(self._root_node, conn_name)
        if conn_node and conn_node.top_level_data is Ellipsis:
            conn_node.top_level_data = data

    def clear_tree(self):
        self._root_node.children.clear()

    def get_node(self, node_data: dict):
        return self._do_get_node(node_data, self._root_node, self._keys.__iter__())

    def _do_get_node(self, node_data: dict, parent_node: TreeDataNode, keys_iter):
        cur_key = keys_iter.__next__()
        node_name = node_data.get(cur_key)
        if node_name:
            node = self._get_node(parent_node, node_name)
            # 遍历到最后一个结束
            if cur_key == tuple(node_data.keys())[-1]:
                return node
            if node:
                return self._do_get_node(node_data, node, keys_iter)
