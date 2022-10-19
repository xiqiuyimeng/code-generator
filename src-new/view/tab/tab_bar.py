# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QObject, QEvent, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTabBar, QTabWidget, QAction, QMenu

from constant.constant import CLOSE_CURRENT_TAB, CLOSE_OTHER_TABS, CLOSE_ALL_TABS, CLOSE_TABS_TO_THE_LEFT, \
    CLOSE_TABS_TO_THE_RIGHT, SET_CURRENT_INDEX, TABLE_CLOSE_WITH_PARTIALLY_CHECKED, CLOSE_TABLE_MENU
from service.system_storage.ds_table_tab_sqlite import DsTableTab
from view.box.message_box import pop_fail
from view.tree.tree_widget.tree_item_func import set_item_opened_tab, get_item_opening_flag

_author_ = 'luwt'
_date_ = '2022/10/9 17:39'


class TabBar(QTabBar):

    remove_tab_signal = pyqtSignal(DsTableTab)

    def __init__(self, parent: QTabWidget, main_window):
        """tab bar index按照从左到右变大的顺序,0,1,2..."""
        super().__init__(parent=parent)
        self.parent = parent
        self.main_window = main_window
        self.is_moving = False
        self.current_changed = False
        # tab_bar在tab页过多时，开启滚动按钮
        self.setUsesScrollButtons(True)
        # 选项卡增加关闭按钮
        self.setTabsClosable(True)
        # 设置标签可拖拽改变顺序
        self.setMovable(True)
        # 监听自身，tab bar事件
        self.installEventFilter(self)
        # tab bar右击菜单功能
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click_menu)
        # 关闭选项卡事件
        self.tabCloseRequested.connect(self.remove_tab)

    def mousePressEvent(self, event):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.LeftButton:
            self.is_moving = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "is_moving"):
            # 鼠标按键松开，恢复标志位
            self.is_moving = False
            self.sort_tab()
        super().mouseReleaseEvent(event)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # 当事件的对象是tab bar时，并且是气泡提示事件
        if obj == self and event.type() == QEvent.ToolTip:
            # 获取鼠标停留的tab索引
            index = self.tabAt(event.pos())
            # 获取当前tab页
            current_tab = self.parent.widget(index)
            # 设置气泡提示
            self.setTabToolTip(index, current_tab.toolTip())
        return super().eventFilter(obj, event)

    def right_click_menu(self, pos):
        """tab bar弹出右键菜单"""
        index = self.tabAt(pos)
        menu_names = [CLOSE_CURRENT_TAB, CLOSE_OTHER_TABS, CLOSE_ALL_TABS,
                      CLOSE_TABS_TO_THE_LEFT, CLOSE_TABS_TO_THE_RIGHT, SET_CURRENT_INDEX]
        menu = QMenu()
        [menu.addAction(QAction(option, menu)) for option in menu_names]
        # 右键菜单点击事件
        menu.triggered.connect(lambda action: self.handle_menu_func(action, index))
        # 右键菜单弹出位置跟随焦点位置
        menu.exec_(QCursor.pos())

    def handle_menu_func(self, act: QAction, index):
        """tab bar右键菜单功能实现，需要注意的是，删除tab后，索引也会刷新"""
        if act.text() == CLOSE_CURRENT_TAB:
            # 删除当前tab
            self.remove_tab(index)
        elif act.text() == CLOSE_OTHER_TABS:
            # 删除其他tab，先删除右边的
            for idx in range(self.count()):
                if idx > index:
                    if not self.remove_tab(index + 1):
                        break
            # 再删除左边的
            for idx in range(self.count()):
                if idx < index:
                    if not self.remove_tab(0):
                        break
        elif act.text() == CLOSE_ALL_TABS:
            # 删除所有tab
            while self.count():
                if not self.remove_tab(0):
                    break
        elif act.text() == CLOSE_TABS_TO_THE_LEFT:
            # 关闭标签页左边所有tab，找到比当前tab索引小的tab个数，按个数删除，删除左边一位即可
            for idx in range(self.count()):
                if idx < index:
                    if not self.remove_tab(0):
                        break
        elif act.text() == CLOSE_TABS_TO_THE_RIGHT:
            # 关闭标签页右边所有tab，找到比当前索引大的tab个数，按个数删除，删除右边一位即可
            for idx in range(self.count()):
                if idx > index:
                    if not self.remove_tab(index + 1):
                        break
        elif act.text() == SET_CURRENT_INDEX:
            # 当前页置顶
            self.setCurrentIndex(index)

    def remove_tab(self, index):
        # 获取tab table
        tab_widget = self.parent.widget(index)
        # 如果当前复选框的状态未部分选中，则关闭将不可用，因为关闭后，无法获取部分选中的具体列
        if tab_widget.tree_item.checkState(0) == Qt.PartiallyChecked:
            pop_fail(TABLE_CLOSE_WITH_PARTIALLY_CHECKED.format(tab_widget.tree_item.parent().parent().text(0),
                                                               tab_widget.tree_item.parent().text(0),
                                                               tab_widget.tree_item.text(0)),
                     CLOSE_TABLE_MENU.format(tab_widget.tree_item.text(0)), self.main_window)
            return False
        # 删除tab widget在树节点中的引用
        set_item_opened_tab(tab_widget.tree_item, None)
        # 删除tab
        self.parent.removeTab(index)
        table_tab = tab_widget.table_tab
        self.remove_tab_signal.emit(table_tab)
        return True

    def change_current(self, index):
        # 获取当前项
        current_tab = self.parent.widget(index)
        # 项目初始化中，或正在打开tab页不处理
        if self.parent.main_window.sql_tree_widget.reopening_flag or \
                (current_tab and get_item_opening_flag(current_tab.tree_item)):
            return
        if current_tab:
            # 考虑处理tab顺序问题
            if self.is_moving:
                # 设置标志位，方便排序时判断使用
                self.current_changed = True
            self.parent.async_save_executor.change_current(current_tab.table_tab)

    def sort_tab(self):
        """在拖拉tab页签，松开鼠标时触发，对最终状态的tab widget进行排序并保存"""
        if self.current_changed:
            tab_table_list = list()
            current_index = self.parent.currentIndex()
            # 首先收集现在的tab list，收集顺序及是否当前，全量更新tab
            for i in range(self.count()):
                table_tab = self.parent.widget(i).table_tab
                table_tab.tab_order = i + 1
                if current_index == i:
                    table_tab.is_current = table_tab.set_current()
                else:
                    table_tab.is_current = table_tab.set_not_current()
                tab_table_list.append(table_tab)
            # 保存数据
            if tab_table_list:
                self.parent.async_save_executor.sort_order(tab_table_list)
            # 重置标志位
            self.current_changed = False

