# -*- coding: utf-8 -*-
"""
处理已选中的表和字段信息，放入一个多重嵌套的字典中。结构如下:
{
    conn_name: {
        db_name: {
            tb_name: [col_A, col_B]
        }
    }
}
第一层字典（连接字典）：存放连接信息，key为连接名称，value为字典。称之为conn_dict
第二层字典（数据库字典）：存放对应连接下的数据库信息，key为数据库名称，value为字典。称之为db_dict
第三层字典（表字典）：存放对应数据库下的表信息，key为表名，value为列表。称之为tb_dict
第四层列表（字段列表）：存放对应表下的字段信息，称之为col_list，如果全选字段，则为元祖类型，否则为列表
"""

from src.db.cursor_proxy import get_cols_group_by_table
from src.func.connection_function import open_connection

_author_ = 'luwt'
_date_ = '2020/7/8 16:45'


def sort_dict(src_dict):
    # 对字典进行排序，得到一个列表，列表元素为元祖，
    # 包含多个元祖，元祖第一个值为key，第二个为value
    sorted_list = sorted(src_dict.items())
    # 对排序后得到的列表进行解压，还原为只有两个元祖，
    # 第一个元祖为keys，第二个为values
    sorted_tuple = list(zip(*sorted_list))
    # 将还原后的元祖拆分为两部分，然后用zip压缩为一个字典
    return dict(zip(sorted_tuple[0], sorted_tuple[1]))


