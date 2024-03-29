# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt, QObject, QEvent, pyqtSignal, QPoint
from PyQt6.QtGui import QCursor, QAction
from PyQt6.QtWidgets import QTabBar, QTabWidget, QMenu, QToolTip

from src.constant.tab_constant import CLOSE_CURRENT_TAB, CLOSE_OTHER_TABS, CLOSE_ALL_TABS, CLOSE_TABS_TO_THE_LEFT, \
    CLOSE_TABS_TO_THE_RIGHT, SET_CURRENT_INDEX, TABLE_CLOSE_WITH_PARTIALLY_CHECKED, TABLE_CLOSE_WITH_REFRESHING, \
    RIGHT_CLICK_MENU_NAMES
from src.constant.tree_constant import CLOSE_TABLE_BOX_TITLE
from src.service.system_storage.ds_table_tab_sqlite import DsTableTab
from src.view.box.message_box import pop_fail
from src.view.tree.tree_item.tree_item_func import set_item_opened_tab
from src.view.window.main_window_func import get_window

_author_ = 'luwt'
_date_ = '2022/10/9 17:39'


class TabBarABC(QTabBar):

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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click_menu)
        # 关闭选项卡事件
        self.tabCloseRequested.connect(self.close_current_tab)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        # 当事件的对象是tab bar时，并且是气泡提示事件
        if obj == self and event.type() == QEvent.Type.ToolTip:
            # 获取鼠标停留的tab索引
            index = self.tabAt(event.pos())
            # 获取当前tab页
            current_tab = self.parent.widget(index)
            # 设置气泡提示，向下略微偏移一些，以免鼠标挡住提示文字
            QToolTip.showText(QPoint(event.globalPos().x() + 5, event.globalPos().y() + 10),
                              current_tab.toolTip())
            return True
        return super().eventFilter(obj, event)

    def right_click_menu(self, pos):
        """tab bar弹出右键菜单"""
        index = self.tabAt(pos)
        menu = QMenu()
        for option in RIGHT_CLICK_MENU_NAMES:
            menu.addAction(QAction(option, menu))
        # 右键菜单点击事件
        menu.triggered.connect(lambda action: self.handle_menu_func(action, index))
        # 右键菜单弹出位置跟随焦点位置
        menu.exec(QCursor.pos())

    def handle_menu_func(self, act: QAction, index):
        """tab bar右键菜单功能实现，需要注意的是，删除tab后，索引也会刷新"""
        if act.text() == CLOSE_CURRENT_TAB:
            self.close_current_tab(index)
        elif act.text() == CLOSE_OTHER_TABS:
            self.close_other_tabs(index)
        elif act.text() == CLOSE_ALL_TABS:
            self.close_all_tabs()
        elif act.text() == CLOSE_TABS_TO_THE_LEFT:
            self.close_tabs_to_left(index)
        elif act.text() == CLOSE_TABS_TO_THE_RIGHT:
            self.close_tabs_to_right(index)
        elif act.text() == SET_CURRENT_INDEX:
            # 当前页置顶
            self.setCurrentIndex(index)

    def check_tab_allow_close(self, *args) -> bool:
        # 检查是否允许关闭
        return True

    def close_current_tab(self, index):
        if self.check_tab_allow_close((index,)):
            self.remove_tab(index)

    def close_other_tabs(self, index):
        # 左侧的index
        left_index_list = list(range(0, index))
        # 右侧的index
        right_index_list = list(range(index + 1, self.count()))
        if self.check_tab_allow_close((*left_index_list, *right_index_list)):
            # 删除其他tab，先删除右边的，因为在删除的过程中，index会发生变化，所以要从大到小删除
            for idx in reversed(right_index_list):
                self.remove_tab(idx)
            # 再删除左边的
            for idx in reversed(left_index_list):
                self.remove_tab(idx)

    def close_all_tabs(self):
        index_list = range(0, self.count())
        if self.check_tab_allow_close(index_list):
            # 删除所有tab
            for idx in reversed(index_list):
                self.remove_tab(idx)

    def close_tabs_to_left(self, index):
        # 左侧的index
        left_index_list = range(0, index)
        if self.check_tab_allow_close(left_index_list):
            # 关闭标签页左边所有tab
            for idx in reversed(left_index_list):
                self.remove_tab(idx)

    def close_tabs_to_right(self, index):
        # 右侧的index
        right_index_list = range(index + 1, self.count())
        if self.check_tab_allow_close(right_index_list):
            # 关闭标签页右边所有tab
            for idx in reversed(right_index_list):
                self.remove_tab(idx)

    def remove_tab(self, index):
        self.parent.removeTab(index)


