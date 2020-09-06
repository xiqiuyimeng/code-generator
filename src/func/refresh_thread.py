# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QThread

from src.constant.constant import TEST_CONN_FAIL_PROMPT
from src.func.connection_function import open_connection
from src.func.open_conn_thread import AsyncOpenConn

_author_ = 'luwt'
_date_ = '2020/8/31 11:38'


class RefreshWorker(QThread):

    # 定义信号，返回结果，第一个参数为是否成功，第二个：成功为返回的查询结果，失败为返回的异常信息
    result = pyqtSignal(bool, object)

    def __init__(self, gui, conn_id, conn_name, opened_child=None, opened_table=None):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.opened_child = opened_child
        self.opened_table = opened_table

    def run(self):
        try:
            self.db_executor = open_connection(self.gui, self.conn_id, self.conn_name)
            data = self.refresh_data()
            self.result.emit(True, data)
        except Exception as e:
            data = f'{TEST_CONN_FAIL_PROMPT}：[{self.conn_name}]' \
                   f'\t\n {e.args[0]} - {e.args[1]}'
            self.result.emit(False, data)

    def refresh_data(self):
        """刷新数据"""
        result_data = dict()
        # 刷新连接下的库列表信息
        dbs = self.db_executor.get_dbs()
        for db in dbs:
            result_data[db] = None
        if self.opened_child:
            opened_db_dict = self.opened_child.get("opened_db")
            opened_dbs = opened_db_dict.keys()
            # 为保证数据真实，以数据库查出的库名与保存的打开库名做交集
            real_opened_dbs = set(dbs) & set(opened_dbs)
            for opened_db in real_opened_dbs:
                self.db_executor.switch_db(opened_db)
                tables = self.db_executor.get_tables()
                table_dict = dict()
                tb_status_dict = opened_db_dict[opened_db]["table"]
                for table in tables:
                    table_dict[table] = tb_status_dict.get(table)
                result_data[opened_db] = {
                    "expanded": opened_db_dict[opened_db]["expanded"],
                    "table": table_dict
                }
                # 如果之前打开的表存在
                if self.opened_table and self.opened_table[1] == opened_db and self.opened_table[2] in tables:
                    cols = self.db_executor.get_cols(opened_db, self.opened_table[2])
        return result_data


class Refresh(QObject):

    refresh_finished = pyqtSignal()

    def __init__(self, gui):
        super().__init__()
        self.gui = gui
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")
        self.icon = self.item.icon(0)

    def refresh(self):
        # 遍历所有刷新前的打开项
        for conn_name, values in self.gui.open_item_dict.items():
            # 将刷新前打开的连接重新打开
            conn_item = self.iterate_tree_root(conn_name)
            refresh_worker = RefreshWorker(self.gui, int(conn_item.text(1)), conn_name, values)
            refresh_worker.result.connect(self.refresh_ui)
            refresh_worker.start()
            # open_conn = AsyncOpenConn(self.gui,
            #                           conn_item,
            #                           int(conn_item.text(1)),
            #                           conn_name,
            #                           expanded=values.get("expanded"))
            # open_conn.connect_db()
            # db_values = values.get("opened_db")
            # if db_values:
            #     open_conn.finished.connect(lambda: self.refresh_db(conn_item, db_values))

    def refresh_ui(self, flag, data):
        """刷新界面"""
        pass

    def refresh_db(self, conn_item, db_values):
        """刷新库，db_values 结构 db_name, expanded"""
        conn_id = int(conn_item.text(1))
        conn_name = conn_item.text(0)
        for db_name, db_value in db_values.items():
            db_item = self.iterate_tree_item(conn_item, db_name)
            open_db = AsyncOpenConn(self.gui,
                                    db_item,
                                    conn_id,
                                    conn_name,
                                    db_name,
                                    expanded=db_value.get("expanded"),
                                    check_status=db_value.get("table"))
            open_db.connect_db()
            if self.gui.opened_table and self.gui.opened_table[0] == conn_name \
                    and self.gui.opened_table[1] == db_name:
                open_db.finished.connect(lambda: self.refresh_table(conn_id, conn_name, db_item))

    def refresh_table(self, conn_id, conn_name, db_item):
        tb_name = self.gui.opened_table[2]
        tb_item = self.iterate_tree_item(db_item, tb_name)
        open_tb = AsyncOpenConn(self.gui, tb_item, conn_id, conn_name, db_item.text(0), tb_name)
        open_tb.connect_db()

    def update_expanded_before_refresh(self):
        """更新下已打开项的展开状态"""
        for conn_name, values in self.gui.open_item_dict.items():
            conn_item = self.iterate_tree_root(conn_name)
            expanded = conn_item.isExpanded()
            self.gui.open_item_dict[conn_name]["expanded"] = expanded
            if values.get("opened_db"):
                for db, db_value in values.get("opened_db").items():
                    db_item = self.iterate_tree_item(conn_item, db)
                    db_value["expanded"] = db_item.isExpanded()
                    db_value["table"] = self.collect_table_check_status(db_item)

    def collect_table_check_status(self, db_item):
        check_status = dict()
        for index in range(db_item.childCount()):
            tb_item = db_item.child(index)
            check_status[tb_item.text(0)] = tb_item.checkState(0)
        return check_status

    def iterate_tree_root(self, conn_name):
        """遍历树节点，返回匹配名字的节点"""
        iterator = QtWidgets.QTreeWidgetItemIterator(self.gui.treeWidget)
        while iterator.value():
            if iterator.value().text(0) == conn_name:
                return iterator.value()
            # 下一个节点
            iterator = iterator.__iadd__(1)

    def iterate_tree_item(self, tree_item, name):
        for index in range(tree_item.childCount()):
            item = tree_item.child(index)
            if item.text(0) == name:
                return item

