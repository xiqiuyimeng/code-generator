# -*- coding: utf-8 -*-
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon

from src.constant.constant import SELECT_TABLE_FAIL_PROMPT
from src.func.gui_function import set_children_check_state
from src.func.selected_data import SelectedData
from src.func.table_func import change_table_checkbox
from src.little_widget.message_box import pop_fail
from static import image_rc

_author_ = 'luwt'
_date_ = '2020/8/21 10:04'


class SelectTableWorker(QThread):

    # 定义信号，返回测试结果，第一个参数为是否成功，第二个为提示语
    result = pyqtSignal(bool, str)

    def __init__(self, gui, conn_id, conn_name, db_name, tb_names):
        super().__init__()
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_names = tb_names

    def run(self):
        self.select_table()

    def select_table(self):
        try:
            SelectedData().set_tbs(self.gui, self.conn_id, self.conn_name, self.db_name, self.tb_names)
            self.result.emit(True, None)
        except Exception as e:
            self.result.emit(False, f'{SELECT_TABLE_FAIL_PROMPT}：[{self.conn_name}]'
                                    f'\t\n {e.args[0]} - {e.args[1]}')


class AsyncSelectTable:

    def __init__(self, gui, item, conn_id, conn_name, db_name, tb_names=None):
        self.item = item
        self.gui = gui
        self.conn_id = conn_id
        self.conn_name = conn_name
        self.db_name = db_name
        self.tb_names = tb_names
        self._movie = QtGui.QMovie(":/gif/loading_simple.gif")

    def select_table(self):
        self._movie.start()
        self._movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self._movie.currentPixmap())))
        # 创建并启用子线程，这里需要注意的是，线程需要处理为类成员变量，
        # 如果是方法内的局部变量，在方法自上而下执行完后将被销毁
        self.select_table_thread = SelectTableWorker(self.gui, self.conn_id, self.conn_name, self.db_name, self.tb_names)
        self.select_table_thread.result.connect(lambda flag, prompt: self.handle_show(flag, prompt))
        self.select_table_thread.start()

    def handle_show(self, flag, prompt):
        """解析测试连接的结果"""
        self._movie.stop()
        self.item.setIcon(0, QIcon())
        if self.tb_names:
            self.select_one(flag, prompt)
        else:
            self.select_all(flag, prompt)

    def select_all(self, flag, prompt):
        """全选所有表页面效果"""
        if flag:
            set_children_check_state(self.item, Qt.Checked)
            if hasattr(self.gui, 'current_table') and self.gui.current_table.parent() is self.item:
                change_table_checkbox(self.gui, self.gui.current_table, True)
        else:
            pop_fail(SELECT_TABLE_FAIL_PROMPT, prompt)

    def select_one(self, flag, prompt):
        """选择一个表页面效果"""
        if flag:
            change_table_checkbox(self.gui, self.item, True)
        else:
            # 将当前项改为未选择状态
            self.item.setCheckState(0, Qt.Unchecked)
            pop_fail(SELECT_TABLE_FAIL_PROMPT, prompt)
