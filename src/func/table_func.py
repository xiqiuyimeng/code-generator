# -*- coding: utf-8 -*-
"""
处理表格控件动作
"""
import sip
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView

from src.constant_.constant import TABLE_HEADER_LABELS
from src.scrollable_widget.scrollable_widget import MyTableWidget
from src.table.table_header import CheckBoxHeader
from src.table.table_item import MyTableWidgetItem

_author_ = 'luwt'
_date_ = '2020/7/2 16:17'


def add_table(gui, tree_item):
    """添加表格"""
    gui.tab_frame = QtWidgets.QFrame(gui.centralwidget)
    gui.tab_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
    gui.tab_frame.setFrameShadow(QtWidgets.QFrame.Raised)
    gui.tab_frame.setObjectName("table_frame")
    gui.table_verticalLayout = QtWidgets.QVBoxLayout(gui.tab_frame)
    gui.table_verticalLayout.setObjectName("table_verticalLayout")
    gui.tab_header_label = QtWidgets.QLabel(gui.tab_frame)
    gui.tab_header_label.setObjectName("table_header_label")
    gui.table_verticalLayout.addWidget(gui.tab_header_label)

    gui.tableWidget = MyTableWidget(gui.tab_frame)
    gui.tableWidget.setObjectName("tableWidget")
    gui.tableWidget.setAttribute(Qt.WA_TranslucentBackground, True)
    # 在布局中添加表格
    gui.table_verticalLayout.addWidget(gui.tableWidget)
    gui.horizontalLayout.addWidget(gui.tab_frame)
    # 设置只读表格
    gui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    # 交替行颜色
    gui.tableWidget.setAlternatingRowColors(True)
    # 处理一些其他信息
    add_table_ext_info(gui, tree_item)
    # 创建表格列标题，共四列
    make_table_header(gui)


def add_table_ext_info(gui, tree_item):
    # 表格复选框改变事件
    gui.tableWidget.item_checkbox_clicked.connect(gui.on_table_check_changed)
    gui.current_table = tree_item
    tb_name = tree_item.text(0)
    db_name = tree_item.parent().text(0)
    conn_name = tree_item.parent().parent().text(0)
    # 标题
    gui.tab_header_label.setText(f"当前展示表为：{tb_name}")
    # 状态栏提示
    gui.statusbar.showMessage(f"当前展示的表为：{tb_name}")
    # 设置气泡提示
    gui.tableWidget.setToolTip(f'当前表为{tb_name}')
    # 已经打开的表，记录下连接名、库名和表名
    gui.opened_table = conn_name, db_name, tb_name


def make_table_header(gui):
    """设置表格列标题"""
    # 表格设置为4列
    gui.tableWidget.setColumnCount(4)
    # 实例化自定义表头
    gui.table_header = CheckBoxHeader()
    gui.table_header.setObjectName("table_header")
    # 设置表头
    gui.tableWidget.setHorizontalHeader(gui.table_header)
    # 设置表头字段
    gui.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
    # 设置表头列宽度，第一列全选列
    gui.tableWidget.horizontalHeader().resizeSection(0, 60)
    # 第二列字段列，根据大小自动调整宽度
    gui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
    # 最后备注列拉伸到最大
    gui.tableWidget.horizontalHeader().setStretchLastSection(True)
    # 默认行号隐藏
    gui.tableWidget.verticalHeader().setHidden(True)
    # 表头复选框单击信号与槽
    gui.table_header.select_all_clicked.connect(gui.all_selected_table_cols)


def close_table(gui):
    """
    关闭右侧表格
    :param gui: 启动的主窗口界面对象
    """
    # 在布局中移除表格
    gui.horizontalLayout.removeWidget(gui.tab_frame)
    # 必须调用sip才能彻底删除
    sip.delete(gui.tab_frame)
    # 删除table_frame属性，方便后续判断
    del gui.tab_frame
    gui.table_header.all_header_combobox.clear()
    # 重置打开表
    gui.opened_table = tuple()
    gui.statusbar.showMessage(f"成功关闭表：{gui.current_table.text(0)}")


def fill_table(gui, cols, selected_cols):
    """
    将列名字段全数填充在表中，四列多行表
    :param gui: 启动的主窗口界面对象
    :param cols: 字段信息的数组，为二维数组
    :param selected_cols: 已经选中的字段，如果为空，则证明是未选择。
        如果列表中有值，应将此数组中包含的字段复选框置为选中，其余未选中。
    """
    # 将当前表的列放入列表中
    gui.current_cols = list(map(lambda x: x[0], cols))
    # 填充数据
    for i, col in enumerate(cols):
        # 插入新的一行
        gui.tableWidget.insertRow(i)
        # 设置checkbox在第一列
        table_check_item = MyTableWidgetItem(gui.tableWidget)
        if selected_cols is None:
            check_status = Qt.Unchecked
        else:
            selected_col_list = list(map(lambda x: x[1], selected_cols))
            if col[0] in selected_col_list:
                check_status = Qt.Checked
            else:
                check_status = Qt.Unchecked
        table_check_item.setCheckState(check_status)
        # 加上行号
        table_check_item.setText(i + 1)
        gui.tableWidget.setItem(i, 0, table_check_item)
        gui.table_header.all_header_combobox.append(table_check_item)

        for n, field in enumerate(col, start=1):
            # 建立一个新的对象，赋值，填充到表格中对应位置
            item = MyTableWidgetItem(gui.tableWidget)
            item.setText(field)
            gui.tableWidget.setItem(i, n, item)
    # 设置表格根据内容调整行高
    gui.tableWidget.resizeRowsToContents()


def change_table_checkbox(gui, item, checked):
    """
    改变表格中checkbox中所有复选框状态，换言之，全选或清空选择，单纯改变页面效果
    :param gui: 启动的主窗口界面对象
    :param item: 当前点击树节点元素，必须是表级别
    :param checked: 复选框选中状态
    """
    # 判断表是否已经打开
    if check_table_opened(gui, item):
        gui.table_header.set_header_checked(checked)
        gui.table_header.change_state(checked)


def check_table_opened(gui, item):
    """
    检查表是否展示：首先检查表格是否存在，其次表头是否是显示状态，
    最后检查当前表是否是当前点击元素，如果都满足则为打开状态。
    如果前两项满足，而第三项不满足，则可能展示的是其他表
    :param gui: 启动的主窗口界面对象
    :param item: 当前点击树节点，必须是表级别
    """
    return hasattr(gui, 'table_frame') \
        and gui.current_table is item


def get_node(item):
    conn_id = item.parent().parent().text(1)
    conn_name = item.parent().parent().text(0)
    db_name = item.parent().text(0)
    tb_name = item.text(0)
    return conn_id, conn_name, db_name, tb_name

