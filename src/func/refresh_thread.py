# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QObject, pyqtSignal, QThread, Qt
from PyQt5.QtGui import QIcon

from src.constant_.constant import TEST_CONN_FAIL_PROMPT, OPEN_CONN_MENU
from src.func.connection_function import open_connection
from src.func.selected_data import SelectedData
from src.func.table_func import add_table, fill_table
from src.func.tree_function import make_tree_item
from src.little_widget.message_box import pop_fail

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
            data = f'{TEST_CONN_FAIL_PROMPT}：[{self.conn_name}]\t\n {e}'
            self.result.emit(False, data)

    def refresh_data(self):
        """
        刷新数据
        :return result_data: 返回字典，字典三层结构
            {
                db_name: None,
                db_name2: {
                    'expanded': True,
                    'table': {
                        table_name: checkState
                    },
                    'opened_table': {
                        'table': table_name,
                        'cols': col_names
                    }
                }
            }
            将当前连接下打开的库、表信息刷新并返回
        """
        # 刷新连接下的库列表信息
        dbs = self.db_executor.get_dbs()
        # 初始化当前连接下刷新的数据字典，{库名：None}
        result_data = dict(zip(dbs, [None] * len(dbs)))
        if self.opened_child:
            opened_db_dict = self.opened_child.get("opened_db")
            opened_dbs = opened_db_dict.keys()
            # 为保证数据真实，以数据库查出的库名与保存的打开库名做交集
            real_opened_dbs = set(dbs) & set(opened_dbs)
            # 已经不存在的库
            non_exists_dbs = set(opened_dbs) - set(dbs)
            # 删除选中字段中不存在的库
            unset_db = lambda db: SelectedData().unset_db(self.gui, self.conn_name, db)
            [unset_db(db) for db in non_exists_dbs if non_exists_dbs]
            # 刷新库
            [self.refresh_db(opened_db, opened_db_dict, result_data) for opened_db in real_opened_dbs]
        return result_data

    def refresh_db(self, db, opened_db_dict, result_data):
        """刷新库"""
        self.db_executor.switch_db(db)
        tables = self.db_executor.get_tables()
        table_dict = dict()
        tb_status_dict = opened_db_dict[db]["table"]
        # 找到不存在的表
        non_exists_tables = set(tb_status_dict.keys()) - set(tables)
        # 删除选中字段中不存在的表
        unset_tb = lambda table: SelectedData().unset_tbs(self.gui, self.conn_name, db, table)
        [unset_tb(table) for table in non_exists_tables if non_exists_tables]
        # 刷新表
        for table in tables:
            table_dict[table] = tb_status_dict.get(table, Qt.Unchecked)
        result_data[db] = {
            "expanded": opened_db_dict[db]["expanded"],
            "table": table_dict
        }
        self.refresh_table(db, tables, result_data)

    def refresh_table(self, db, tables, result_data):
        """如果之前打开的表存在就刷新表"""
        if self.opened_table and self.opened_table[1] == db and self.opened_table[2] in tables:
            cols = self.db_executor.get_cols(db, self.opened_table[2])
            result_data[db]['opened_table'] = {
                'table': self.opened_table[2],
                'cols': cols
            }


