# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt

from confirm_select_dialog import DisplaySelectedDialog
from connection_function import close_connection
from constant import TREE_HEADER_LABELS, WRONG_UNSELECT_DATA, WRONG_TITLE
from font import set_font
from menu_bar_func import fill_menu_bar
from message_box import pop_fail
from selected_data import SelectedData
from sys_info_storage.sqlite import get_conns
from table_func import on_cell_changed
from tool_bar import fill_tool_bar
from tree_function import make_tree_item, add_conn_func
from tree_strategy import tree_node_factory, Context


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # 已经连接数据库的连接，key为连接名，value为DBExecutor对象
        self.connected_dict = dict()
        self._translate = QtCore.QCoreApplication.translate
        # 页面展示的连接（从系统库中获取的连接信息），key为id，value为connection对象，
        # 因为在编辑连接后，连接名称可能会变化，无法作为唯一标识
        self.display_conn_dict = dict()
        self.dbs = list()
        self.tables = list()

        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.resize(1123, 896)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)

        # 树结构的字体设置
        self.treeWidget.setFont(set_font())
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout.addWidget(self.treeWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.setCentralWidget(self.centralwidget)
        # 菜单栏
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 23))
        self.menubar.setObjectName("menubar")
        fill_menu_bar(self)
        self.setMenuBar(self.menubar)

        # 工具栏
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        # 设置名称显示在图标下面（默认本来是只显示图标）
        fill_tool_bar(self)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # 初始化树：初始化获取树结构的第一层元素，为数据库连接列表
        self.get_saved_conns()

        # 双击树节点事件
        self.treeWidget.doubleClicked.connect(self.get_tree_list)
        # 树结构中，第三层表格的复选框点击事件
        self.treeWidget.itemClicked.connect(self.table_check_box)
        # 右击事件
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.right_click_menu)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(self._translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, self._translate("MainWindow", TREE_HEADER_LABELS))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def get_saved_conns(self):
        """获取所有已存储的连接，生成页面树结构第一层"""
        conns = get_conns()
        for item in conns:
            # item属性：id name host port user pwd
            # 根节点，展示连接的列表
            make_tree_item(self, self.treeWidget, item.name, item.id)
            self.display_conn_dict[item.id] = item

    def get_tree_list(self):
        """获取树的子节点，双击触发，将连接 -> 数据库 -> 数据表，按顺序读取出来"""
        item = self.treeWidget.currentItem()
        node = tree_node_factory(item)
        Context(node).open_item(item, self)

    def table_check_box(self, item):
        """
        处理树结构中，表的复选框，实现表的复选框与表格控件中复选框联动效果
        :param item: 当前点击树节点元素
        """
        node = tree_node_factory(item)
        # 只处理表
        Context(node).change_check_box(item, self)

    def update_tree_item_name(self, item, name, col=0):
        """
        更新树的节点项名称
        :param item: 当前树节点元素
        :param name: 要更新的名字
        :param col: 写入在哪一列，默认名字写在第一列，第二列为隐藏列，可写id作为隐藏属性
        """
        item.setText(col, self._translate("MainWindow", name))

    def update_table_item(self, item, field):
        """
        更新表格控件中表格的值
        :param item: 当前表格元素
        :param field: 要填写的值
        """
        item.setText(self._translate("MainWindow", field))

    def on_cell_changed_func(self, row, col):
        """
        第一列checkbox状态改变时触发
        :param row: 表格中当前行
        :param col: 表格中当前列
        """
        on_cell_changed(self, row, col)

    def close_conn(self, conn_name=None):
        """
        关闭连接
        :param conn_name: 要关闭的连接名称，若无，则关闭所有
        """
        close_connection(self, conn_name)

    def right_click_menu(self, pos):
        """
        右键菜单功能，实现右键弹出菜单功能
        :param pos:右键的坐标位置
        """
        # 获取当前元素，只有在元素上才显示菜单
        item = self.treeWidget.itemAt(pos)
        if item:
            # 生成右键菜单
            menu = QtWidgets.QMenu()
            node = tree_node_factory(item)
            menu_names = Context(node).get_menu_names(item, self)
            [menu.addAction(QtWidgets.QAction(option, menu)) for option in menu_names]
            # 右键菜单点击事件
            menu.triggered.connect(self.menu_slot)
            # 右键菜单弹出位置跟随焦点位置
            menu.exec_(QtGui.QCursor.pos())

    def menu_slot(self, act):
        """
        点击右键菜单选项后触发事件
        :param act: 右键菜单中的动作
        """
        # 获取右键点击的项
        item = self.treeWidget.currentItem()
        func = act.text()
        node = tree_node_factory(item)
        Context(node).handle_menu_func(item, func, self)

    def add_conn(self):
        add_conn_func(self)

    def generate(self):
        selected_data = SelectedData().conn_dict
        if selected_data:
            generate_dialog = DisplaySelectedDialog(self, selected_data)
            generate_dialog.setWindowModality(Qt.ApplicationModal)
            generate_dialog.show()
        else:
            pop_fail(WRONG_TITLE, WRONG_UNSELECT_DATA)

    def quit(self):
        self.close()

