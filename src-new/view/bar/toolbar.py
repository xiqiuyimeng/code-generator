# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QAction

from view.bar.bar_function import open_conn_dialog
from view.custom_widget.draggable_widget import DraggableWidget

_author_ = 'luwt'
_date_ = '2022/5/7 12:43'


class ToolBar(QToolBar, DraggableWidget):

    def __init__(self, window):
        super().__init__(window)
        self.main_window = window
        self.setObjectName("toolbar")

        self.setIconSize(QSize(50, 40))
        # 设置名称显示在图标下面（默认本来是只显示图标）
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

    def fill_tool_bar(self):
        self.add_switch_source_tool()
        self.add_insert_conn_tool()
        self.add_refresh_tool()
        self.add_generate_tool()
        self.add_clear_tool()
        self.add_template_tool()
        self.add_exit_tool()

    def add_switch_source_tool(self):
        switch_tool = QAction(QIcon(':/icon/exec.png'), '切换数据源列表', self.main_window)
        switch_tool.setStatusTip('切换数据源列表')
        # switch_tool.triggered.connect()

        self.addSeparator()
        self.addAction(switch_tool)

    def add_insert_conn_tool(self):
        insert_tool = QAction(QIcon(':/icon/add.png'), '添加连接', self.main_window)
        insert_tool.setStatusTip('在左侧列表中添加一条连接')
        insert_tool.triggered.connect(lambda: open_conn_dialog(self.main_window.tree_widget,
                                                               self.main_window.geometry()))
        self.addAction(insert_tool)

    def add_refresh_tool(self):
        refresh_tool = QAction(QIcon(':/icon/refresh.png'), '刷新', self.main_window)
        refresh_tool.setStatusTip('刷新')
        refresh_tool.setShortcut('F5')
        # refresh_tool.triggered.connect(gui.refresh)

        self.addAction(refresh_tool)

    def add_generate_tool(self):
        generate_tool = QAction(QIcon(':/icon/exec.png'), '生成', self.main_window)
        generate_tool.setStatusTip('根据选择执行生成命令')
        # generate_tool.triggered.connect(gui.generate)

        self.addAction(generate_tool)

    def add_clear_tool(self):
        clear_tool = QAction(QIcon(':/icon/remove.png'), '清空选择', self.main_window)
        clear_tool.setStatusTip('清空所有已经选择的字段')
        # clear_tool.triggered.connect(gui.clear_selected)

        self.addSeparator()
        self.addAction(clear_tool)

    def add_template_tool(self):
        template_tool = QAction(QIcon(':/icon/template.png'), '模板设置', self.main_window)
        template_tool.setStatusTip('查看模板、修改模板、新建模板等操作')
        # template_tool.triggered.connect(gui.template_setting)
        self.addSeparator()

        self.addAction(template_tool)

    def add_exit_tool(self):
        exit_tool = QAction(QIcon(':/icon/exit.png'), '退出程序', self.main_window)
        exit_tool.setStatusTip('退出应用程序')
        exit_tool.triggered.connect(self.main_window.close)

        self.addSeparator()
        self.addAction(exit_tool)
