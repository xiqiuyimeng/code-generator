# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from table_header import all_header_combobox, CheckBoxHeader
from conn_dialog import *
from sys_info_storage.sqlite import *
from db_info import DBExecutor
from message_box import *
from menu import *
from menu_bar import *
from PyQt5 import QtWidgets, QtGui

# 已选中集合
checked_set = set()


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
            self.make_tree_item(self.treeWidget, item.name, item.id)
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

    def get_conn(self, conn_id):
        """根据连接名称，从当前维护的连接字典中获取一个数据库连接操作对象"""
        # 如果该连接已经打开，直接取，否则获取新的连接
        if not self.connected_dict.get(conn_id):
            # id name host port user pwd
            conn_info = self.conns_dict.get(conn_id)
            executor = DBExecutor(*conn_info[2:])
            self.connected_dict[conn_id] = executor
        else:
            executor = self.connected_dict.get(conn_id)
        return executor

    def get_tree_list(self):
        """获取树的子节点，双击触发，将连接 -> 数据库 -> 数据表，按顺序读取出来"""
        item = self.treeWidget.currentItem()
        # 当前点击项为连接时，父节点为空，查询连接下所有的库
        if item.parent() is None:
            # 仅当子元素不存在时，获取子元素并填充
            if item.childCount() == 0:
                # 连接的id，存在于元素的第一列
                conn_id = int(item.text(1))
                dbs = self.get_conn(conn_id).get_dbs()
                for db in dbs:
                    self.make_tree_item(item, db)
        # 如果是具体的数据库，那么查询库中所有的表，并展示为树形结构，增加复选框，默认未选中
        # 父节点为连接，连接的父节点为空
        elif item.parent().parent() is None:
            # 仅当子元素不存在时，获取子元素并填充
            if item.childCount() == 0:
                # 获取连接id，从而获取该连接的数据库操作对象
                conn_id = int(item.parent().text(1))
                executor = self.get_conn(conn_id)
                # 首先需要切换库
                executor.switch_db(item.text(0))
                tables = executor.get_tables()
                for table in tables:
                    self.make_tree_item(item, table, checkbox=QtCore.Qt.Unchecked)
        # 如果是具体的表，那么查询所有的字段名称，显示在右侧表格中，
        # 父节点为库，库父节点为连接，连接父节点为空
        elif item.parent().parent().parent() is None:
            # 获取连接id，从而获取该连接的数据库操作对象
            conn_id = int(item.parent().parent().text(1))
            executor = self.get_conn(conn_id)
            # 获取当前表下所有的列名
            cols = executor.get_cols(item.text(0))
            # 当前表若被选中，则其所有字段都应被选中
            self.fill_table(cols, item.checkState(0))
            if item.checkState(0) == Qt.Checked:
                self.header.set_header_checked(True)
            self.tableWidget.cellChanged.connect(self.on_cell_changed)
            self.current_table = item

    def table_check_box(self, item, col):
        """处理树结构中，表的复选框"""
        if item.parent() is None:
            pass
        elif item.parent().parent() is None:
            pass
        # 只处理表
        elif item.parent().parent().parent() is None:
            check_state = item.checkState(0)
            # 如果表已经选中，那么右侧表格需全选字段
            if check_state == Qt.Checked:
                self.change_table_checkbox(True)
            # 如果表未选中，那么右侧表格需清空选择
            elif check_state == Qt.Unchecked:
                self.change_table_checkbox(False)

    def change_table_checkbox(self, checked):
        """改变表格中checkbox中所有复选框状态，换言之，全选或清空选择"""
        # 通过表头是否展示，判定表是否已经展示
        visible = self.tableWidget.horizontalHeader().isVisible()
        if visible:
            self.header.set_header_checked(checked)
            self.header.change_state(checked)

    def make_tree_item(self, parent, name, item_id=None, checkbox=None):
        """构造树的子项"""
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, self._translate("MainWindow", name))
        if item_id:
            # id 作为隐藏属性，写于第二列
            item.setText(1, self._translate("MainWindow", str(item_id)))
        if checkbox is not None:
            item.setCheckState(0, checkbox)

    def update_tree_item_name(self, item, name):
        item.setText(0, self._translate("MainWindow", name))

    def fill_table(self, cols, checked):
        """将列名字段全数填充在表中，四列多行表"""
        # 显示列标题
        self.tableWidget.horizontalHeader().setVisible(True)
        self.clear_table()
        # 填充数据
        for i, col in enumerate(cols):
            # 插入新的一行
            self.tableWidget.insertRow(i)
            # 设置checkbox在第一列
            check = QtWidgets.QTableWidgetItem()
            check.setCheckState(checked)
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
        self.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
        # 表头复选框单击信号与槽
        self.header.select_all_clicked.connect(self.header.change_state)
        # 隐藏表格头部列标题
        self.header.setVisible(False)

    def on_cell_changed(self, row, col):
        """第一列checkbox状态改变时触发"""
        if col == 0:
            # 检查第一列，checkbox选中状态
            item = self.tableWidget.item(row, col)
            # 如果有选中的checkbox
            # todo 暂时只能通过判断 row 不在选中集合中来处理下面的操作。
            #  如果不处理，在选择第二个表的全选时，将会重复调用本方法，第三个表全选将会重复调用本方法三次 。。。
            #  目前没找到原因，只能先简单判断处理下。未选中的状态加入的 row判断也是因此。
            if item.checkState() == QtCore.Qt.Checked and row not in checked_set:
                # 表格总行数
                count = self.tableWidget.rowCount()
                # 将选中的行号加入选中行列表中
                checked_set.add(row)
                # 取出选中行的字段名称
                data = self.tableWidget.item(row, 1).text()
                print(f'{row}行 选中了 -> {data}：{checked_set}')
                # 状态栏
                self.statusbar.showMessage(f'{row}行 选中了 -> {data}：{checked_set}')
                # 如果选中行列表元素个数等于表格总行数
                if count == len(checked_set):
                    # 全选按钮应该选中，设置表头复选框按钮状态为选中
                    self.header.set_header_checked(True)
                # 设置左侧树部件中，对应表也应为选中状态
                self.current_table.setCheckState(0, Qt.Checked)
            elif item.checkState() == QtCore.Qt.Unchecked and row in checked_set:
                # 设置表头复选框按钮状态为未选中
                self.header.set_header_checked(False)
                if checked_set:
                    # 清空选中集合
                    if row in checked_set:
                        checked_set.remove(row)
                    # 设置左侧树部件中，对应表为未选中状态
                    if len(checked_set) == 0:
                        self.current_table.setCheckState(0, Qt.Unchecked)
                    data = self.tableWidget.item(row, 1).text()
                    print(f'{row}行 撤销选中 -> {data} : {checked_set}')
                    # 状态栏
                    self.statusbar.showMessage(f'{row}行 撤销选中 -> {data} : {checked_set}')

    def close_conn(self, conn_id=None):
        """关闭连接"""
        if conn_id and self.connected_dict.get(conn_id):
            self.connected_dict.get(conn_id).exit()
            del self.connected_dict[conn_id]
        else:
            [executor.exit() for executor in self.connected_dict.values()]
            self.connected_dict.clear()

    def right_click_menu(self, pos):
        # 获取当前元素，只有在元素上才显示菜单
        item = self.treeWidget.itemAt(pos)
        if item:
            menu = QtWidgets.QMenu()
            # 连接列表的右键菜单
            if item.parent() is None:
                menu_names = get_conn_menu_names(item)
            # 数据库列表的右键菜单
            elif item.parent().parent() is None:
                checked = self.check_table_status(item)
                menu_names = get_db_menu_names(item, checked)
            # 其他作为数据库中表列表的右键菜单
            else:
                # 检查字段选中状态
                checked = self.check_field_status(item)
                # 检查表是否展示
                table_opened = self.tableWidget.horizontalHeader().isVisible() and self.current_table is item
                menu_names = get_table_menu_names(table_opened, checked)
            [menu.addAction(QtWidgets.QAction(option, menu)) for option in menu_names]
            menu.triggered.connect(self.menu_slot)
            menu.exec_(QtGui.QCursor.pos())

    def menu_slot(self, act):
        """点击右键菜单选项后触发事件"""
        # 获取右键点击的项
        item = self.treeWidget.currentItem()
        func = act.text()
        # 如果是连接
        if item.parent() is None:
            self.handle_conn_menu(item, func)
        # 如果是数据库
        elif item.parent().parent() is None:
            self.handle_db_menu(item, func)
        # 如果是表
        elif item.parent().parent().parent() is None:
            self.handle_table_menu(item, func)

    def open_tree_item(self, item):
        """打开树的某项，展开状态置为 true，刷新下页面"""
        self.get_tree_list()
        item.setExpanded(True)
        self.treeWidget.repaint()

    def close_tree_item(self, item):
        """关闭树的某项，将其下所有子项移除，并将扩展状态置为false"""
        # 移除所有子项目
        item.takeChildren()
        self.close_table()

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

    def show_conn_dialog(self, conn_info, title):
        """打开添加、编辑连接子窗口"""
        dialog = Ui_Dialog(conn_info, title)
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.show()
        if title == ADD_CONN_MENU:
            dialog.conn_signal.connect(self.add_conn_tree_item)
        elif title == EDIT_CONN_MENU:
            dialog.conn_signal.connect(self.update_conn_tree_item)

    def add_conn_tree_item(self, connection):
        """添加树节点（连接）"""
        self.conns_dict[connection.id] = connection
        self.make_tree_item(self.treeWidget, connection.name, connection.id)

    def update_conn_tree_item(self, connection):
        """更新树节点"""
        self.conns_dict[connection.id] = connection
        item = self.treeWidget.currentItem()
        self.update_tree_item_name(item, connection.name)

    def handle_conn_menu(self, item, func):
        """右键菜单中关于连接的处理"""
        # 获取当前选中的连接id
        conn_id = int(item.text(1))
        # 打开连接
        if func == OPEN_CONN_MENU:
            self.open_tree_item(item)
        # 关闭连接
        elif func == CLOSE_CONN_MENU:
            self.close_tree_item(item)
            # 关闭数据连接，关闭特定连接，id为标识
            self.close_conn(conn_id)
        # 测试连接
        elif func == TEST_CONN_MENU:
            test_connection(self.conns_dict.get(conn_id))
        # 添加连接
        elif func == ADD_CONN_MENU:
            conn_info = Connection(None, None, None, None, None, None)
            self.show_conn_dialog(conn_info, func)
        # 编辑连接
        elif func == EDIT_CONN_MENU:
            # 先弹关闭连接确认框
            reply = pop_question(func, EDIT_CONN_PROMPT)
            if reply:
                # 关闭连接
                self.close_conn(conn_id)
                self.close_tree_item(item)
                conn_info = self.conns_dict.get(conn_id)
                self.show_conn_dialog(conn_info, func)
                # 在子窗口更新完数据库和页面后，将页面的存储数据也更新
                self.conns_dict[conn_id] = get_conn(conn_id)
        # 删除连接
        elif func == DEL_CONN_MENU:
            # 弹出关闭连接确认框
            reply = pop_question(func, DEL_CONN_PROMPT)
            if reply:
                # 关闭连接
                self.close_conn(conn_id)
                conn_info = self.conns_dict[conn_id]
                delete_conn(conn_info.id)
                del self.conns_dict[conn_id]
                # 删除树元素
                # 树型部件的takeTopLevelItem方法可以从树型部件中删除对应项的节点并返回该项，语法：takeTopLevelItem(index)
                # 通过调用树型部件的indexOfTopLevelItem方法可以获得对应项在顶层项的位置，语法：indexOfTopLevelItem
                #
                # self.treeWidget.removeItemWidget，它从一个项中移除一个小部件，而不是QTreeWidgetItem。它对应于setItemWidget方法
                self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(item))

    def handle_db_menu(self, item, func):
        """右键菜单中关于数据库的处理"""
        # 打开数据库
        if func == OPEN_DB_MENU:
            self.open_tree_item(item)
        # 关闭数据库
        elif func == CLOSE_DB_MENU:
            self.close_tree_item(item)
        # 全选所有表
        elif func == SELECT_ALL_TB_MENU:
            self.set_check_state(item, QtCore.Qt.Checked)
        # 取消全选表
        elif func == UNSELECT_TB_MENU:
            self.set_check_state(item, QtCore.Qt.Unchecked)

    def handle_table_menu(self, item, func):
        """右键菜单关于表的处理"""
        # 打开表
        if func == OPEN_TABLE_MENU:
            self.get_tree_list()
        # 关闭表
        elif func == CLOSE_TABLE_MENU:
            self.close_table()
        # 全选字段
        elif func == SELECT_ALL_FIELD_MENU:
            self.change_table_checkbox(True)
        # 取消选择字段
        elif func == UNSELECT_FIELD_MENU:
            self.change_table_checkbox(False)
        # 生成
        elif func == GENERATE_MENU:
            pass

    def check_table_status(self, parent):
        """
        检查表是否被全选，被部分选中，第三种情况为都没有选中
        @:param parent: 在树部件中，表层次的父项，
        all_checked: 是否被全选
        parted_checked: 是否部分选中
        """
        all_checked, parted_checked = False, False
        # 如果数据库已经打开，再检测子项
        if parent.childCount():
            check_set = set()
            for index in range(parent.childCount()):
                # 将checkbox选中状态放入集合，状态只有选中与未选中，
                # 若集合元素为两个，则为部分选中，若为一个，取值判断。
                check_set.add(parent.child(index).checkState(0))
            if len(check_set) == 2:
                parted_checked = True
            elif check_set.pop() == QtCore.Qt.Checked:
                all_checked = True
        return all_checked, parted_checked

    def check_field_status(self, item):
        """
        检查字段是否全选
        all_checked: 是否被全选
        parted_checked: 是否部分选中
        """
        parted_check = False
        # 根据表头复选框状态判断是否全选
        all_checked = self.header.isOn
        # 如果表头没有全选，左侧表选中，证明是部分选中
        if not all_checked and item.checkState(0) == Qt.Checked:
            parted_check = True
        return all_checked, parted_check

    def set_check_state(self, parent, check_state):
        """设置树结构下父项下所有子项的选中状态"""
        for index in range(parent.childCount()):
            parent.child(index).setCheckState(0, check_state)

    def fill_menubar(self):
        self.file_menu = self.menubar.addMenu('文件')
        add_conn_menu(self)
        generate_menu(self)
        exit_app_menu(self)

        self.help_menu = self.menubar.addMenu('帮助')

    def add_conn(self):
        conn_info = Connection(None, None, None, None, None, None)
        self.show_conn_dialog(conn_info, ADD_CONN_MENU)

    def generate(self):...

    def quit(self):
        print("退出")
        self.main_window.close()

