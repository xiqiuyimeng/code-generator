# -*- coding: utf-8 -*-
"""
处理表格控件动作
"""
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from table_header import all_header_combobox
_author_ = 'luwt'
_date_ = '2020/7/2 16:17'


# 已选中集合
checked_set = set()


def fill_table(gui, cols, checked):
    """将列名字段全数填充在表中，四列多行表"""
    # 显示列标题
    gui.tableWidget.horizontalHeader().setVisible(True)
    clear_table(gui)
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
            gui.update_tree_item_name(item, field)


def change_table_checkbox(gui, checked):
    """改变表格中checkbox中所有复选框状态，换言之，全选或清空选择"""
    # 通过表头是否展示，判定表是否已经展示
    visible = gui.tableWidget.horizontalHeader().isVisible()
    if visible:
        gui.table_header.set_header_checked(checked)
        gui.table_header.change_state(checked)


def close_table(gui):
    """关闭右侧表格"""
    # 删除表格内容
    clear_table(gui)
    # 隐藏表头
    gui.tableWidget.horizontalHeader().setVisible(False)


def clear_table(gui):
    """清空右侧表格"""
    [gui.tableWidget.removeRow(0) for r in range(gui.tableWidget.rowCount())]
    # 清空选中集合
    checked_set.clear()
    all_header_combobox.clear()
    gui.table_header.set_header_checked(False)


def on_cell_changed(gui, row, col):
    """第一列checkbox状态改变时触发"""
    if col == 0:
        # 检查第一列，checkbox选中状态
        item = gui.tableWidget.item(row, col)
        # 如果有选中的checkbox
        # todo 暂时只能通过判断 row 不在选中集合中来处理下面的操作。
        #  如果不处理，在选择第二个表的全选时，将会重复调用本方法，第三个表全选将会重复调用本方法三次 。。。
        #  目前没找到原因，只能先简单判断处理下。未选中的状态加入的 row判断也是因此。
        if item.checkState() == Qt.Checked and row not in checked_set:
            # 表格总行数
            count = gui.tableWidget.rowCount()
            # 将选中的行号加入选中行列表中
            checked_set.add(row)
            # 取出选中行的字段名称
            data = gui.tableWidget.item(row, 1).text()
            print(f'{row}行 选中了 -> {data}：{checked_set}')
            # 状态栏
            gui.statusbar.showMessage(f'{row}行 选中了 -> {data}：{checked_set}')
            # 如果选中行列表元素个数等于表格总行数
            if count == len(checked_set):
                # 全选按钮应该选中，设置表头复选框按钮状态为选中
                gui.table_header.set_header_checked(True)
            # 设置左侧树部件中，对应表也应为选中状态
            gui.current_table.setCheckState(0, Qt.Checked)
        elif item.checkState() == Qt.Unchecked and row in checked_set:
            # 设置表头复选框按钮状态为未选中
            gui.table_header.set_header_checked(False)
            if checked_set:
                # 清空选中集合
                if row in checked_set:
                    checked_set.remove(row)
                # 设置左侧树部件中，对应表为未选中状态
                if len(checked_set) == 0:
                    gui.current_table.setCheckState(0, Qt.Unchecked)
                data = gui.tableWidget.item(row, 1).text()
                print(f'{row}行 撤销选中 -> {data} : {checked_set}')
                # 状态栏
                gui.statusbar.showMessage(f'{row}行 撤销选中 -> {data} : {checked_set}')
