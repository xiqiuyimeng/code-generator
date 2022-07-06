# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar, QFrame, QLabel, \
    QSplitter

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
        self.main_widget: QWidget = ...
        self.main_layout: QVBoxLayout = ...

        # 定义中心控件，用以包含主体内容
        self.central_widget: QWidget = ...
        self.central_layout: QHBoxLayout = ...

        # 定义水平方向分割器
        self.horizontal_splitter: QSplitter = ...

        # 菜单栏、标题栏、工具栏、状态栏
        self.menubar: Menubar = ...
        self.titlebar: TitleBar = ...
        self.toolbar: ToolBar = ...
        self.statusbar: QStatusBar = ...

        # 左侧树结构
        self.tree_frame: QFrame = ...
        self.tree_layout: QVBoxLayout = ...
        self.tree_header_label: QLabel = ...
        self.tree_widget: TreeWidget = ...

        # 右侧表结构
        self.table_frame: QFrame = ...
        self.table_layout: QVBoxLayout = ...
        self.table_header: CheckBoxHeader = ...
        self.table_header_label: QLabel = ...
        self.table_widget: TableWidget = ...

        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 按当前分辨率计算窗口大小
        self.resize(self.desktop_screen_rect.width() * 0.6, self.desktop_screen_rect.height() * 0.75)
        # 不透明度
        self.setWindowOpacity(0.95)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        # 设置所有间距为0
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(10, 0, 0, 0)

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
        self.titlebar = TitleBar(self, self.menubar)
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

        self.tree_widget = TreeWidget(self.tree_frame, self)
        self.tree_widget.setObjectName('tree_widget')
        self.tree_widget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.tree_layout.addWidget(self.tree_widget)

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

        # 默认隐藏
        self.table_frame.setHidden(True)
