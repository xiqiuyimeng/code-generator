# -*- coding: utf-8 -*-
"""
工具栏
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

_author_ = 'luwt'
_date_ = '2020/7/13 14:28'


def fill_tool_bar(gui):
    add_insert_conn_tool(gui)
    add_refresh_tool(gui)
    add_generate_tool(gui)
    add_exit_tool(gui)


def add_insert_conn_tool(gui):
    # 指定图标
    insert_tool = QAction(QIcon(':/icon/add.png'), '添加连接', gui)
    insert_tool.setStatusTip('在左侧列表中添加一条连接')
    insert_tool.triggered.connect(gui.add_conn)
    gui.toolBar.addAction(insert_tool)


def add_refresh_tool(gui):
    refresh_tool = QAction(QIcon(':/icon/refresh.png'), '刷新', gui)
    refresh_tool.setStatusTip('刷新')
    refresh_tool.setShortcut('F5')
    refresh_tool.triggered.connect(gui.refresh)
    gui.toolBar.addAction(refresh_tool)


def add_generate_tool(gui):
    generate_tool = QAction(QIcon(':/icon/exec.png'), '生成', gui)
    generate_tool.setStatusTip('根据选择执行生成命令')
    generate_tool.triggered.connect(gui.generate)
    gui.toolBar.addAction(generate_tool)


def add_exit_tool(gui):
    exit_tool = QAction(QIcon(':/icon/exit.png'), '退出程序', gui)
    exit_tool.setStatusTip('退出应用程序')
    exit_tool.triggered.connect(gui.quit)
    gui.toolBar.addSeparator()
    gui.toolBar.addAction(exit_tool)

