# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from function import *


# 表格头的标题文字
header_labels = ["全选", "字段名", "数据类型", "备注"]
# 用来装行表头所有复选框 全局变量
all_header_combobox = list()
# 已选中集合
checked_set = set()


class CheckBoxHeader(QtWidgets.QHeaderView):
    """自定义表头类，参考自 https://www.pythonf.cn/read/108150"""

    # 自定义 复选框全选信号
    select_all_clicked = QtCore.pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2)

        if logicalIndex == 0:
            option = QtWidgets.QStyleOptionButton()
            option.rect = QtCore.QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_Active
            if self.isOn:
                option.state |= QtWidgets.QStyle.State_On
            else:
                option.state |= QtWidgets.QStyle.State_Off
            self.style().drawControl(QtWidgets.QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width \
                    and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 自定义信号 select_all_clicked 的槽方法
    def change_state(self, isOn):
        # 如果行表头复选框为勾选状态
        if isOn:
            # 将所有的复选框都设为勾选状态
            for i in all_header_combobox:
                i.setCheckState(QtCore.Qt.Checked)
        else:
            for i in all_header_combobox:
                i.setCheckState(QtCore.Qt.Unchecked)

    def set_header_checked(self, checked):
        if checked:
            self.isOn = True
            # 更新表头控件
            self.updateSection(0)
        else:
            self.isOn = False
            # 更新表头控件
            self.updateSection(0)


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
        # 创建表格列标题，共四列
        self.make_table_header()

        # 设置只读表格
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 让表格铺满整个控件
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.horizontalLayout.addWidget(self.tableWidget)
        # 隐藏表格头部列标题
        self.tableWidget.horizontalHeader().setVisible(False)
        # 交替行颜色
        self.tableWidget.setAlternatingRowColors(True)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "mysql连接列表"))
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
            self.tableWidget.cellChanged.connect(self.on_cell_changed)

    def make_tree_item(self, parent, name):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, self._translate("MainWindow", name))

    def fill_table(self, cols):
        """将列名字段全数填充在表中，三列多行表"""
        # 显示列标题
        self.tableWidget.horizontalHeader().setVisible(True)
        [self.tableWidget.removeRow(0) for r in range(self.tableWidget.rowCount())]
        # 清空选中集合
        checked_set.clear()
        all_header_combobox.clear()
        self.header.set_header_checked(False)
        # 填充数据
        for i, col in enumerate(cols):
            # 插入新的一行
            self.tableWidget.insertRow(i)
            # 设置checkbox在第一列，默认未选中
            check = QtWidgets.QTableWidgetItem()
            check.setCheckState(QtCore.Qt.Unchecked)
            self.tableWidget.setItem(i, 0, check)
            all_header_combobox.append(check)

            for n, field in enumerate(col, start=1):
                # 建立一个新的对象，赋值，填充到表格中对应位置
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, n, item)
                item.setText(self._translate("MainWindow", field))

    def make_table_header(self):
        """设置表格列标题"""
        # 表格设置为4列
        self.tableWidget.setColumnCount(4)
        # 实例化自定义表头
        self.header = CheckBoxHeader()
        # 设置表头
        self.tableWidget.setHorizontalHeader(self.header)
        # 设置表头字段
        self.tableWidget.setHorizontalHeaderLabels(header_labels)
        # 表头复选框单击信号与槽
        self.header.select_all_clicked.connect(self.header.change_state)

    def on_cell_changed(self, row, col):
        if col == 0:
            # 检查第一列，checkbox选中状态
            check = self.tableWidget.item(row, col)
            # 如果有选中的checkbox
            # todo 暂时只能通过判断 row 不在选中集合中来处理下面的操作。
            #  如果不处理，在选择第二个表的全选时，将会重复调用本方法，第三个表全选将会重复调用本方法三次 。。。
            #  目前没找到原因，只能先简单判断处理下。未选中的状态加入的 row判断也是因此。
            if check.checkState() == QtCore.Qt.Checked and row not in checked_set:
                # 表格总行数
                count = self.tableWidget.rowCount()
                # 将选中的行号加入选中行列表中
                checked_set.add(row)
                # 取出选中行的字段名称
                data = self.tableWidget.item(row, 1).text()
                print(f'{row}行 选中了 -> {data}：{checked_set}')
                # 如果选中行列表元素个数等于表格总行数
                if count == len(checked_set):
                    # 全选按钮应该选中，设置表头复选框按钮状态为选中
                    self.header.set_header_checked(True)
                else:
                    # 全选按钮应该是部分选中状态
                    pass
            elif check.checkState() == QtCore.Qt.Unchecked and row in checked_set:
                # 设置表头复选框按钮状态为未选中
                self.header.set_header_checked(False)
                if checked_set:
                    # 清空选中集合
                    if row in checked_set:
                        checked_set.remove(row)
                    data = self.tableWidget.item(row, 1).text()
                    print(f'{row}行 撤销选中 -> {data} : {checked_set}')

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
