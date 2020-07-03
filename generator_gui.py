# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from tree_strategy import *
from menu_bar_func import *
from sys_info_storage.sqlite import get_conns
from PyQt5 import QtGui, QtCore
from table_header import CheckBoxHeader
from gui_function import make_tree_item


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # 已经连接数据库的连接，key为id，value为DBExecutor对象
        self.connected_dict = dict()
        self._translate = QtCore.QCoreApplication.translate
        # 页面展示的连接（从系统库中获取的连接信息），key为id，value为connection对象
        self.conns_dict = dict()
        self.dbs = list()
        self.tables = list()

        self.setupUi()

    def setupUi(self):
        self.main_window.setObjectName("MainWindow")
        self.main_window.resize(1123, 896)
        self.centralwidget = QtWidgets.QWidget(self.main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)

        # 树结构的字体设置
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(13)
        self.treeWidget.setFont(font)
        self.treeWidget.setObjectName("treeWidget")
        self.horizontalLayout.addWidget(self.treeWidget)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.main_window.setCentralWidget(self.centralwidget)
        # 菜单栏
        self.menubar = QtWidgets.QMenuBar(self.main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 23))
        self.menubar.setObjectName("menubar")
        self.fill_menubar()
        self.main_window.setMenuBar(self.menubar)

        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(self.main_window)
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        # 初始化树：初始化获取树结构的第一层元素，为数据库连接列表
        self.get_saved_conns()

        # 初始化表格：隐式添加表格
        self.add_table()

        # 双击树节点事件
        self.treeWidget.doubleClicked.connect(self.get_tree_list)
        # 树结构中，第三层表格的复选框点击事件
        self.treeWidget.itemClicked.connect(self.table_check_box)
        # 右击事件
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.right_click_menu)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def retranslateUi(self):
        self.main_window.setWindowTitle(self._translate("MainWindow", "MainWindow"))
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
            self.conns_dict[item.id] = item

    def add_table(self):
        """添加表格"""
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        # 创建表格列标题，共四列
        self.make_table_header()

        # 设置只读表格
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 让表格铺满整个控件
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.horizontalLayout.addWidget(self.tableWidget)
        # 交替行颜色
        self.tableWidget.setAlternatingRowColors(True)

    def get_tree_list(self):
        """获取树的子节点，双击触发，将连接 -> 数据库 -> 数据表，按顺序读取出来"""
        item = self.treeWidget.currentItem()
        node = tree_node_factory(item)
        Context(node).open_item(item, self)

    def table_check_box(self, item):
        """处理树结构中，表的复选框"""
        node = tree_node_factory(item)
        # 只处理表
        Context(node).change_check_box(item, self)

    def update_tree_item_name(self, item, name, col=0):
        item.setText(col, self._translate("MainWindow", name))

    def make_table_header(self):
        """设置表格列标题"""
        # 表格设置为4列
        self.tableWidget.setColumnCount(4)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader()
        # 设置表头
        self.tableWidget.setHorizontalHeader(self.table_header)
        # 设置表头字段
        self.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
        # 表头复选框单击信号与槽
        self.table_header.select_all_clicked.connect(self.table_header.change_state)
        # 隐藏表格头部列标题
        self.table_header.setVisible(False)

    def on_cell_changed(self, row, col):
        """第一列checkbox状态改变时触发"""
        on_cell_changed(self, row, col)

    def close_conn(self, conn_id=None):
        """关闭连接"""
        close_connection(self, conn_id)

    def right_click_menu(self, pos):
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
        """点击右键菜单选项后触发事件"""
        # 获取右键点击的项
        item = self.treeWidget.currentItem()
        func = act.text()
        node = tree_node_factory(item)
        Context(node).handle_menu_func(item, func, self)

    def fill_menubar(self):
        fill_menu_bar(self)

    def add_conn(self):
        add_conn_func(self)

    def generate(self): ...

    def quit(self):
        self.main_window.close()

