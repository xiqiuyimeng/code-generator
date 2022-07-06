# -*- coding: utf-8 -*-
"""
树结构，实现了智能展示滚动条功能，智能搜索功能
但是树节点复选框点击信号没有直接可以用的方法，经过计算可以获取复选框矩形，理论上点击坐标处于矩形内，可以发送复选框点击信号，
经测试发现，在矩形四角处似乎有问题，由于复选框圆角问题，导致圆角外坐标判断正确，却不能触发复选框点击状态变化，可能导致逻辑bug
所以根据树节点点击且导致复选框改变的需求，经过测试发现相关事件与信号的顺序为：
    mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发 -> itemChanged信号 -> clicked信号
    可以在mousePressEvent事件中设置标志位，表明在点击，在itemChanged信号槽函数中判断是否点击，在clicked信号槽函数中重置标志位，
    实现点击复选框触发事件
"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QMenu, QAction

from service.async_func.async_conn_task import ListConnExecutor
from view.custom_widget.scrollable_widget import ScrollableWidget
from view.searcher.smart_item_view import SmartSearcherTreeWidget
from view.tree.tree_function import make_conn_tree_items
from view.tree.tree_item_strategy import Context

_author_ = 'luwt'
_date_ = '2022/5/7 17:21'


class TreeWidget(QTreeWidget, ScrollableWidget, SmartSearcherTreeWidget):

    def __init__(self, parent, window):
        super().__init__(parent)
        self.main_window = window
        self.conn_name_dict: dict = ...
        # item 是否正在被鼠标左键点击
        self.item_clicked = False
        self.headerItem().setHidden(True)
        # 统一设置图标大小
        self.setIconSize(QSize(40, 30))
        # 连接的图标
        self.conn_icon = QIcon(":/icon/mysql_conn_icon.png")
        # 数据库图标
        self.db_icon = QIcon(":icon/database_icon.png")
        # 数据表图标
        self.tb_icon = QIcon(":icon/table_icon.png")
        self.connect_signal()
        # 初始化数据
        self.list_conn_executor = ListConnExecutor(parent, parent, self.init_conn_tree_items)
        self.list_conn_executor.start()

    def init_conn_tree_items(self, conns):
        make_conn_tree_items(conns, self, self.conn_icon)
        self.init_conn_name_list(conns)

    def init_conn_name_list(self, conns):
        self.conn_name_dict = dict(zip(map(lambda conn: conn.id, conns), map(lambda conn: conn.name, conns)))

    def add_conn_name(self, conn_id, conn_name):
        self.conn_name_dict[conn_id] = conn_name

    def update_conn_name(self, conn_id, conn_name):
        self.conn_name_dict[conn_id] = conn_name

    def del_conn_name(self, conn_id):
        del self.conn_name_dict[conn_id]

    def connect_signal(self):
        # 双击树节点事件
        self.doubleClicked.connect(self.open_tree_item)
        # 第三层树节点，复选框点击事件
        self.itemClicked.connect(self.handle_item_clicked)
        # 右击事件
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_right_mouse_clicked)
        # 主要为了实现监听复选框点击
        self.itemChanged.connect(self.item_change)

    def open_tree_item(self, idx):
        item = self.itemFromIndex(idx)
        Context(item, self, self.main_window).open_item()

    def handle_item_clicked(self):
        # 鼠标左键点击结束事件，将标志位置位False
        self.item_clicked = False

    def handle_right_mouse_clicked(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.itemAt(pos)
        if item:
            # 生成右键菜单
            menu = QMenu()
            menu_names = Context(item, self, self.main_window).get_menu_names()
            [menu.addAction(QAction(option, menu)) for option in menu_names]
            # 右键菜单点击事件
            menu.triggered.connect(self.right_menu_func)
            # 右键菜单弹出位置跟随焦点位置
            menu.exec_(QCursor.pos())

    def item_change(self, item: QTreeWidgetItem):
        # 事件信号顺序是：mousePressEvent 按鼠标事件触发 -> mouseReleaseEvent 鼠标释放事件触发
        # -> itemChanged信号 -> clicked信号
        if self.item_clicked:
            Context(item, self, self.main_window).change_check_box(item.checkState(0))

    def mousePressEvent(self, e) -> None:
        if e.button() == Qt.LeftButton:
            # 判断是左键点击，将标志位置位True
            self.item_clicked = True
        super().mousePressEvent(e)

    def right_menu_func(self, action):
        """
        点击右键菜单选项后触发事件
        :param action: 右键菜单中的选项
        """
        # 获取右键点击的项
        item = self.currentItem()
        Context(item, self, self.main_window).handle_menu_func(action.text())





