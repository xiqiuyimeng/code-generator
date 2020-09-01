# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QObject
from PyQt5.QtGui import QIcon

from src.constant.constant import OPEN_CONN_MENU, TEST_CONN_FAIL_PROMPT
from src.func.connection_function import open_connection
from src.func.selected_data import SelectedData
from src.func.table_func import add_table, fill_table, on_cell_changed
from src.func.tree_function import make_tree_item
from src.little_widget.message_box import pop_fail


_author_ = 'luwt'
_date_ = '2020/8/19 14:20'


class ConnectDBWorker(QThread):

    # 定义信号，返回结果，第一个参数为是否成功，第二个：成功为返回的查询结果，失败为返回的异常信息
    result = pyqtSignal(bool, object)

    def __init__(self, gui, conn_id, conn_name, db_name=None, tb_name=None):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_name = tb_name

    def run(self):
        try:
            self.executor = open_connection(self.gui, self.conn_id, self.conn_name)
            data = self.open_sth()
            self.result.emit(True, data)
        except Exception as e:
            data = f'{TEST_CONN_FAIL_PROMPT}：[{self.conn_name}]' \
                   f'\t\n {e.args[0]} - {e.args[1]}'
            self.result.emit(False, data)

    def open_sth(self):
        # 库名和表名不存在，认为是操作连接
        if self.db_name is None and self.tb_name is None:
            return self.open_conn()
        # 库名存在，表名不存在，认为操作库
        elif self.db_name and self.tb_name is None:
            return self.open_db()
        # 两者都存在，认为操作表
        elif self.db_name and self.tb_name:
            return self.open_tb()

    def open_conn(self):
        return self.executor.get_dbs()

    def open_db(self):
        self.executor.switch_db(self.db_name)
        return self.executor.get_tables()

    def open_tb(self):
        return self.executor.get_cols(self.db_name, self.tb_name)


class AsyncOpenConn(QObject):

    finished = pyqtSignal()

    def __init__(self, gui, item, conn_id, conn_name, db_name=None, tb_name=None, expanded=True):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.item = item
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_name = tb_name
        self.expanded = expanded
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")
        self.icon = self.item.icon(0)

    def connect_db(self):
        self._movie.start()
        # 设置icon
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程，这里需要注意的是，线程需要处理为类成员变量，
        # 如果是方法内的局部变量，在方法自上而下执行完后将被销毁
        self.open_conn_thread = ConnectDBWorker(self.gui,
                                                self.conn_id,
                                                self.conn_name,
                                                self.db_name,
                                                self.tb_name)
        self.open_conn_thread.result.connect(lambda flag, data: self.analyse_result(flag, data))
        self.open_conn_thread.start()

    def analyse_result(self, flag, data):
        """解析读取数据库的结果"""
        self._movie.stop()
        self.item.setIcon(0, self.icon)
        if flag:
            # 库名和表名不存在，认为是操作连接
            if self.db_name is None and self.tb_name is None:
                self.analyse_conn_result(data)
            # 库名存在，表名不存在，认为操作库
            elif self.db_name and self.tb_name is None:
                self.analyse_db_result(data)
            # 两者都存在，认为操作表
            elif self.db_name and self.tb_name:
                self.analyse_tb_result(data)
        else:
            pop_fail(OPEN_CONN_MENU, data)

    def analyse_conn_result(self, data):
        """解析打开连接的结果"""
        icon = QIcon(":icon/database_icon.png")
        for db in data:
            make_tree_item(self.gui, self.item, db, icon)
        self.item.setExpanded(self.expanded)
        self.gui.open_item_dict[self.conn_name] = {"expanded": self.expanded, "opened_db": dict()}
        self.finished.emit()

    def analyse_db_result(self, data):
        icon = QIcon(":icon/table_icon.png")
        for table in data:
            make_tree_item(self.gui, self.item, table, icon, checkbox=Qt.Unchecked)
        self.item.setExpanded(self.expanded)
        opened_db_dict = {self.db_name: {"expanded": self.expanded, "table": dict()}}
        self.gui.open_item_dict[self.conn_name]["opened_db"].update(opened_db_dict)
        self.finished.emit()

    def analyse_tb_result(self, data):
        # 添加表格控件
        add_table(self.gui)
        cols = data
        # 获取选中的字段，如果为空，则未选中，如果选中列表长度等于字段列表长度，那么为全选
        selected_cols = SelectedData().get_col_list(self.conn_name, self.db_name, self.tb_name, True)
        # 当前表复选框的状态，赋予表格中复选框的状态
        fill_table(self.gui, cols, selected_cols, self.tb_name)
        # 如果表格复选框为选中且选中的字段数等于总字段数，那么将表头的复选框也选中，默认表头复选框未选中
        if self.item.checkState(0) == Qt.Checked and len(cols) == len(selected_cols):
            self.gui.table_header.set_header_checked(True)
        # 表格复选框改变事件
        self.gui.tableWidget.cellChanged.connect(lambda row, col: on_cell_changed(self.gui, row, col))
        self.gui.current_table = self.item
        # 状态栏提示
        self.gui.statusbar.showMessage(f"当前展示的表为：{self.item.text(0)}")
        # 设置气泡提示
        self.gui.tableWidget.setToolTip(f'当前表为{self.tb_name}')
        # 已经打开的表，记录下连接名、库名和表名
        self.gui.opened_table = self.conn_name, self.db_name, self.tb_name