class RefreshConnection(QObject):
    refresh_conn_finished = pyqtSignal()

    def __init__(self, gui, conn_item, movie, expanded, opened_child=None, opened_table=None):
        super().__init__()
        self.gui = gui
        self.conn_item = conn_item
        self.conn_id = int(self.conn_item.text(1))
        self.conn_name = self.conn_item.text(0)
        self.movie = movie
        self.expanded = expanded
        self.opened_child = opened_child
        self.opened_table = opened_table
        # 记录下原始icon
        self.conn_icon = self.conn_item.icon(0)

    def refresh_data(self):
        self.movie.start()
        # 设置icon
        self.movie.frameChanged.connect(lambda: self.conn_item.setIcon(0, QIcon(self.movie.currentPixmap())))
        self.refresh_worker = RefreshWorker(self.gui,
                                            self.conn_id,
                                            self.conn_name,
                                            self.opened_child,
                                            self.opened_table)
        self.refresh_worker.result.connect(lambda flag, data: self.refresh_ui(flag, data))
        self.refresh_worker.start()

    def refresh_ui(self, flag, data):
        """刷新界面"""
        self.movie.stop()
        self.conn_item.setIcon(0, self.conn_icon)
        if flag:
            self.reopen_conn(data)
        else:
            pop_fail(OPEN_CONN_MENU, data)
        self.refresh_conn_finished.emit()

    def reopen_conn(self, db_dict):
        """
        打开连接
        :param db_dict: {
                db_name: None,
                db_name2: {
                    'expanded': True,
                    'table': {
                        table_name: checkState
                    },
                    'opened_table': {
                        'table': table_name,
                        'cols': col_names
                    }
                }
            }
        """
        icon = QIcon(":icon/database_icon.png")
        for db_name, db_value in db_dict.items():
            db_item = make_tree_item(self.gui, self.conn_item, db_name, icon)
            if db_value:
                self.reopen_db(db_item, db_value.get("table"))
                # 库节点设置展开状态为刷新前的
                db_item.setExpanded(db_value.get("expanded"))
                # 打开表
                if db_value.get("opened_table"):
                    self.reopen_table(db_item, db_value.get("opened_table"))
        # 连接节点设置展开状态为刷新前的
        self.conn_item.setExpanded(self.expanded)

    def reopen_db(self, db_item, table_dict):
        """
        打开数据库
        :param db_item: 代表库的树节点
        :param table_dict: {
                        table_name: checkState
                    }
        """
        icon = QIcon(":icon/table_icon.png")
        for table_name, checkState in table_dict.items():
            make_tree_item(self.gui, db_item, table_name, icon, checkbox=checkState)

    def reopen_table(self, db_item, opened_table_dict):
        """
        :param db_item: 代表库的树节点
        :param opened_table_dict: {
                        'table': table_name,
                        'cols': col_names
                    }
        """
        # 添加表格控件
        table_name = opened_table_dict.get('table')
        cols = opened_table_dict.get('cols')
        db_name = db_item.text(0)
        table_item = Refresh.iterate_tree_item(db_item, table_name)
        # 添加表格控件
        add_table(self.gui, table_item)
        # 获取选中的字段，如果为空，则未选中，如果选中列表长度等于字段列表长度，那么为全选
        selected_cols = SelectedData().get_col_list(self.conn_name, db_name, table_name, True)
        # 填充表格，当前表复选框的状态，赋予表格中复选框的状态
        fill_table(self.gui, cols, selected_cols)
        # 如果表格复选框为选中且选中的字段数等于总字段数，那么将表头的复选框也选中，默认表头复选框未选中
        if table_item.checkState(0) == Qt.Checked and len(cols) == len(selected_cols):
            self.gui.table_header.set_header_checked(True)


class Refresh(QObject):
    refresh_finished = pyqtSignal()

    def __init__(self, gui, opened_table=None):
        super().__init__()
        self.gui = gui
        self.opened_table = opened_table
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")
        self.finish_count = 0

    def refresh_data(self):
        """刷新界面"""
        # 遍历所有刷新前的打开项
        for conn_name, values in self.gui.open_item_dict.items():
            # 将刷新前打开的连接重新打开
            conn_item = self.iterate_tree_root(conn_name)
            expanded = values.get("expanded")
            if self.opened_table and self.opened_table[0] == conn_name:
                refresh_connection = RefreshConnection(self.gui,
                                                       conn_item,
                                                       self._movie,
                                                       expanded,
                                                       values,
                                                       self.opened_table)
            else:
                refresh_connection = RefreshConnection(self.gui,
                                                       conn_item,
                                                       self._movie,
                                                       expanded,
                                                       values)
            refresh_connection.refresh_conn_finished.connect(lambda: self.refresh_finish())
            refresh_connection.refresh_data()

    def refresh_finish(self):
        """当所有连接都完成，发送完成信号"""
        self.finish_count += 1
        if self.finish_count == len(self.gui.open_item_dict):
            self.refresh_finished.emit()

    def collect_data_before_refresh(self):
        """收集下刷新前页面打开元素的状态，填充gui.open_item_dict"""
        open_dict = self.gui.open_item_dict
        iterator = QtWidgets.QTreeWidgetItemIterator(self.gui.treeWidget)
        # 遍历连接，找到打开项
        while iterator.value():
            conn_item = iterator.value()
            if conn_item.childCount() > 0 and not iterator.value().parent():
                open_dict[conn_item.text(0)] = {
                    'expanded': conn_item.isExpanded()
                }
                open_dict[conn_item.text(0)]['opened_db'] = dict()
                # 遍历库，找到打开项
                for index in range(conn_item.childCount()):
                    db_item = conn_item.child(index)
                    # 如果库打开了，再填充
                    if db_item.childCount() > 0:
                        open_dict[conn_item.text(0)]['opened_db'][db_item.text(0)] = {
                            'table': self.collect_table_check_status(db_item),
                            'expanded': db_item.isExpanded()
                        }
            iterator = iterator.__iadd__(1)

    @staticmethod
    def collect_table_check_status(db_item):
        check_status = dict()
        for index in range(db_item.childCount()):
            tb_item = db_item.child(index)
            check_status[tb_item.text(0)] = tb_item.checkState(0)
        return check_status

    def iterate_tree_root(self, conn_name):
        """遍历树节点，返回匹配名字的节点"""
        iterator = QtWidgets.QTreeWidgetItemIterator(self.gui.treeWidget)
        while iterator.value():
            if iterator.value().text(0) == conn_name and not iterator.value().parent():
                return iterator.value()
            # 下一个节点
            iterator = iterator.__iadd__(1)

    @staticmethod
    def iterate_tree_item(tree_item, name):
        for index in range(tree_item.childCount()):
            item = tree_item.child(index)
            if item.text(0) == name:
                return item
