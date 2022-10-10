# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QTabBar, QTabWidget, QAction, QMenu

from constant.constant import CLOSE_CURRENT_TAB, CLOSE_OTHER_TABS, CLOSE_ALL_TABS, CLOSE_TABS_TO_THE_LEFT, \
    CLOSE_TABS_TO_THE_RIGHT, SET_CURRENT_INDEX

_author_ = 'luwt'
_date_ = '2022/10/9 17:39'


class TabBar(QTabBar):

    def __init__(self, parent: QTabWidget):
        """tab bar index按照从左到右变大的顺序,0,1,2..."""
        super().__init__(parent=parent)
        self.parent = parent
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
            # 删除其他tab，先删除右边的，再删除左边的
            [self.remove_tab(index + 1) for idx in range(self.count()) if idx > index]
            [self.remove_tab(0) for idx in range(self.count()) if idx < index]
        elif act.text() == CLOSE_ALL_TABS:
            # 删除所有tab
            [self.remove_tab(0) for idx in range(self.count())]
        elif act.text() == CLOSE_TABS_TO_THE_LEFT:
            # 关闭标签页左边所有tab，找到比当前tab索引小的tab个数，按个数删除，删除左边一位即可
            [self.remove_tab(0) for idx in range(self.count()) if idx < index]
        elif act.text() == CLOSE_TABS_TO_THE_RIGHT:
            # 关闭标签页右边所有tab，找到比当前索引大的tab个数，按个数删除，删除右边一位即可
            [self.remove_tab(index + 1) for idx in range(self.count()) if idx > index]
        elif act.text() == SET_CURRENT_INDEX:
            # 当前页置顶
            self.setCurrentIndex(index)

    def remove_tab(self, index):
        tab_id = self.parent.widget(index).property("tab_id")
        # 删除tab
        self.parent.removeTab(index)
        # 删除存储的打开tab记录
        self.parent.async_save_manager.remove_tab(tab_id)

    def change_current_order(self, index):
        """修改is current值和item order"""
        current_widget = self.parent.widget(index)
        if current_widget:
            current_tab_id = current_widget.property("tab_id")
            # 元素是否相等
            tab_id_equal_flag = False
            # 列表大小是否相等
            len_equal_flag = self.parent.count() == len(self.parent.tab_id_list)
            tab_ids = list()
            # order信息保存
            for idx in range(self.parent.count()):
                tab = self.parent.widget(idx)
                tab_id = tab.property("tab_id")
                tab_ids.append(tab_id)
                tab_id_equal_flag = tab_id == self.parent.tab_id_list[idx]
            self.parent.fill_tab_id_list(tab_ids)
            # 如果列表中每一个元素相等，并且大小一致，可以证明两者相同，不需要更新order
            if tab_id_equal_flag and len_equal_flag:
                self.parent.async_save_manager.change_current(current_tab_id, None)
            else:
                self.parent.async_save_manager.change_current(current_tab_id, tab_ids)
        else:
            # 如果是删除，删除到最后一个了，那么清空tab_id_list
            self.parent.clear_tab_id_list()

