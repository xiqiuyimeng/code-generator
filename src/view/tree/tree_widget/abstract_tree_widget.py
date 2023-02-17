# -*- coding: utf-8 -*-
"""
树结构抽象类，实现了智能展示滚动条功能，智能搜索功能
但是树节点复选框点击信号没有直接可以用的方法，经过计算可以获取复选框矩形，理论上点击坐标处于矩形内，可以发送复选框点击信号，
经测试发现，在矩形四角处似乎有问题，由于复选框圆角问题，导致圆角外坐标判断正确，却不能触发复选框点击状态变化，可能导致逻辑bug
所以根据树节点点击且导致复选框改变的需求，经过测试发现相关事件与信号的顺序为：
    mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发 -> itemChanged信号 -> clicked信号
    可以在mousePressEvent事件中设置标志位，表明事件类型是鼠标点击事件，
    而在itemChanged信号发出时，会触发树节点的 setData 方法，所以可以根据是否点击和数据变化，判断复选框是否点击，
    在clicked信号槽函数中重置标志位，实现点击复选框功能
"""
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidgetItemIterator

from src.service.async_func.async_item_changed_task import ItemChangedExecutor
from src.view.item_view_widget.abstract_item_view import AbstractItemView
from src.view.searcher.smart_item_view import SmartSearcherTreeWidget
from src.view.tab.tab_ui import TabTableUI
from src.view.tab.tab_widget.tab_widget import TabWidget
from src.view.tree.tree_item.abstract_tree_node import AbstractTreeNode
from src.view.tree.tree_item.tree_item_func import get_item_opened_record, link_table_checkbox, get_item_opened_tab, \
    recursive_get_add_del_data

_author_ = 'luwt'
_date_ = '2022/9/14 15:48'


class DisplayTreeWidget(SmartSearcherTreeWidget, AbstractItemView):

    def __init__(self, parent):
        super().__init__(parent)
        self.headerItem().setHidden(True)
        # 设置宽度
        self.resize_header_width()

    def keyPressEvent(self, event) -> None:
        # 先调用智能搜索的按键检测方法
        super().keyPressEvent(event)
        # 再调用统一元素视图中的方法
        AbstractItemView.keyPressEvent(self, event)

    def resizeEvent(self, e) -> None:
        self.resize_header_width()
        super().resizeEvent(e)

    def resize_header_width(self):
        # 按列宽来设置最小宽度，这样可以避免文本过长时，自动隐藏为省略号
        self.header().setMinimumSectionSize(self.sizeHintForColumn(0))


