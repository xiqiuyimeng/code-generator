# -*- coding: utf-8 -*-
"""
处理树节点相关操作
"""
from PyQt5.QtGui import QIcon

from src.constant_.constant import ADD_CONN_MENU, EDIT_CONN_MENU
from src.dialog.conn_dialog import ConnDialog
from src.sys.sys_info_storage.conn_sqlite import Connection
from src.tree.tree_item import MyTreeWidgetItem

_author_ = 'luwt'
_date_ = '2020/7/6 11:34'


def make_tree_item(gui, parent, name, icon, item_id=None, checkbox=None):
    """
    构造树的子项
    :param gui: 启动的主窗口界面对象
    :param parent: 要构造子项的父节点元素
    :param name: 构造的子节点名称
    :param icon: 图标，该元素的展示图标对象
    :param item_id: 构造的子节点隐藏属性id，可无
    :param checkbox: 构造的子节点的复选框，可无。若存在，将当前状态写入第三列中
    """
    item = MyTreeWidgetItem(gui.treeWidget, parent)
    item.setIcon(0, icon)
    item.setText(0, name)
    if item_id:
        # id 作为隐藏属性，写于第二列
        item.setText(1, item_id)
    if checkbox is not None:
        item.setCheckState(0, checkbox)
    return item


def add_conn_func(gui, screen_rect):
    """
    添加连接，打开弹窗，接收输入，保存系统库
    :param gui: 启动的主窗口界面对象
    :param screen_rect: 主窗口大小
    """
    conn_info = Connection(*((None,) * len(Connection._fields)))
    show_conn_dialog(gui, conn_info, ADD_CONN_MENU, screen_rect)


def show_conn_dialog(gui, conn_info, title, screen_rect):
    """
    打开添加、编辑连接子窗口
    :param gui: 启动的主窗口界面对象
    :param conn_info: Connection对象，若该对象有id值，则认为操作为编辑操作，
        将在弹窗界面回显数据，若无数据，则为添加操作
    :param title: 弹窗的标题，与操作保持一致，不作为弹窗中回显数据标志，以conn_info为回显标志
    :param screen_rect: 主窗口大小
    """
    dialog = ConnDialog(conn_info, title, screen_rect)
    if title == ADD_CONN_MENU:
        dialog.conn_signal.connect(lambda conn: add_conn_tree_item(gui, conn))
    elif title == EDIT_CONN_MENU:
        dialog.conn_signal.connect(lambda conn: update_conn_tree_item(gui, conn))
    dialog.exec()


def add_conn_tree_item(gui, connection):
    """
    添加树节点（连接），弹窗中点击确定后信号连接的槽函数，负责处理添加数据的操作
    :param gui: 启动的主窗口界面对象
    :param connection: 弹窗中信号发射的连接对象，带有用户填写的信息
    """
    gui.display_conn_dict[connection.id] = connection
    icon = QIcon(":/icon/mysql_conn_icon.png")
    make_tree_item(gui, gui.treeWidget, connection.name, icon, connection.id)


def update_conn_tree_item(gui, connection):
    """
    更新树节点，弹窗中点击确定后信号连接的槽函数，负责处理编辑数据的操作
    :param gui: 启动的主窗口界面对象
    :param connection: 弹窗中信号发射的连接对象，带有用户填写的信息
    """
    gui.display_conn_dict[connection.id] = connection
    item = gui.treeWidget.currentItem()
    item.setText(0, connection.name)
