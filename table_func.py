# -*- coding: utf-8 -*-
"""
处理表格控件动作
"""
import sip
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from constant import TABLE_HEADER_LABELS
from selected_data import SelectedData
from table_header import all_header_combobox, CheckBoxHeader

_author_ = 'luwt'
_date_ = '2020/7/2 16:17'


def add_table(gui):
    """添加表格"""
    gui.tableWidget = QtWidgets.QTableWidget(gui.centralwidget)
    gui.tableWidget.setObjectName("tableWidget")
    # 创建表格列标题，共四列
    make_table_header(gui)

    # 设置只读表格
    gui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    # 让表格铺满整个控件
    gui.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
    # 在布局中添加表格
    gui.horizontalLayout.addWidget(gui.tableWidget)
    # 交替行颜色
    gui.tableWidget.setAlternatingRowColors(True)


def make_table_header(gui):
    """设置表格列标题"""
    # 表格设置为4列
    gui.tableWidget.setColumnCount(4)
    # 实例化自定义表头
    gui.table_header = CheckBoxHeader()
    # 设置表头
    gui.tableWidget.setHorizontalHeader(gui.table_header)
    # 设置表头字段
    gui.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
    # 表头复选框单击信号与槽
    gui.table_header.select_all_clicked.connect(gui.table_header.change_state)


def close_table(gui):
    """
    关闭右侧表格
    :param gui: 启动的主窗口界面对象
    """
    # 在布局中移除表格
    gui.horizontalLayout.removeWidget(gui.tableWidget)
    # 必须调用sip才能彻底删除
    sip.delete(gui.tableWidget)
    # 删除tableWidget属性，方便后续判断
    del gui.tableWidget
    all_header_combobox.clear()
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
        check = QTableWidgetItem()
        if selected_cols is None:
            check_status = Qt.Unchecked
        else:
            if col[0] in selected_cols:
                check_status = Qt.Checked
            else:
                check_status = Qt.Unchecked
        check.setCheckState(check_status)
        gui.tableWidget.setItem(i, 0, check)
        all_header_combobox.append(check)

        for n, field in enumerate(col, start=1):
            # 建立一个新的对象，赋值，填充到表格中对应位置
            item = QTableWidgetItem()
            gui.tableWidget.setItem(i, n, item)
            gui.update_table_item(item, field)


def change_table_checkbox(gui, item, checked):
    """
    改变表格中checkbox中所有复选框状态，换言之，全选或清空选择
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
    return hasattr(gui, 'tableWidget') \
        and gui.current_table is item


def on_cell_changed(gui, row, col):
    """
    第一列checkbox状态改变时触发
    :param gui 启动的主窗口界面对象
    :param row 表格中当前行
    :param col 表格中当前列
    """
    if col == 0:
        # 检查第一列，checkbox选中状态
        item = gui.tableWidget.item(row, col)
        # 获取当前打开表对应的树控件中的信息
        conn_name, db_name, tb_name = get_node(gui.current_table)
        # 取出选中行的字段名称
        field = gui.tableWidget.item(row, 1).text()
        # 如果有选中的checkbox
        if item.checkState() == Qt.Checked:
            # 表格总行数
            count = gui.tableWidget.rowCount()
            # 已选字段保存
            SelectedData().set_cols(gui, conn_name, db_name, tb_name, (field, ))
            checked_list = SelectedData().get_col_list(conn_name, db_name, tb_name)
            # 如果选中字段个数等于表格总行数，且表头复选框未选中
            if count == len(checked_list) and not gui.table_header.isOn:
                # 全选按钮应该选中，设置表头复选框按钮状态为选中
                gui.table_header.set_header_checked(True)
            # 设置左侧树部件中，对应表也应为选中状态
            gui.current_table.setCheckState(0, Qt.Checked)
            # 当前item为表格项，下面更新的是树控件中的项，需要将当前表对应的树节点更新即可
            gui.update_tree_item_name(gui.current_table, str(Qt.Checked), 2)
        elif item.checkState() == Qt.Unchecked:
            # 设置表头复选框按钮状态为未选中
            gui.table_header.set_header_checked(False)
            # 删除字段
            SelectedData().unset_cols(gui, conn_name, db_name, tb_name, (field, ))
            checked_list = SelectedData().get_col_list(conn_name, db_name, tb_name, True)
            # 设置左侧树部件中，对应表为未选中状态
            if checked_list is None:
                gui.current_table.setCheckState(0, Qt.Unchecked)
                # 当前item为表格项，下面更新的是树控件中的项，需要将当前表对应的树节点更新即可
                gui.update_tree_item_name(gui.current_table, str(Qt.Unchecked), 2)


def get_node(item):
    conn_name = item.parent().parent().text(0)
    db_name = item.parent().text(0)
    tb_name = item.text(0)
    return conn_name, db_name, tb_name