class AbstractTreeWidget(DisplayTreeWidget):
    # 定义信号，发送点击复选框的树节点
    item_checkbox_clicked = pyqtSignal(QTreeWidgetItem)

    def __init__(self, parent, window):
        super().__init__(parent)
        self.main_window = window
        # item 是否正在被鼠标左键点击
        self.item_clicked = False
        self.clicked_item = ...
        # 是否正在重新打开中，重新打开的过程，会创建子节点，并设置展开状态等，影响部分信号槽
        self.reopening_flag = False
        self.tree_data = ...
        # 用来记录item变化：当前项变化、展开状态
        self.item_changed_executor = ItemChangedExecutor()
        self.item_changed_executor.start()

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            # 判断是左键点击，将标志位置位True
            self.item_clicked = True
            # 获取点击的项
            self.clicked_item = self.itemAt(e.pos())
        super().mousePressEvent(e)

    def connect_signal(self):
        """定义通用的信号槽连接"""
        super().connect_signal()
        # 双击树节点事件
        self.doubleClicked.connect(self.open_tree_item)
        # 主要为了实现监听复选框点击
        self.itemClicked.connect(self.handle_item_clicked)
        self.item_checkbox_clicked.connect(self.handle_checkbox_changed)
        # 展开折叠信号
        self.itemCollapsed.connect(self.handle_item_collapsed)
        self.itemExpanded.connect(self.handle_item_expanded)
        # 当前项变化信号
        self.currentItemChanged.connect(self.handle_current_item_changed)

    def open_tree_item(self, idx):
        item = self.itemFromIndex(idx)
        self.do_open_tree_item(item)

    def handle_item_clicked(self):
        # 鼠标左键点击结束事件，将标志位置位False
        self.item_clicked = False
        self.clicked_item = ...

    def handle_checkbox_changed(self, item: QTreeWidgetItem, clicked=True):
        # 事件信号顺序是：mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发
        # -> itemChanged信号 -> clicked信号
        # 而在itemChanged信号发出时，会触发树节点的 setData方法，
        # 所以可以根据是否点击和数据变化，判断复选框是否点击
        self.do_handle_checkbox_changed(item, clicked)
        check_state = item.checkState(0)
        self.handle_child_item_checked(item, check_state)

    def handle_child_item_checked(self, item, check_state):
        # 之所以不直接使用 item.checkState(0)，而使用参数传递的形式，
        # 是为了避免当前节点没有设置复选框，但是又需要将子节点复选框状态统一修改时使用
        # 如果存在子元素，应该将子元素复选框状态同步修改
        if item.childCount():
            # 批量更新选中状态
            self.item_changed_executor.item_child_checked(item, check_state)

            # 批量添加选中数据
            add_del_data, opened_list = dict(), list()

            for i in range(item.childCount()):
                child_item = item.child(i)
                # 如果复选框状态相同，跳过
                if child_item.data(0, Qt.CheckStateRole) is None \
                        or child_item.checkState(0) == check_state:
                    continue
                opened_list.append(get_item_opened_record(child_item))
                child_item.setCheckState(0, check_state)
                get_item_opened_record(child_item).checked = check_state
                self.handle_checkbox_changed(child_item, clicked=False)
            if opened_list:
                recursive_get_add_del_data(item, add_del_data)
                add_del_data[opened_list[0].level] = opened_list
                if check_state == Qt.Unchecked:
                    self.tree_data.del_node(add_del_data)
                else:
                    self.tree_data.add_node(add_del_data)

    def handle_item_collapsed(self, item):
        if not self.reopening_flag:
            # item收起
            self.item_changed_executor.item_collapsed(item)
            self.recursive_collapse_item(item)

    def handle_item_expanded(self, item):
        if not self.reopening_flag:
            self.item_changed_executor.item_expanded(item)

    def handle_current_item_changed(self, current_item):
        if current_item and not self.reopening_flag:
            self.item_changed_executor.current_item_changed(current_item)

    def recursive_collapse_item(self, item):
        if item.childCount():
            for index in range(item.childCount()):
                child_item = item.child(index)
                if child_item.isExpanded():
                    child_item.setExpanded(False)
                    self.item_changed_executor.item_collapsed(child_item)
                    self.recursive_collapse_item(child_item)
                if get_item_opened_record(child_item).is_current:
                    self.item_changed_executor.not_current_item(child_item)

    def get_item_by_opened_id(self, opened_id):
        """根据打开记录表中的id查找"""
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if get_item_opened_record(item).id == opened_id:
                return item
            iterator = iterator.__iadd__(1)

    def set_record_current_item(self):
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            if get_item_opened_record(item).is_current:
                self.set_selected_focus(item)
            iterator = iterator.__iadd__(1)

    def get_top_level_items(self):
        top_level_items = list()
        for idx in range(self.topLevelItemCount()):
            top_level_items.append(self.topLevelItem(idx))
        return top_level_items

    def set_tree_unchecked(self):
        iterator = QTreeWidgetItemIterator(self)
        while iterator.value():
            item = iterator.value()
            # 如果选中，置为非选中
            if item.checkState(0):
                item.setCheckState(0, Qt.Unchecked)
                self.item_changed_executor.item_checked(item)
                link_table_checkbox(item, Qt.Unchecked)
            iterator = iterator.__iadd__(1)

    def locate_item(self):
        # 找到当前tab，取出对应item
        tab = self.get_current_tab()
        if tab:
            self.set_selected_focus(tab.tree_item)

    def do_open_tree_item(self, item):
        self.get_item_node(item).open_item()

    def fill_menu(self, item, menu):
        self.do_fill_menu(item, menu)

    def do_fill_menu(self, item, menu):
        self.get_item_node(item).do_fill_menu(menu)

    def do_right_menu_func(self, item, func_name):
        self.get_item_node(item).handle_menu_func(func_name)

    def do_handle_checkbox_changed(self, item, clicked):
        self.get_item_node(item).change_check_box(item.checkState(0), clicked)

    def refresh(self, item):
        self.get_item_node(item).refresh()

    def get_current_tab(self) -> TabTableUI:
        return self.get_current_tab_widget().get_current_widget()

    def reopen_tree_item(self, opened_items):
        # 首先获取父元素
        parent_item = self.get_item_by_opened_id(opened_items[0].parent_id)
        self.get_item_node(parent_item).reopen_item(opened_items)

    def reopen_tab(self, opened_tabs):
        """
        重新打开tab页
        """
        current_tab = None
        for opened_tab in opened_tabs:
            # 找到表节点
            item = self.get_item_by_opened_id(opened_tab.parent_opened_id)
            self.get_item_node(item).reopen_item(opened_tab)
            tab = get_item_opened_tab(item)
            if opened_tab.is_current:
                current_tab = tab
        # 将当前页置为当前
        self.get_current_tab_widget().setCurrentWidget(current_tab)

    def reopen_end(self):
        # 找出当前项，选中
        self.set_record_current_item()
        self.reopening_flag = False

    def reopen_tree(self):
        ...

    def get_current_tab_widget(self) -> TabWidget:
        ...

    def get_item_node(self, item) -> AbstractTreeNode:
        ...
