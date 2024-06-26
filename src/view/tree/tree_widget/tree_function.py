﻿# -*- coding: utf-8 -*-
"""
处理树节点相关操作
"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTreeWidgetItem, QApplication, QStyle

from src.constant.ds_type_constant import FOLDER_TYPE
from src.enum.common_enum import get_checked_enum
from src.enum.icon_enum import get_icon
from src.constant.tree_constant import ADD_CONN_DIALOG_TITLE, EDIT_CONN_DIALOG_TITLE, ADD_STRUCT_DIALOG_TITLE, \
    EDIT_STRUCT_DIALOG_TITLE, CREATE_NEW_FOLDER, EDIT_FOLDER_NAME
from src.enum.conn_type_enum import get_conn_dialog
from src.enum.struct_type_enum import get_struct_dialog, FolderTypeEnum
from src.service.util.tree_node_util import TreeData
from src.view.dialog.datasource.conn_dialog import *
from src.view.dialog.datasource.struct_dialog import *
from src.view.tree.tree_item.tree_item import TreeWidgetItem
from src.view.tree.tree_item.tree_item_func import set_item_opened_record, get_item_opened_record, \
    get_children_items, get_add_del_data
from src.view.window.main_window_func import get_sql_tree_widget, get_struct_tree_widget

_author_ = 'luwt'
_date_ = '2020/7/6 11:34'


def make_sql_tree_item(tree_widget, parent, name, icon, opened_item_record=None, check_value=None):
    """
    构造sql树的子项
    :param tree_widget: 树部件
    :param parent: 要构造子项的父节点元素
    :param name: 构造的子节点名称
    :param icon: 图标，该元素的展示图标对象
    :param opened_item_record: 打开记录表中的记录
    :param check_value: 构造的子节点的复选框状态值
    """
    item = TreeWidgetItem(tree_widget, parent)
    item.setIcon(0, icon)
    item.setText(0, name)
    if opened_item_record:
        set_item_opened_record(item, opened_item_record)
    if check_value is not None:
        item.setCheckState(0, get_checked_enum(check_value))
    return item


def make_display_tree_item(parent, name, icon):
    """
    构造sql树的子项
    :param parent: 要构造子项的父节点元素
    :param name: 构造的子节点名称
    :param icon: 图标，该元素的展示图标对象
    """
    item = QTreeWidgetItem(parent)
    item.setIcon(0, icon)
    item.setText(0, name)
    return item


def add_conn_func(sql_type):
    """
    添加连接，打开弹窗，接收输入，保存系统库
    :param sql_type: 用来标识sql数据源类型
    """
    show_conn_dialog(sql_type, get_sql_tree_widget(), None, ADD_CONN_DIALOG_TITLE)


def edit_conn_func(sql_type, tree_widget, conn_id):
    show_conn_dialog(sql_type, tree_widget, conn_id, EDIT_CONN_DIALOG_TITLE)


def show_conn_dialog(sql_type, tree_widget, conn_id, title):
    """
    打开添加、编辑连接子窗口
    :param sql_type: 用来标识sql数据源类型
    :param tree_widget: 树对象
    :param conn_id:若有id值，则认为操作为编辑操作，
        将在弹窗界面回显数据，若无数据，则为添加操作
    :param title: 弹窗的标题，与操作保持一致，不作为弹窗中回显数据标志，以conn_info为回显标志
    """
    conn_items = tree_widget.get_top_level_items()
    exists_conn_names = [get_item_opened_record(conn_item).item_name for conn_item in conn_items]
    # 根据类型，动态获取对话框
    dialog: ConnDialogABC = globals()[get_conn_dialog(sql_type)](title, exists_conn_names, conn_id)
    if title == ADD_CONN_DIALOG_TITLE:
        dialog.save_signal.connect(lambda opened_conn_record: add_conn_tree_item(tree_widget, opened_conn_record))
    elif title == EDIT_CONN_DIALOG_TITLE:
        dialog.edit_signal.connect(lambda conn_name: update_conn_tree_item(tree_widget, conn_name))
    dialog.exec()


def add_conn_tree_item(tree_widget, opened_conn_record):
    """
    添加树节点（连接），弹窗中点击确定后信号连接的槽函数，负责处理添加数据的操作
    :param tree_widget: 树对象
    :param opened_conn_record: 打开记录表中的连接信息
    """
    conn_type = opened_conn_record.data_type
    conn_icon = get_icon(conn_type.display_name)
    conn_item = make_sql_tree_item(tree_widget, tree_widget, opened_conn_record.item_name,
                                   conn_icon, opened_conn_record)
    # 添加顶层节点
    tree_widget.addTopLevelItem(conn_item)
    # 设置当前项
    tree_widget.set_selected_focus(conn_item)


def update_conn_tree_item(tree_widget, conn_name):
    """
    更新树节点，弹窗中点击确定后信号连接的槽函数，负责处理编辑数据的操作
    :param tree_widget: 树对象
    :param conn_name: 连接名称
    """
    item = tree_widget.currentItem()
    item.setText(0, conn_name)
    opened_record = get_item_opened_record(item)
    opened_record.item_name = conn_name
    # 这里需要同步更新下 tree_node 对象中的 conn_name，否则 tree_node 对象中取到的就是原来的连接名
    tree_widget.get_item_node(item).item_name = conn_name


def make_conn_tree_items(opened_items, parent):
    """
    根据本地保存的连接列表，构建树节点，在项目启动初始化时调用
    """
    for opened_item in opened_items:
        conn_icon = get_icon(opened_item.data_type.display_name)
        item = make_sql_tree_item(parent, parent, opened_item.item_name, conn_icon, opened_item)
        # 添加顶层节点
        parent.addTopLevelItem(item)


def make_db_items(tree_widget, parent_item, opened_db_items):
    """构建数据库层叶子节点"""
    icon = get_icon(opened_db_items[0].data_type.db_icon_name)
    for opened_db_item in opened_db_items:
        make_sql_tree_item(tree_widget, parent_item, opened_db_item.item_name, icon, opened_db_item)


def make_table_items(tree_widget, parent_item, opened_table_items, tree_data: TreeData):
    """构建数据表层叶子节点"""
    checked_table_opened_items = list()
    icon = get_icon(opened_table_items[0].data_type.tb_icon_name)
    for opened_table_item in opened_table_items:
        make_sql_tree_item(tree_widget, parent_item, opened_table_item.item_name, icon,
                           opened_table_item, check_value=opened_table_item.checked)
        if opened_table_item.checked:
            checked_table_opened_items.append(opened_table_item)
    # 如果表已选中，添加到选中数据集合中
    if checked_table_opened_items:
        tb_data = get_add_del_data(parent_item)
        tb_data[max(tb_data) + 1] = checked_table_opened_items
        tree_data.add_node(tb_data)


def check_table_status(parent):
    """
    检查表是否被全选，被部分选中，第三种情况为都没有选中
    :param parent: 在树部件中，表层次的父项，
    :return all_checked: 是否被全选
            parted_checked: 是否部分选中
    """
    all_checked, parted_checked = False, False
    # 如果数据库已经打开，再检测子项
    if parent.childCount():
        check_set = set()
        for index in range(parent.childCount()):
            # 将checkbox选中状态放入集合，状态有选中、部分选中与未选中，
            # 若集合元素为两个，则为部分选中，若为一个，取值判断。
            check_set.add(parent.child(index).checkState(0))
        if Qt.CheckState.PartiallyChecked in check_set or len(check_set) > 1:
            parted_checked = True
        elif len(check_set) == 1 and check_set.pop() == Qt.CheckState.Checked:
            all_checked = True
    return all_checked, parted_checked


# ------------------------- 结构体使用方法 -------------------------#

def add_struct_func(struct_type, parent_opened_item, parent_item):
    """
    添加结构体，打开弹窗，接收输入，保存系统库
    :param struct_type: 用来标识结构体数据源类型
    :param parent_opened_item 上级节点的打开记录
    :param parent_item 上级节点
    """
    show_struct_dialog(struct_type, get_struct_tree_widget(), None, ADD_STRUCT_DIALOG_TITLE,
                       parent_opened_item, parent_item)


def edit_struct_func(struct_type, tree_widget, opened_struct_id):
    show_struct_dialog(struct_type, tree_widget, opened_struct_id, EDIT_STRUCT_DIALOG_TITLE)


def get_struct_parent_item(tree_widget, parent_item):
    # 如果父节点为空，动态获取当前节点为父节点
    if parent_item is None:
        cur_item = tree_widget.currentItem()
        # 如果不存在当前项，那么取树本身
        if cur_item is None:
            return tree_widget, tree_widget.top_item
        # 如果当前节点不是文件夹类型，那么应该向上找一层
        if get_item_opened_record(cur_item).data_type is not FolderTypeEnum.folder_type.value:
            return do_get_struct_parent_item(tree_widget, cur_item)
        else:
            return cur_item, get_item_opened_record(cur_item)
    # 如果当前节点不为空，且不是文件夹类型，那么应该向上找一层
    elif get_item_opened_record(parent_item).data_type is not FolderTypeEnum.folder_type.value:
        return do_get_struct_parent_item(tree_widget, parent_item)


def do_get_struct_parent_item(tree_widget, parent_item):
    # 如果当前节点上一层为空，说明当前节点为顶层节点，那么父节点是树本身
    cur_parent_item = parent_item.parent()
    if cur_parent_item is None:
        parent_item = tree_widget
        parent_opened_item = tree_widget.top_item
    else:
        # 当前节点上一层不为空，取上层节点为父节点
        parent_item = cur_parent_item
        parent_opened_item = get_item_opened_record(cur_parent_item)
    return parent_item, parent_opened_item


def show_struct_dialog(struct_type, tree_widget, opened_struct_id, title,
                       parent_opened_item=None, parent_item=None):
    """
    打开添加、编辑结构体子窗口
    :param struct_type: 用来标识结构体数据源类型
    :param tree_widget: 树对象
    :param opened_struct_id: 结构体对应打开记录的id值，若存在则认为操作为编辑操作，
        将在弹窗界面回显数据，若无数据，则为添加操作
    :param title: 弹窗的标题，与操作保持一致，不作为弹窗中回显数据标志，以conn_info为回显标志
    :param parent_opened_item 上级节点的打开记录
    :param parent_item 上级节点
    """
    # 动态智能获取父节点，父节点打开记录项
    if parent_item is None:
        parent_item, parent_opened_item = get_struct_parent_item(tree_widget, parent_item)
    # 获取当前不允许重复的名称列表
    exists_struct_names = get_exists_struct_names(tree_widget, parent_opened_item, parent_item)
    # 根据类型，动态获取对话框
    dialog: StructDialogABC = globals()[get_struct_dialog(struct_type)](title, exists_struct_names,
                                                                        opened_struct_id, tree_widget,
                                                                        parent_opened_item)
    if title == ADD_STRUCT_DIALOG_TITLE:
        dialog.save_signal.connect(lambda opened_struct_record: add_struct_tree_item(tree_widget, parent_item,
                                                                                     opened_struct_record,
                                                                                     struct_type))

    elif title == EDIT_STRUCT_DIALOG_TITLE:
        dialog.edit_signal.connect(lambda struct_name: update_struct_tree_item(tree_widget, struct_name))
    dialog.exec()


def add_folder_func(tree_widget):
    """
    添加文件夹
    :param tree_widget: 树对象
    """
    parent_item, parent_opened_item = get_struct_parent_item(tree_widget, None)
    show_folder_dialog(tree_widget, parent_opened_item, CREATE_NEW_FOLDER, OpenedTreeItem(), parent_item)


def edit_folder_func(tree_widget, parent_opened_item, folder_info, parent_item):
    show_folder_dialog(tree_widget, parent_opened_item, EDIT_FOLDER_NAME, folder_info, parent_item)


def get_exists_struct_names(tree_widget, parent_opened_item, parent_item):
    # 根据节点层次，获取子节点，得到当前不允许重复的名称列表
    if parent_opened_item is tree_widget.top_item:
        children_items = tree_widget.get_top_level_items()
    else:
        children_items = get_children_items(parent_item)
    return [get_item_opened_record(child_item).item_name for child_item in children_items]


def show_folder_dialog(tree_widget, parent_opened_item, dialog_title, folder_info, parent_item):
    """
    打开文件夹对话框
    :param tree_widget: 树对象
    :param parent_opened_item: 父节点的 opened item 对象，用来构造子节点 opened item 信息
    :param dialog_title: 对话框标题
    :param folder_info: 文件夹信息，也就是 opened item 对象
    :param parent_item: 树结构中的父节点
    """
    # 根据节点层次，获取子节点，得到当前不允许重复的名称列表
    exists_folder_names = get_exists_struct_names(tree_widget, parent_opened_item, parent_item)
    # 打开对话框
    folder_dialog = FolderDialog(dialog_title, exists_folder_names, folder_info, parent_opened_item)
    if dialog_title == CREATE_NEW_FOLDER:
        folder_dialog.save_signal.connect(lambda folder_item: add_struct_tree_item(tree_widget, parent_item,
                                                                                   folder_item, FOLDER_TYPE))
    elif dialog_title == EDIT_FOLDER_NAME:
        folder_dialog.edit_signal.connect(lambda folder_name: update_struct_tree_item(tree_widget, folder_name))
    folder_dialog.exec()


def make_struct_tree_item(tree_widget, parent, name, icon, check_value, opened_item_record):
    """
    构造结构体树的子项
    :param tree_widget: 树组件
    :param parent: 要构造子项的父节点元素
    :param name: 构造的子节点名称
    :param icon: 图标，该元素的展示图标对象
    :param opened_item_record: 打开记录表中的记录
    :param check_value: 构造的子节点的复选框状态值
    """
    item = TreeWidgetItem(tree_widget, parent)
    item.setIcon(0, icon)
    item.setText(0, name)
    item.setCheckState(0, get_checked_enum(check_value))
    set_item_opened_record(item, opened_item_record)
    return item


def add_struct_tree_item(tree_widget, parent, opened_item_record, struct_type):
    """
    添加结构体树节点
    :param tree_widget: 树对象
    :param parent: 父节点
    :param opened_item_record: 打开记录表中记录
    :param struct_type: 结构体类型，文件夹或具体结构体，以此确定icon
    """
    # 如果是文件夹，使用默认图标
    icon = get_icon(struct_type) \
        if struct_type != FOLDER_TYPE else QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
    struct_item = make_struct_tree_item(tree_widget, parent, opened_item_record.item_name,
                                        icon, opened_item_record.checked, opened_item_record)
    struct_item.setExpanded(opened_item_record.expanded)
    if tree_widget is parent:
        # 如果父节点是树本身，那么添加顶层节点
        tree_widget.addTopLevelItem(struct_item)
    elif not tree_widget.reopening_flag:
        # 展开父节点
        parent.setExpanded(True)
    # 如果是结构体节点，置为当前项
    if struct_type != FOLDER_TYPE:
        tree_widget.setCurrentItem(struct_item)
    # 由于添加新的项以后，可能导致父节点复选框状态变化，所以需要联动父节点
    if not tree_widget.reopening_flag:
        tree_widget.link_parent_node(struct_item)
    # 如果节点是选中状态，添加到选中数据中
    if opened_item_record.checked:
        add_data = get_add_del_data(struct_item)
        tree_widget.tree_data.add_node(add_data)


def update_struct_tree_item(tree_widget, item_name):
    item = tree_widget.currentItem()
    item.setText(0, item_name)
    opened_item = get_item_opened_record(item)
    opened_item.item_name = item_name
    # 如果节点是选中或部分选中状态，更新选中数据中的名称
    check_state = item.checkState(0)
    if check_state == Qt.CheckState.Checked or check_state == Qt.CheckState.PartiallyChecked:
        update_data = get_add_del_data(item)
        tree_widget.tree_data.update_node_name(update_data)
    # 同sql连接节点，这里也需要同步更新下 tree_node 对象中的 结构体名称
    tree_widget.get_item_node(item).item_name = item_name
