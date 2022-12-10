# -*- coding: utf-8 -*-
from service.system_storage.ds_table_info_sqlite import DsTableInfo
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem

_author_ = 'luwt'
_date_ = '2022/6/3 15:56'


class TreeDataNode:

    def __init__(self, parent):
        # 记录当前节点的id，唯一标识，取自 data 中的id
        self.node_id: int = ...
        # 父节点
        self.parent: TreeDataNode = parent
        # 下一级元素集合, key: node_id, value: node
        self.children: dict = dict()
        # 当前节点名称
        self.node_name = ...
        # 存放当前节点的数据
        self.data = ...
        # 当前节点级别
        self.item_level: int = ...


class TreeData:

    def __new__(cls, *args, **kwargs):
        if not hasattr(TreeData, '_instance'):
            TreeData._instance = object.__new__(cls)
            TreeData._instance._root_node = TreeDataNode(None)
            TreeData._instance._root_node.node_name = 'root'
            # 根节点级别为0
            TreeData._instance._root_node.item_level = -1
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
    def _get_child_node(parent_node: TreeDataNode, node_id):
        if parent_node.children:
            return parent_node.children.get(node_id)

    def add_node(self, add_data):
        """
        添加节点
        :param add_data: 要添加的数据
            1. 添加单列情况
            add_data = {
                0: test_conn: OpenedTreeItem,
                1: test_db: OpenedTreeItem,
                2: test_tb: OpenedTreeItem,
                3: test_col: DsTableInfo,
            }
            2. 添加多列情况，用于选择整表的时候使用
            add_data = {
                0: test_conn: OpenedTreeItem,
                1: test_db: OpenedTreeItem,
                2: test_tb: OpenedTreeItem,
                3: (test_col1: DsTableInfo, test_col2: DsTableInfo),
            }
            2. 添加单表或多个表，不存在同时添加多列情况
            add_data = {
                0: test_conn: OpenedTreeItem,
                1: test_db: OpenedTreeItem,
                2: [test_tb1: OpenedTreeItem, test_tb2: OpenedTreeItem] or test_tb1: OpenedTreeItem
            }
        """
        self._do_add_node(add_data, self._root_node, self._root_node.item_level + 1)

    def _do_add_node(self, add_data: dict, parent_node: TreeDataNode, item_level):
        # 从添加数据中获取当前级别的数据
        node_data = add_data.get(item_level)
        if isinstance(node_data, (list, tuple)):
            # 如果是list类型，此时一定是最后一次处理，所以不必获取创建的node
            [self._create_node(parent_node, child_node_data) for child_node_data in node_data]
        else:
            # 如果是单独的元素，直接处理
            node = self._create_node(parent_node, node_data)
            # 结束标志位，当遍历到添加数据的最后一个键，停止
            if item_level == max(add_data):
                return
            self._do_add_node(add_data, node, item_level + 1)

    def _create_node(self, parent_node, node_data):
        node_name = ...
        # 列对象将以 DsTableInfo 对象的形式传入，所以需要将名称和数据分开处理
        if isinstance(node_data, DsTableInfo):
            node_name = node_data.col_name
        elif isinstance(node_data, OpenedTreeItem):
            node_name = node_data.item_name
        # 查询node是否存在
        node = self._get_child_node(parent_node, node_data.id)
        # 如果node不存在，创建
        if not node:
            node = TreeDataNode(parent_node)
            node.node_id = node_data.id
            node.node_name = node_name
            node.data = node_data
            node.item_level = parent_node.item_level + 1
            parent_node.children[node_data.id] = node
            # 重排序
            parent_node.children = dict(sorted(parent_node.children.items(),
                                               key=lambda x: x[1].data.item_order))
        return node

    def del_node(self, del_data, recursive_del=True):
        """
        删除节点
        :param del_data: 删除的数据
        :param recursive_del: 是否递归删除
        1. 删除单列的情况
            del_data = {
                0: 1: opened_conn_id,
                1: 23: opened_db_id,
                2: 31: opened_tb_id,
                3: 2: col_id
            }
        2. 删除多列情况，一般场景是， 表已经选择了一部分列，再次进行全选，那么需要将之前选中列全部删除，
                并不进行递归删除，保留表，这样视为表全选
            del_data = {
                0: 1: opened_conn_id,
                1: 23: opened_db_id,
                2: 31: opened_tb_id,
                3: [2: col_id, 3: col_id]
            }
        3. 删除单表或多表
            del_data = {
                0: 1: opened_conn_id,
                1: 23: opened_db_id,
                2: [31: opened_tb_id, 32: opened_tb_id]  or 31: opened_tb_id
            }
        """
        self._do_del_node(del_data, self._root_node, self._root_node.item_level + 1, recursive_del)

    def _do_del_node(self, del_data: dict, parent_node, item_level, recursive_del=True):
        # 找出要删的数据
        node_id = del_data.get(item_level)
        # 找到当前级别的node
        node = self._get_child_node(parent_node, node_id if isinstance(node_id, int) else node_id[0])
        # 如果节点不存在，直接结束
        if not node:
            return

        # 首先，如果当前节点不是最后一级，递归到最后一级，再进行删除逻辑处理
        if item_level < max(del_data):
            self._do_del_node(del_data, node, item_level + 1, recursive_del)

        # 如果当前节点是最后一级，直接删除
        if item_level is max(del_data):
            self._remove_node(parent_node, node_id)
        # 如果当前节点不是最后一级，并且没有子项，也需要递归删除，那么删除节点
        elif not node.children and recursive_del:
            self._remove_node(parent_node, node_id)

    def _remove_node(self, parent_node, node_id):
        # 如果node id是单个id，直接删除，否则视为list，循环删除
        if isinstance(node_id, int):
            self._do_remove_node(parent_node, node_id)
        else:
            [self._do_remove_node(parent_node, single_node_id) for single_node_id in node_id]

    @staticmethod
    def _do_remove_node(parent_node, node_id):
        if parent_node.children.get(node_id):
            del parent_node.children[node_id]

    def clear_tree(self):
        self._root_node.children.clear()

    def clear_node_children(self, node_data: dict):
        node = self.get_node(node_data)
        node.children.clear()

    def get_node(self, node_data: dict):
        return self._do_get_node(node_data, self._root_node, self._root_node.item_level + 1)

    def _do_get_node(self, node_data: dict, parent_node: TreeDataNode, item_level):
        node_id = node_data.get(item_level)
        if node_id:
            node = self._get_child_node(parent_node, node_id)
            # 遍历到最后一个结束
            if item_level == max(node_data):
                return node
            if node:
                return self._do_get_node(node_data, node, item_level + 1)
