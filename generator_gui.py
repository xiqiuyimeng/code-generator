# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
# from function import *


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


from collections import namedtuple
from db_info import DBExecutor
# todo 模拟数据
conn = namedtuple('conn', 'host user pwd port')
centos121 = conn('centos121', 'root', 'admin', 3306)
cvhub_107 = conn('172.16.17.107', 'root', 'admin', 3306)
cvhub_89 = conn('172.16.26.89', 'root', 'admin', 3306)
conn_dict = {
    'centos121': centos121,
    'cvhub_107': cvhub_107,
    'cvhub_89': cvhub_89
}


class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        self.conn_dict = dict()
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
        self.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.right_click_menu)

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
        for alias, conn in conn_dict.items():
            # 根节点，展示连接的列表
            self.conn = self.treeWidget.currentItem()
            conn_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            conn_item.setText(0, self._translate("MainWindow", alias))

    def get_conn(self, conn_name):
        """根据连接名称，从当前维护的连接字典中获取一个数据库连接操作对象"""
        if not self.conn_dict.get(conn_name):
            executor = DBExecutor(*conn_dict.get(conn_name))
            self.conn_dict[conn_name] = executor
        else:
            executor = self.conn_dict.get(conn_name)
        return executor

    def get_tree_list(self):
        """获取树的子节点，双击触发，将连接 -> 数据库 -> 数据表，按顺序读取出来"""
        item = self.treeWidget.currentItem()
        # 当前点击项为连接时，父节点为空，查询连接下所有的库
        if item.parent() is None:
            # 仅当子元素不存在时，获取子元素并填充
            if item.childCount() == 0:
                # 连接名称
                conn_name = item.text(0)
                dbs = self.get_conn(conn_name).get_dbs()
                for db in dbs:
                    self.make_tree_item(item, db)
        # 如果是具体的数据库，那么查询库中所有的表，并展示为树形结构，
        # 父节点为连接，连接的父节点为空
        elif item.parent().parent() is None:
            # 仅当子元素不存在时，获取子元素并填充
            if item.childCount() == 0:
                # 获取连接名称，从而获取该连接的数据库操作对象
                conn_name = item.parent().text(0)
                executor = self.get_conn(conn_name)
                # 首先需要切换库
                executor.switch_db(item.text(0))
                tables = executor.get_tables()
                for table in tables:
                    self.make_tree_item(item, table)
        # # 如果是具体的表，那么查询所有的字段名称，显示在右侧表格中，
        # 父节点为库，库父节点为连接，连接父节点为空
        elif item.parent().parent().parent() is None:
            # 获取连接名称，从而获取该连接的数据库操作对象
            conn_name = item.parent().parent().text(0)
            executor = self.get_conn(conn_name)
            # 获取当前表下所有的列名
            cols = executor.get_cols(item.text(0))
            self.fill_table(cols)
            self.tableWidget.cellChanged.connect(self.on_cell_changed)

    def make_tree_item(self, parent, name):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, self._translate("MainWindow", name))

    def fill_table(self, cols):
        """将列名字段全数填充在表中，三列多行表"""
        # 显示列标题
        self.tableWidget.horizontalHeader().setVisible(True)
        self.clear_table()
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

    def close_conn(self, conn_name=None):
        if conn_name:
            self.conn_dict.get(conn_name).exit()
            del self.conn_dict[conn_name]
        else:
            [executor.exit() for executor in self.conn_dict.values()]
            self.conn_dict.clear()

    def right_click_menu(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.treeWidget.itemAt(pos)
        if item:
            menu = QtWidgets.QMenu()
            menu_names = list()
            # 连接列表的右键菜单
            if item.parent() is None:
                menu_names = self.get_conn_menu_names(item)
            # 数据库列表的右键菜单
            elif item.parent().parent() is None:
                menu_names = self.get_db_menu_names(item)
            # 其他作为数据表列表的右键菜单
            else:
                menu_names = self.get_table_menu_names()
            [menu.addAction(QtWidgets.QAction(option, menu)) for option in menu_names]
            menu.triggered.connect(self.menu_slot)
            menu.exec_(QtGui.QCursor.pos())

    def get_conn_menu_names(self, item):
        """生成第一层，连接列表的右键菜单名称"""
        menu_names = list()
        if item.childCount():
            menu_names.append('关闭连接')
        else:
            menu_names.append('打开连接')
        menu_names.append('编辑连接')
        menu_names.append('删除连接')
        return menu_names

    def get_db_menu_names(self, item):
        """生成第二层，数据库列表的右键菜单名称"""
        menu_names = list()
        if item.childCount():
            menu_names.append('关闭数据库')
            menu_names.append('全选所有表')
        else:
            menu_names.append('打开数据库')
        return menu_names

    def get_table_menu_names(self):
        """生成第三层，数据表列表的右键菜单"""
        menu_names = ['生成']
        return menu_names

    def menu_slot(self, act):
        """点击右键菜单选项后触发事件"""
        # 获取右键点击的项
        item = self.treeWidget.currentItem()
        # 如果是连接
        if item.parent() is None:
            func = act.text()
            if func == '打开连接':
                self.open_tree_item(item)
            elif func == '关闭连接':
                self.close_tree_item(item)
                # 关闭数据连接
                self.close_conn(item.text(0))
        # 如果是数据库
        elif item.parent().parent() is None:
            func = act.text()
            if func == '打开数据库':
                self.open_tree_item(item)
            elif func == '关闭数据库':
                self.close_tree_item(item)

    def open_tree_item(self, item):
        """打开树的某项，展开状态置为 true，刷新下页面"""
        self.get_tree_list()
        item.setExpanded(True)
        self.treeWidget.repaint()

    def close_tree_item(self, item):
        """关闭树的某项，将其下所有子项移除，并将扩展状态置为false"""
        # 移除所有子项目
        for child in item.takeChildren():
            item.removeChild(child)
        self.close_table()
        item.setExpanded(False)

    def close_table(self):
        """关闭右侧表格"""
        # 删除表格内容
        self.clear_table()
        # 隐藏表头
        self.tableWidget.horizontalHeader().setVisible(False)

    def clear_table(self):
        """清空右侧表格"""
        [self.tableWidget.removeRow(0) for r in range(self.tableWidget.rowCount())]
        # 清空选中集合
        checked_set.clear()
        all_header_combobox.clear()
        self.header.set_header_checked(False)
