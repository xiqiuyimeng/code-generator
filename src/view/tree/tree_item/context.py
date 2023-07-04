# -*- coding: utf-8 -*-
from src.service.system_storage.struct_type import FolderTypeEnum
from src.view.tree.tree_item.sql_tree_node.sql_tree_node_abc import SqlTreeNodeABC
from src.view.tree.tree_item.sql_tree_node.conn_tree_node import ConnTreeNode
from src.view.tree.tree_item.sql_tree_node.db_tree_node import DBTreeNode
from src.view.tree.tree_item.sql_tree_node.table_tree_node import TableTreeNode
from src.view.tree.tree_item.struct_tree_node.struct_tree_node_abc import StructTreeNodeABC
from src.view.tree.tree_item.struct_tree_node.folder_tree_node import FolderTreeNode
from src.view.tree.tree_item.struct_tree_node.struct_tree_node import StructTreeNode
from src.view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/7/6 22:03'


def get_sql_tree_node(item, tree_widget) -> SqlTreeNodeABC:
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
    if hasattr(item, 'tree_node'):
        return item.tree_node
    # 如果父级为空，那么则为连接
    if item.parent() is None:
        return ConnTreeNode(item, tree_widget)
    elif item.parent().parent() is None:
        return DBTreeNode(item, tree_widget)
    elif item.parent().parent().parent() is None:
        return TableTreeNode(item, tree_widget)


def get_struct_tree_node(item, tree_widget) -> StructTreeNodeABC:
    """
    获取结构体树节点对象，结构体树节点分为两种：文件夹节点、结构体节点
    """
    if hasattr(item, 'tree_node'):
        return item.tree_node
    opened_item_record = get_item_opened_record(item)
    # 如果是文件夹，那么返回文件夹节点对象，否则返回结构体节点对象
    if opened_item_record.data_type == FolderTypeEnum.folder_type.value:
        return FolderTreeNode(item, tree_widget)
    else:
        return StructTreeNode(item, tree_widget)
