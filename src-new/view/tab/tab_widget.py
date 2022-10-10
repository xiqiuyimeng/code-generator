# -*- coding: utf-8 -*-
from queue import Queue

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTabWidget

from view.tab.tab_bar import TabBar

_author_ = 'luwt'
_date_ = '2022/10/9 17:37'


class TabWidget(QTabWidget):

    # 当前至少存在一个tab
    opened_tab_signal = pyqtSignal()
    # 清除所有tab
    clear_tabs_signal = pyqtSignal()

    def __init__(self, parent, main_window):
        super().__init__(parent=parent)
        self.main_window = main_window
        self.tab_bar = TabBar(self)
        self.setTabBar(self.tab_bar)
        # 在启动过程中，暂存tab 列表，方便按排序展示
        self.temp_tab_list = list()
        # 存储tab_id顺序
        self.tab_id_list = list()
        # 临时变量，存储下库中存储的当前tab，仅在启动过程中使用
        self.current = None
        # 维护一个队列，用来持续保存tab页的数据
        self.queue = Queue()
        # self.async_save_manager = AsyncSaveTabObjManager(self.queue,
        #                                                  self.main_window,
        #                                                  SAVE_TAB_DATA)
        # self.async_save_manager.start()

    def read_saved_tab(self, idx):
        """当前页变化时，调用tab的read_saved_tab方法"""
        if idx >= 0:
            tab = self.widget(idx)
            tab_ui = tab.property("tab_ui")
            tab_ui.read_saved_tab()

    def insert_tab_by_order(self):
        # 按order排序
        self.temp_tab_list.sort(key=lambda x: x[0])
        if self.temp_tab_list:
            self.fill_tab_id_list(list(map(lambda x: x[1].property('tab_id'), self.temp_tab_list)))
        [self.addTab(tab[1], tab[2]) for tab in self.temp_tab_list]
        if self.current is not None:
            self.setCurrentIndex(self.current)
            self.read_saved_tab(self.current)
        del self.temp_tab_list
        del self.current
        # 在处理完后，将信号连上
        self.currentChanged.connect(self.read_saved_tab)
        # 当前选项卡指针改变时（选项卡顺序改变时也会触发），修改数据库
        self.currentChanged.connect(self.tab_bar.change_current_order)

    def close(self):
        self.async_save_manager.worker_quit()
        super().close()

    def fill_tab_id_list(self, data):
        # 如果当前还不存在tab，那么这是第一个，发送信号
        if self.count() == 0:
            self.opened_tab_signal.emit()
        if isinstance(data, list):
            self.tab_id_list = data
        else:
            self.tab_id_list.append(data)

    def clear_tab_id_list(self):
        self.clear_tabs_signal.emit()
        self.tab_id_list.clear()

