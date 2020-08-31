﻿# -*- coding: utf-8 -*-
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
            open_conn = AsyncOpenConn(self.gui, conn_item, int(conn_item.text(1)), conn_name)
            open_conn.connect_db()
            db_values = values[0]
            if db_values:
                open_conn.finished.connect(lambda: self.refresh_db(conn_item, db_values))

    def refresh_db(self, conn_item, db_values):
        """刷新库，db_values 结构 db_name, expanded"""
        for db_value in db_values:
            db_item = self.iterate_conn_item(conn_item, db_value[0])
            open_db = AsyncOpenConn(self.gui,
                                    db_item,
                                    int(conn_item.text(1)),
                                    conn_item.text(0),
                                    db_value[0],
                                    expanded=db_value[1])
            open_db.connect_db()

    def refresh_table(self):
        pass

    def iterate_tree_root(self, conn_name):
        """遍历树节点，返回匹配名字的节点"""
        iterator = QtWidgets.QTreeWidgetItemIterator(self.gui.treeWidget)
        while iterator.value():
            if iterator.value().text(0) == conn_name:
                return iterator.value()
            # 下一个节点
            iterator = iterator.__iadd__(1)

    def iterate_conn_item(self, conn_item, db_name):
        for index in range(conn_item.childCount()):
            db_item = conn_item.child(index)
            if db_item.text(0) == db_name:
                return db_item

