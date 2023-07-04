# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/5/23 12:11'


# 维护主窗口，方便其他窗口使用
main_window = ...


def set_window(window):
    global main_window
    main_window = window


def get_window():
    return main_window


def get_window_geometry():
    return main_window.geometry()


# 维护树、tab引用
sql_tree_widget = ...
struct_tree_widget = ...
sql_tab_widget = ...
struct_tab_widget = ...


def set_sql_tree_widget(tree_widget):
    global sql_tree_widget
    sql_tree_widget = tree_widget


def get_sql_tree_widget():
    return sql_tree_widget


def set_struct_tree_widget(tree_widget):
    global struct_tree_widget
    struct_tree_widget = tree_widget


def get_struct_tree_widget():
    return struct_tree_widget


def set_sql_tab_widget(tab_widget):
    global sql_tab_widget
    sql_tab_widget = tab_widget


def get_sql_tab_widget():
    return sql_tab_widget


def set_struct_tab_widget(tab_widget):
    global struct_tab_widget
    struct_tab_widget = tab_widget


def get_struct_tab_widget():
    return struct_tab_widget
