# -*- coding: utf-8 -*-
from src.enum.ds_category_enum import DsCategoryEnum
from src.service.sql_ds_executor import *
from src.service.system_storage.conn_sqlite import ConnSqlite
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItem
from src.service.system_storage.struct_sqlite import StructSqlite
from src.service.util.struct_util import *

_author_ = 'luwt'
_date_ = '2023/5/4 11:02'


def convert_intact_table_cols(selected_data, type_mapping_dict):
    """
    转转完整的表格列数据，如果选中的数据中存在列信息，直接使用；否则实时获取最新列数据
    """
    # 取第一个节点，判断数据类型是sql类型还是结构体类型
    root_children = selected_data.root_children()
    first_node = tuple(root_children.values())[0]
    table_col_dict_list = list()
    if first_node.data.ds_category == DsCategoryEnum.sql_ds_category.get_name():
        CollectSqlTableCol(table_col_dict_list, type_mapping_dict).collect_table_cols(root_children)
    elif first_node.data.ds_category == DsCategoryEnum.struct_ds_category.get_name():
        CollectStructTableCol(table_col_dict_list, type_mapping_dict).collect_table_cols(root_children)
    return table_col_dict_list


class CollectTableColABC:

    def __init__(self, table_col_dict_list: list, type_mapping_dict):
        self.table_col_dict_list = table_col_dict_list
        self.type_mapping_dict = type_mapping_dict

    def collect_table_cols(self, data_children: dict):
        for node in data_children.values():
            # 判断是否存在子元素，如果存在子元素且子元素是树节点，继续递归处理，否则开始收集数据
            if node.children:
                if isinstance(tuple(node.children.values())[0].data, OpenedTreeItem):
                    self.collect_table_cols(node.children)
                else:
                    # 列信息
                    col_list = [col.data for col in node.children.values()]
                    self.collect_table_col_dict(node, col_list)
            else:
                # 没有子节点，那么需要动态获取
                col_list = self.get_table_cols(node)
                self.collect_table_col_dict(node, col_list)

    def collect_table_col_dict(self, node, col_list):
        # 表名
        table_name = node.node_name
        # 表注释
        table_comment = self.get_table_comment()
        self.table_col_dict_list.append({
            'table_name': table_name,
            'table_comment': table_comment,
            'cols': self.convert_to_dict(col_list)
        })

    def convert_to_dict(self, col_list):
        col_dict_list = list()
        for col in col_list:
            col_dict = dict()
            col_dict['name'] = col.col_name
            col_dict['data_type'] = col.data_type
            col_dict['full_data_type'] = col.full_data_type
            # 将映射类型放入字典中
            type_mapping_group_dict = self.type_mapping_dict.get(col.data_type)
            if type_mapping_group_dict:
                for mapping_col_name, type_mapping in type_mapping_group_dict.items():
                    col_dict[mapping_col_name] = {
                        'mapping_type': type_mapping.mapping_type,
                        'import_desc': type_mapping.import_desc
                    }
            col_dict['comment'] = col.col_comment
            col_dict['is_pk'] = bool(col.is_pk)
            col_dict['col_type'] = col.col_type
            if col.children:
                # 递归处理
                col_dict['children'] = self.convert_to_dict(col.children)
            col_dict_list.append(col_dict)
        return col_dict_list

    def get_table_cols(self, table_node) -> tuple:
        ...

    def get_table_comment(self) -> str:
        ...


class CollectSqlTableCol(CollectTableColABC):

    def __init__(self, *args):
        # 读取连接信息的类
        self.conn_sqlite: ConnSqlite = ...
        # 数据库连接dict
        self.sql_db_executor_dict: dict = ...
        super().__init__(*args)

    def get_table_cols(self, table_node) -> tuple:
        conn_node = table_node.parent.parent
        sql_db_executor = self.get_sql_db_executor(conn_node)
        return sql_db_executor.open_tb(table_node.parent.node_name, table_node.node_name)

    def get_sql_db_executor(self, conn_node):
        conn_id = conn_node.data.parent_id
        if self.sql_db_executor_dict is Ellipsis:
            self.sql_db_executor_dict = dict()
        # 首先尝试获取执行器，如果获取失败，再进行创建
        sql_db_executor = self.sql_db_executor_dict.get(conn_id)
        if not sql_db_executor:
            if self.conn_sqlite is Ellipsis:
                self.conn_sqlite = ConnSqlite()
            # 读取连接信息
            conn_info = self.conn_sqlite.get_conn_by_id(conn_id)
            # 创建连接执行器
            sql_db_executor: SqlDBExecutor = globals()[conn_node.data.data_type.db_executor](conn_info)
            # 放入字典中，缓存等待下次使用
            self.sql_db_executor_dict[conn_id] = sql_db_executor
        return sql_db_executor

    def get_table_comment(self) -> str:
        ...


class CollectStructTableCol(CollectTableColABC):

    def __init__(self, *args):
        # 读取结构体信息的类
        self.struct_sqlite: StructSqlite = ...
        super().__init__(*args)

    def get_table_cols(self, table_node) -> tuple:
        if self.struct_sqlite is Ellipsis:
            self.struct_sqlite = StructSqlite()
        struct_info = self.struct_sqlite.get_struct_info(table_node.node_id)
        struct_parser: StructParser = globals()[table_node.data.data_type.parse_executor](struct_info.content)
        return struct_parser.parse()
