# -*- coding: utf-8 -*-
"""
处理表格控件动作
"""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem

from selected_data import SelectedData
from table_header import all_header_combobox

_author_ = 'luwt'
_date_ = '2020/7/2 16:17'


def fill_table(gui, cols, checked):
    """
    将列名字段全数填充在表中，四列多行表
    :param gui: 启动的主窗口界面对象
    :param cols: 列信息的数组，为二维数组
    :param checked: 表格中复选框状态，作为初始化复选框依据
    """
    # 显示列标题
    gui.table_header.setVisible(True)
    # 将当前表的列放入列表中
    gui.current_cols = list(map(lambda x: x[0], cols))
    print(gui.current_cols)
    # 填充数据
    for i, col in enumerate(cols):
        # 插入新的一行
        gui.tableWidget.insertRow(i)
        # 设置checkbox在第一列
        check = QTableWidgetItem()
        check.setCheckState(checked)
        gui.tableWidget.setItem(i, 0, check)
        all_header_combobox.append(check)

        for n, field in enumerate(col, start=1):
            # 建立一个新的对象，赋值，填充到表格中对应位置
            item = QTableWidgetItem()
            gui.tableWidget.setItem(i, n, item)
            gui.update_table_item(item, field)


def change_table_checkbox(gui, checked):
    """
    改变表格中checkbox中所有复选框状态，换言之，全选或清空选择
    :param gui: 启动的主窗口界面对象
    :param checked: 复选框选中状态
    """
    # 通过表头是否展示，判定表是否已经展示
    visible = gui.table_header.isVisible()
    if visible:
        gui.table_header.set_header_checked(checked)
        gui.table_header.change_state(checked)


def close_table(gui):
    """
    关闭右侧表格
    :param gui: 启动的主窗口界面对象
    """
    # 删除表格内容
    clear_table(gui)
    # 隐藏表头
    gui.table_header.setVisible(False)


def clear_table(gui):
    """
    清空右侧表格，也一并清空选中的字段集合
    :param gui: 启动的主窗口界面对象
    """
    [gui.tableWidget.removeRow(0) for r in range(gui.tableWidget.rowCount())]
    all_header_combobox.clear()
    gui.table_header.set_header_checked(False)


def on_cell_changed(gui, row, col):
    """
    第一列checkbox状态改变时触发
    :param gui 启动的主窗口界面对象
    :param row 表格中当前行
    :param col 表格中当前列
    """
    if col == 0 and gui.tableWidget.item(row, 1):
        print(row)
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
            # 如果选中字段个数等于表格总行数
            if count == len(checked_list):
                # 全选按钮应该选中，设置表头复选框按钮状态为选中
                gui.table_header.set_header_checked(True)
            # 设置左侧树部件中，对应表也应为选中状态
            gui.current_table.setCheckState(0, Qt.Checked)
        elif item.checkState() == Qt.Unchecked:
            # 设置表头复选框按钮状态为未选中
            gui.table_header.set_header_checked(False)
            # 删除字段
            SelectedData().unset_cols(gui, conn_name, db_name, tb_name, (field, ))
            checked_list = SelectedData().get_col_list(conn_name, db_name, tb_name, True)
            # 设置左侧树部件中，对应表为未选中状态
            if checked_list is None:
                gui.current_table.setCheckState(0, Qt.Unchecked)


def get_node(item):
    conn_name = item.parent().parent().text(0)
    db_name = item.parent().text(0)
    tb_name = item.text(0)
    return conn_name, db_name, tb_name
