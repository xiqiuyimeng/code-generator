# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

from src.constant.constant import SELECT_TABLE_FAIL_PROMPT
from src.db.cursor_proxy import get_cols_group_by_table
from src.func.connection_function import open_connection
from src.func.gui_function import set_children_check_state
from src.func.selected_data import SelectedData
from src.func.table_func import check_table_opened, close_table, fill_table, add_table
from src.little_widget.message_box import pop_fail

_author_ = 'luwt'
_date_ = '2020/8/21 10:04'


class SelectTableWorker(QThread):

    # 定义信号，返回测试结果，第一个参数为是否成功，
    # 第二个查询成功时：打开表存在即为表的字段，否则为空，
    # 查询失败为错误提示语
    result = pyqtSignal(bool, object)

    def __init__(self, gui, conn_id, conn_name, db_name, tb_name, opened_table):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_name = tb_name
        self.opened_table = opened_table

    def run(self):
        self.select_table()

    def select_table(self):
        try:
            # 获取要选择的所有数据
            executor = open_connection(self.gui, self.conn_id, self.conn_name)
            cols = executor.get_tb_cols(self.db_name, self.tb_name)
            # tb_cols_dict: {tb: (col_A, col_B),}
            tb_cols_dict = get_cols_group_by_table(cols)
            SelectedData().set_tbs(self.gui, self.conn_name, self.db_name, tb_cols_dict)
            result = None
            if self.opened_table:
                # 查询打开表的字段并发射信号
                result = executor.get_cols(self.db_name, self.opened_table)
            self.result.emit(True, result)
        except Exception as e:
            self.result.emit(False, f'{SELECT_TABLE_FAIL_PROMPT}：[{self.conn_name}]'
                                    f'\t\n {e.args[0]} - {e.args[1]}')


class AsyncSelectTable:

    def __init__(self, gui, item, conn_id, conn_name, db_name, tb_name=None):
        self.item = item
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_name = tb_name
        self.opened_table = self.find_opened_table()
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")
        self.icon = self.item.icon(0)

    def find_opened_table(self):
        """找到打开的表"""
        # 如果是表
        if self.tb_name and check_table_opened(self.gui, self.item):
            return self.tb_name
        # 如果是库
        elif hasattr(self.gui, 'table_frame') and self.gui.current_table.parent() is self.item:
            return self.gui.current_table.text(0)
        else:
            return None

    def select_table(self):
        self._movie.start()
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程，这里需要注意的是，线程需要处理为类成员变量，
        # 如果是方法内的局部变量，在方法自上而下执行完后将被销毁
        self.select_table_thread = SelectTableWorker(self.gui,
                                                     self.conn_id,
                                                     self.conn_name,
                                                     self.db_name,
                                                     self.tb_name,
                                                     self.opened_table)
        self.select_table_thread.result.connect(lambda flag, data: self.handle_show(flag, data))
        self.select_table_thread.start()

    def handle_show(self, flag, data):
        """解析测试连接的结果"""
        self._movie.stop()
        self.item.setIcon(0, self.icon)
        if self.tb_name:
            self.select_one(flag, data)
        else:
            self.select_all(flag, data)

    def select_all(self, flag, data):
        """全选所有表页面效果"""
        if flag:
            # 节点下所有表的复选框置为选择状态
            set_children_check_state(self.item, Qt.Checked)
            # 如果打开了某个表
            if self.opened_table:
                self.rebuild_table(data)
        else:
            pop_fail(SELECT_TABLE_FAIL_PROMPT, data)

    def select_one(self, flag, data):
        """选择一个表页面效果，刷新表格"""
        # 如果成功且表已打开，重新渲染表格，以保持数据真实
        if flag:
            if self.opened_table:
                self.rebuild_table(data)
        # 如果失败
        else:
            # 将当前项改为未选择状态
            self.item.setCheckState(0, Qt.Unchecked)
            pop_fail(SELECT_TABLE_FAIL_PROMPT, data)

    def rebuild_table(self, data):
        """刷新下表格数据"""
        # 关闭表格
        close_table(self.gui)
        # 刷新表格
        selected_cols = list(map(lambda x: x[0], data))
        add_table(self.gui, self.gui.current_table)
        fill_table(self.gui, data, selected_cols)
        # 填充表格时会将单元格复选框勾选，只剩下表头需要单独处理
        self.gui.table_header.set_header_checked(True)
