# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTabWidget

from service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from view.tab.tab_bar.sql_tab_bar import SqlTabBar
from view.tab.tab_bar.struct_tab_bar import StructTabBar
from view.tab.tab_bar.tab_bar import TabBar

_author_ = 'luwt'
_date_ = '2022/10/9 17:37'


class TabWidget(QTabWidget):

    def __init__(self, parent, main_window):
        super().__init__(parent=parent)
        self.main_window = main_window
        self.tab_bar = self.get_tab_bar(main_window)
        self.setTabBar(self.tab_bar)

        self.async_save_executor = AsyncSaveTabObjExecutor()
        self.connect_signal()

        self.async_save_executor.start()

    def get_current_widget(self):
        return self.currentWidget()

    def get_tab_bar(self, window) -> TabBar: ...

    def connect_signal(self):
        # 删除tab页信号
        self.tab_bar.remove_tab_signal.connect(self.async_save_executor.remove_tab)
        # 当前项变化信号
        self.currentChanged.connect(self.tab_bar.change_current)


class SqlTabWidget(TabWidget):

    def get_tab_bar(self, window) -> TabBar:
        return SqlTabBar(self, window)


class StructTabWidget(TabWidget):

    def get_tab_bar(self, window) -> TabBar:
        return StructTabBar(self, window)