class DsTabBar(TabBarABC):
    remove_tab_signal = pyqtSignal(DsTableTab)

    def __init__(self, parent: QTabWidget):
        self.is_moving = False
        self.current_changed = False
        super().__init__(parent=parent)

    def mousePressEvent(self, event):
        # 如果按下了鼠标左键，将标志位设置为true
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_moving = True
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "is_moving"):
            # 鼠标按键松开，恢复标志位
            self.is_moving = False
            self.sort_tab()
        super().mouseReleaseEvent(event)

    def check_tab_allow_close(self, indexes):
        """根据索引，检查表是否都可以关闭，检查规则是：是否存在部分选中的表，如果部分选中则不可关闭，正在刷新的表也不可关闭"""
        partially_checked_tables, refreshing_tables = list(), list()
        for index in indexes:
            tab_widget = self.parent.widget(index)
            if tab_widget.tree_widget.get_item_node(tab_widget.tree_item).is_refreshing:
                refreshing_tables.append(self.partially_checked_table_prompt(tab_widget))
            if tab_widget.tree_item.checkState(0) == Qt.CheckState.PartiallyChecked:
                partially_checked_tables.append(self.partially_checked_table_prompt(tab_widget))
        if partially_checked_tables or refreshing_tables:
            prompt_list = list()
            if refreshing_tables:
                prompt_list.append(TABLE_CLOSE_WITH_REFRESHING.format('\n'.join(refreshing_tables)))
            if partially_checked_tables:
                prompt_list.append(TABLE_CLOSE_WITH_PARTIALLY_CHECKED.format('\n'.join(partially_checked_tables)))
            # 弹窗提示
            pop_fail('\n\n'.join(prompt_list), CLOSE_TABLE_BOX_TITLE, get_window())
        return not (partially_checked_tables or refreshing_tables)

    def partially_checked_table_prompt(self, tab_widget) -> str:
        ...

    def remove_tab(self, index, batch_clear_checked=True, allow_emit_remove_signal=True):
        # 获取tab table
        tab_widget = self.parent.widget(index)
        # 删除tab widget在树节点中的引用
        set_item_opened_tab(tab_widget.tree_item, None)
        # 删除tab
        self.parent.removeTab(index)
        table_tab = tab_widget.table_tab
        # 由更高层的树节点来调用时，只移除界面中的 tab 对象即可，无需发射其他信号
        if allow_emit_remove_signal:
            self.remove_tab_signal.emit(table_tab)
        # 清除选中数据，调用item node清除数据
        if batch_clear_checked:
            tab_widget.tree_widget.get_item_node(tab_widget.tree_item).close_tab_callback()

    def change_current(self, index):
        # 获取当前项
        current_tab = self.parent.widget(index)
        if self.need_change_current(current_tab) and current_tab:
            # 考虑处理tab顺序问题
            if self.is_moving:
                # 设置标志位，方便排序时判断使用
                self.current_changed = True
            self.parent.async_save_executor.change_current(current_tab.table_tab)

    def need_change_current(self, current_tab) -> bool:
        ...

    def sort_tab(self):
        """在拖拉tab页签，松开鼠标时触发，对最终状态的tab widget进行排序并保存"""
        if self.current_changed:
            tab_table_list = list()
            current_index = self.parent.currentIndex()
            # 首先收集现在的tab list，收集顺序及是否当前，全量更新tab
            for i in range(self.count()):
                table_tab = self.parent.widget(i).table_tab
                table_tab.item_order = i + 1
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