class SelectedData:

    def __new__(cls, *args, **kwargs):
        """以构造器来实现单例"""
        if not hasattr(SelectedData, 'instance'):
            SelectedData.instance = object.__new__(cls)
            # 存放连接信息的字典，key为连接名称，value为字典。为保证唯一，放在构造器中初始化
            SelectedData.instance.conn_dict = dict()
            print('实例化容器')
        return SelectedData.instance

    def unset_conn(self, conn_name):
        """
        删除已选字典中的连接
        :param conn_name: 连接名称
        """
        del self.conn_dict[conn_name]

    def get_db_dict(self, conn_name, allow_none=False):
        """
        从连接字典中取值，key为conn_name，获取对应的db_dict。用以存放数据库与其下表信息，
        若不存在且不允许为空，则初始化一个
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param allow_none: 允许返回空，默认False。由于在删除时，
            可能会导致父结构数据也被清空，故特定情况允许返回空
        """
        if self.conn_dict.get(conn_name) is None and not allow_none:
            self.conn_dict[conn_name] = dict()
        return self.conn_dict.get(conn_name)

    def unset_db(self, gui, conn_name, db_name):
        """
        删除数据库字典中key为db_name的元素
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        """
        db_dict = self.get_db_dict(conn_name)
        del db_dict[db_name]
        # 状态栏信息
        gui.statusbar.showMessage(f"取消选择数据库库{db_name}下所有表")
        # 如果该连接下没有选中值，那么删除连接
        if not self.conn_dict.get(conn_name):
            del self.conn_dict[conn_name]

    def get_tb_dict(self, conn_name, db_name, allow_none=False):
        """
        从数据库字典中取值，key为db_name，获取对应的tb_dict。用以存放表名与其下字段信息，
        若不存在，则初始化一个。若数据库字典不存在，则返回空
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param allow_none: 允许返回空，默认False。由于在删除时，
            可能会导致父结构数据也被清空，故特定情况允许返回空
        """
        db_dict = self.get_db_dict(conn_name, allow_none)
        if db_dict is None:
            return None
        if db_dict.get(db_name) is None:
            if allow_none:
                return None
            else:
                db_dict[db_name] = dict()
        return db_dict.get(db_name)

    def replace_tb_dict(self, conn_name, db_name, tb_dict):
        """
        替换tb_dict
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_dict: 要替换的新tb_dict
        """
        db_dict = self.get_db_dict(conn_name)
        db_dict[db_name] = tb_dict

    def get_col_list(self, conn_name, db_name, tb_name, allow_none=False):
        """
        从表字典中取值，key为tb_name，获取对应的col_list，用以存放指定表下的字段信息，
        若不存在，则初始化一个，若表字典不存在，则返回空
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_name: 表名称，作为key存在于表字典中
        :param allow_none: 允许返回空，默认False。由于在删除时，
            可能会导致父结构数据也被清空，故特定情况允许返回空
        """
        tb_dict = self.get_tb_dict(conn_name, db_name, allow_none)
        if tb_dict is None:
            return None
        if tb_dict.get(tb_name) is None:
            if allow_none:
                return None
            else:
                tb_dict[tb_name] = list()
        return tb_dict.get(tb_name)

    def set_tbs(self, gui, conn_id, conn_name, db_name, tb_names=None):
        """
        批量添加表名称，添加至表字典，key为表名，value为字段列表
        :param gui: 启动的主窗口界面对象
        :param conn_id: 连接id
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_names: 表名称列表，作为key存在于表字典中，若不传则为查询所有
        """
        tb_dict = self.get_tb_dict(conn_name, db_name)
        executor = open_connection(gui, conn_id, conn_name)[1]
        cols = executor.get_tb_cols(db_name, tb_names)
        tb_cols_dict = get_cols_group_by_table(cols)
        tb_dict.update(tb_cols_dict)
        sorted_dict = sort_dict(tb_dict)
        # 将原来的字典替换为排序后的字典
        self.replace_tb_dict(conn_name, db_name, sorted_dict)
        # 状态栏信息
        gui.statusbar.showMessage(f"已选择表：{list(sorted_dict.keys())}")

    def unset_tbs(self, gui, conn_name, db_name, tb_names=None):
        """
        批量删除表名称，从表字典中删除元素，若无指定表名，则清空所有
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_names: 表名称列表，其中元素作为key存在于表字典中
        """
        tb_dict = self.get_tb_dict(conn_name, db_name)
        # 若指定表名，且非所有已选表名，删除表名称，否则应为清空所有
        if tb_names and len(tb_names) != len(tb_dict):
            for tb_name in tb_names:
                del tb_dict[tb_name]
            # 状态栏信息
            gui.statusbar.showMessage(f"取消选择表：{tb_names}")
        else:
            self.unset_db(gui, conn_name, db_name)

    def replace_col_list(self, conn_name, db_name, tb_name, cols):
        """
        将原tb_dict中的列表替换为元祖，替换目的是将此类型作为全选的标识。或将元祖替换为列表
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_name: 表名称，作为key存在于表字典中
        :param cols: 添加的字段名称列表或元祖，作为value存在于表字典中
        """
        tb_dict = self.get_tb_dict(conn_name, db_name)
        tb_dict[tb_name] = cols

    def set_cols(self, gui, conn_name, db_name, tb_name, cols):
        """
        批量添加字段名称，添加至字段列表中
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_name: 表名称，作为key存在于表字典中
        :param cols: 添加的字段名称列表，作为value存在于表字典中
        """
        col_list = self.get_col_list(conn_name, db_name, tb_name)
        if isinstance(col_list, list):
            col_list.extend(cols)
            # 若选中字段个数等于表中总字段数，将列表转为元祖，以此标识全选
            if len(col_list) == len(gui.current_cols):
                col_tuple = tuple(col_list)
                self.replace_col_list(conn_name, db_name, tb_name, col_tuple)
            gui.statusbar.showMessage(f'{tb_name}表已选字段：{col_list}')

    def unset_cols(self, gui, conn_name, db_name, tb_name, cols=None):
        """
        批量删除字段名称，若无指定字典，清空所有
        :param gui: 启动的主窗口界面对象
        :param conn_name: 连接名称，作为key存在于连接字典中
        :param db_name: 数据库名称，作为key存在于数据库字典中
        :param tb_name: 表名称，作为key存在于表字典中
        :param cols: 需要删除的字段名称列表，作为value存在于表字典中
        """
        col_list = self.get_col_list(conn_name, db_name, tb_name, True)
        if col_list:
            # 判断 col_list 类型，如果是tuple，那么需要将其转为list
            if isinstance(col_list, tuple):
                col_list = list(col_list)
                self.replace_col_list(conn_name, db_name, tb_name, col_list)
            # 若指定字段，且非所有已选字段，删除字段，否则应清空所有
            if cols and len(cols) != len(col_list):
                [col_list.remove(col) for col in cols]
                # 状态栏信息
                gui.statusbar.showMessage(f"取消选择字段：{cols}")
            else:
                self.unset_tbs(gui, conn_name, db_name, [tb_name, ])

