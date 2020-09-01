# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

from src.func.open_conn_thread import AsyncOpenConn

_author_ = 'luwt'
_date_ = '2020/8/31 11:38'


class Refresh:

    def __init__(self, gui):
        self.gui = gui

    def refresh(self):
        # 遍历所有刷新前的打开项
        for conn_name, values in self.gui.open_item_dict.items():
            # 将刷新前打开的连接重新打开
            conn_item = self.iterate_tree_root(conn_name)
            open_conn = AsyncOpenConn(self.gui,
                                      conn_item,
                                      int(conn_item.text(1)),
                                      conn_name,
                                      expanded=values.get("expanded"))
            open_conn.connect_db()
            db_values = values.get("opened_db")
            if db_values:
                open_conn.finished.connect(lambda: self.refresh_db(conn_item, db_values))

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
                                    expanded=db_value.get("expanded"))
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
                    self.gui.open_item_dict[conn_name]["opened_db"]["expanded"] = db_item.isExpanded()

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

