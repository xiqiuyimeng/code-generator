# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from function import *


class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1123, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
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
        # 初始化获取树结构的第一层元素，为数据库连接列表
        self.get_conns()
        self.dbs = list()
        self.tables = list()

        # 双击树节点事件
        self.treeWidget.doubleClicked.connect(self.get_tree_list)
        # 右击事件
        # self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.rightClickMenu)
        self.horizontalLayout.addWidget(self.treeWidget)

        # 隐式添加表格
        self.add_table()
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def add_table(self):
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        # 创建表格列标题，共三列
        self.make_table_header()

        # 设置只读表格
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 让表格铺满整个控件
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.horizontalLayout.addWidget(self.tableWidget)
        # 隐藏表格头部列标题
        self.tableWidget.horizontalHeader().setVisible(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "列表"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def get_conns(self):
        """获取所有链接，生成页面列表"""
        # 根节点，展示连接的列表
        self.conn = self.treeWidget.currentItem()
        conn_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        conn_item.setText(0, self._translate("MainWindow", "centos121"))

    def get_tree_list(self, index):
        """获取树的子节点，双击触发，将连接 -> 数据库 -> 数据表，按顺序读取出来"""
        item = self.treeWidget.currentItem()
        # 数据库列表，父节点是连接
        if item.parent() is self.conn:
            dbs = get_dbs()
            for db in dbs:
                self.make_tree_item(item, db)
                self.dbs.append(db)
        # 如果是具体的数据库，那么查询库中所有的表，并展示为树形结构，父节点为当前库
        elif item.text(0) in self.dbs:
            switch_db(item.text(0))
            tables = get_tables()
            for table in tables:
                self.make_tree_item(item, table)
                self.tables.append(table)
        # 如果是具体的表，那么查询所有的字段名称，显示在右侧表格中
        elif item.text(0) in self.tables:
            cols = get_cols(item.text(0))
            self.fill_table(cols)

    def make_tree_item(self, parent, name):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, self._translate("MainWindow", name))

    def fill_table(self, cols):
        """将列名字段全数填充在表中，三列多行表"""
        # 显示列标题
        self.tableWidget.horizontalHeader().setVisible(True)
        [self.tableWidget.removeRow(0) for r in range(self.tableWidget.rowCount())]
        # 填充数据
        for i, col in enumerate(cols):
            # 插入新的一行
            self.tableWidget.insertRow(i)
            for n, field in enumerate(col):
                # 建立一个新的对象，赋值，填充到表格中对应位置
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, n, item)
                item.setText(self._translate("MainWindow", field))

    def make_table_header(self):
        """设置表格列标题"""
        self.tableWidget.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item.setText(self._translate("MainWindow", "字段名"))
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item.setText(self._translate("MainWindow", "数据类型"))
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item.setText(self._translate("MainWindow", "备注"))

    def close_conn(self):
        executor.exit()


    # def rightClickMenu(self, pos):
    #     menu = QtWidgets.QMenu()
    #     menu.addAction(QtWidgets.QAction('编辑连接', menu))
    #     menu.addAction(QtWidgets.QAction('删除连接', menu))
    #     menu.triggered.connect(self.menuSlot)
    #     menu.exec_(QtGui.QCursor.pos())
    #
    # def menuSlot(self, act):
    #     print(act.text())
