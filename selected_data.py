# -*- coding: utf-8 -*-
import json

_author_ = 'luwt'
_date_ = '2020/7/8 16:45'


class SelectedData:

    def __new__(cls, *args, **kwargs):
        """以构造器来实现单例"""
        if not hasattr(SelectedData, 'instance'):
            SelectedData.instance = object.__new__(cls)
            # 存放数据，字典结构，key为连接名称，value为字典，为保证唯一，放在构造器中初始化
            SelectedData.instance.data = dict()
        return SelectedData.instance

    def get_conn(self, conn_name):
        """
        从data容器中获取key为conn_name的值，该值为字典，用以存放 数据库名 - 字典
        若不存在，则初始化一个
        :param conn_name: 连接名称，作为key存在于data容器字典中
        """
        if self.data.get(conn_name) is None:
            self.data[conn_name] = dict()
        return self.data.get(conn_name)

    def get_db(self, conn_name, db_name):
        """
        从连接字典中获取key为db_name的值，该值为字典，用以存放 表名 - 列表
        若不存在，则初始化一个
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        """
        conn_dict = self.get_conn(conn_name)
        if conn_dict.get(db_name) is None:
            conn_dict[db_name] = dict()
        return conn_dict.get(db_name)

    def unset_db(self, conn_name, db_name):
        """
        删除连接字典中key为db_name的元素
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        """
        conn_dict = self.get_conn(conn_name)
        del conn_dict[db_name]

    def get_tb(self, conn_name, db_name, tb_name):
        """
        从数据库字典中获取key为tb_name的值，该值为列表，用以存放 字段名
        若不存在，则初始化一个
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        :param tb_name: 表名称，作为key存在于数据库字典容器中
        """
        db_dict = self.get_db(conn_name, db_name)
        if db_dict.get(tb_name) is None:
            db_dict[tb_name] = list()
        return db_dict.get(tb_name)

    def set_tbs(self, conn_name, db_name, tb_names):
        """
        批量添加表名称，添加至数据库字典，key为表名，value为空列表
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        :param tb_names: 表名称列表，作为key存在于数据库字典容器中
        """
        db_dict = self.get_db(conn_name, db_name)
        for tb_name in tb_names:
            db_dict[tb_name] = list()
        print(json.dumps(self.data, indent=4))

    def set_cols(self, conn_name, db_name, tb_name, cols):
        """
        批量添加列名称，添加至数据库字典中，key为表名，value为列名列表
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        :param tb_name: 表名称，作为key存在于数据库字典容器中
        :param cols: 列名称列表，作为value存在于数据库字典容器中
        """
        col_list = self.get_tb(conn_name, db_name, tb_name)
        col_list.extend(cols)
        print(json.dumps(self.data, indent=4))

    def unset_tbs(self, conn_name, db_name, tb_names=None):
        """
        批量删除表名称，从数据库字典中删除表名称对应的键值对，若无指定表名，则清空所有
        :param conn_name: 连接名称，作为key存在于data容器字典中
        :param db_name: 数据库名称，作为key存在于连接字典容器中
        :param tb_names: 表名称列表，作为key存在于数据库字典容器中
        """
        db_dict = self.get_db(conn_name, db_name)
        # 若指定表名，且非所有已选表名，删除表名称，否则应为清空所有
        if tb_names and len(tb_names) != len(db_dict):
            for tb_name in tb_names:
                del db_dict[tb_name]
        else:
            self.unset_db(conn_name, db_name)
        print(json.dumps(self.data, indent=4))





