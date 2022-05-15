# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar, QFrame, QLabel, \
    QAbstractItemView, QHeaderView, QSplitter

from src.constant.constant import TABLE_HEADER_LABELS
from view.bar.menubar import Menubar
from view.bar.titlebar import TitleBar
from view.bar.toolbar import ToolBar
from view.table.table_header import CheckBoxHeader
from view.table.table_widget import TableWidget
from view.tree.tree_widget import TreeWidget

_author_ = 'luwt'
_date_ = '2022/5/7 10:04'


class MainWindow(QMainWindow):

    def __init__(self, screen_rect):
        super().__init__()
        # 当前屏幕的分辨率大小
        self.desktop_screen_rect = screen_rect

        # 主控件，用以包含所有内容
        self.main_widget = ...
        self.main_layout = ...

        # 定义中心控件，用以包含主体内容
        self.central_widget = ...
        self.central_layout = ...

        # 定义水平方向分割器
        self.horizontal_splitter = ...

        # 菜单栏、标题栏、工具栏、状态栏
        self.menubar = ...
        self.titlebar = ...
        self.toolbar = ...
        self.statusbar = ...

        # 左侧树结构
        self.tree_frame = ...
        self.tree_layout = ...
        self.tree_header_label = ...
        self.tree_widget = ...

        # 右侧表结构
        self.table_frame = ...
        self.table_layout = ...
        self.table_header = ...
        self.table_header_label = ...
        self.table_widget = ...

        self.setup_ui()
        self.connect_signal()

    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 按当前分辨率计算窗口大小
        self.resize(self.desktop_screen_rect.width() * 0.6, self.desktop_screen_rect.height() * 0.75)
        # 不透明度
        self.setWindowOpacity(0.95)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        # 设置所有间距为0
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.central_widget = QWidget()
        self.central_widget.setObjectName('central_widget')
        self.central_layout = QHBoxLayout(self.central_widget)
        self.horizontal_splitter = QSplitter(self.central_widget)
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        self.central_layout.addWidget(self.horizontal_splitter)

        self.setup_bars()
        self.setup_tree()
        self.setup_table()

        # 主布局添加所有部件，依次为标题栏、菜单栏、工具栏、承载了实际窗口内容的主控件，将窗口中央控件设置为包含所有的控件
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.central_widget)
        self.setCentralWidget(self.main_widget)

    def setup_bars(self):
        # 菜单栏
        self.menubar = Menubar(self)
        self.menubar.setObjectName("menubar")
        self.menubar.fill_menu_bar()

        # 创建标题栏
        self.titlebar = TitleBar(30, self, self.menubar)
        self.titlebar.setObjectName("titlebar")
        self.titlebar.setFixedWidth(self.width())

        # 工具栏
        self.toolbar = ToolBar(self)
        self.toolbar.fill_tool_bar()

        # 状态栏
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # 任务栏图标
        self.setWindowIcon(QIcon(":/icon/exec.png"))

    def setup_tree(self):
        self.tree_frame = QFrame(self.horizontal_splitter)
        self.tree_frame.setFrameShape(QFrame.StyledPanel)
        self.tree_frame.setFrameShadow(QFrame.Raised)
        self.tree_frame.setObjectName('tree_frame')

        self.tree_layout = QVBoxLayout(self.tree_frame)
        self.tree_header_label = QLabel(self.tree_frame)
        self.tree_header_label.setObjectName('tree_header_label')
        self.tree_layout.addWidget(self.tree_header_label)

        self.tree_widget = TreeWidget(self.tree_frame)
        self.tree_widget.setObjectName('tree_widget')
        self.tree_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.tree_layout.addWidget(self.tree_widget)
        self.tree_widget.headerItem().setHidden(True)
        # 统一设置图标大小
        self.tree_widget.setIconSize(QSize(40, 30))

    def setup_table(self):
        self.table_frame = QFrame(self.horizontal_splitter)
        self.table_frame.setFrameShape(QFrame.StyledPanel)
        self.table_frame.setFrameShadow(QFrame.Raised)
        self.table_frame.setObjectName('table_frame')

        self.table_layout = QVBoxLayout(self.table_frame)
        self.table_header_label = QLabel(self.table_frame)
        self.table_header_label.setObjectName('table_header_label')
        self.table_layout.addWidget(self.table_header_label)

        self.table_widget = TableWidget(self.table_frame)
        self.table_widget.setObjectName('table_widget')
        self.table_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.table_layout.addWidget(self.table_widget)

        # 设置只读表格
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 交替行颜色
        self.table_widget.setAlternatingRowColors(True)

        # 表格设置为4列
        self.table_widget.setColumnCount(4)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader()
        self.table_header.setObjectName("table_header")
        # 设置表头
        self.table_widget.setHorizontalHeader(self.table_header)
        # 设置表头字段
        self.table_widget.setHorizontalHeaderLabels(TABLE_HEADER_LABELS)
        # 设置表头列宽度，第一列全选列
        self.table_widget.horizontalHeader().resizeSection(0, 60)
        # 第二列字段列，根据大小自动调整宽度
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        # 最后备注列拉伸到最大
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        # 默认行号隐藏
        self.table_widget.verticalHeader().setHidden(True)

    def connect_signal(self):
        # 双击树节点事件
        # self.tree_widget.doubleClicked.connect()
        # 第三层树节点，复选框点击事件
        # self.tree_widget.item_checkbox_clicked.connect()
        # 右击事件
        self.tree_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.tree_widget.customContextMenuRequested.connect()
