# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar

from src.constant.icon_enum import get_icon
from src.constant.window_constant import SWITCH_DS_CATEGORY_TITLE, DS_CATEGORY_NO_CHANGE_MSG
from src.service.async_func.async_ds_category_task import InitDsCategoryExecutor, SwitchDsCategoryExecutor
from src.service.system_storage.ds_category_sqlite import DsCategory
from src.service.util.ds_category_util import get_current_ds_category
from src.view.bar.menubar import Menubar
from src.view.bar.titlebar import TitleBar
from src.view.bar.toolbar import ToolBar
from src.view.box.message_box import pop_ok
from src.view.window.central_widget import CentralWidget

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
        self.central_widget: CentralWidget = ...
        self.central_layout: QHBoxLayout = ...

        # 菜单栏、标题栏、工具栏、状态栏
        self.menubar: Menubar = ...
        self.titlebar: TitleBar = ...
        self.toolbar: ToolBar = ...
        self.statusbar: QStatusBar = ...

        self.ds_categories = ...
        self.current_ds_category = ...
        self.init_ds_category_executor = ...

        self.setup_ui()

        # 初始化 ds category
        self.init_ds_category_executor = InitDsCategoryExecutor(self, self, SWITCH_DS_CATEGORY_TITLE,
                                                                self.setup_ui_by_ds_category)
        self.init_ds_category_executor.start()

        # 切换数据源种类线程
        self.switch_ds_category_executor = ...

    def setup_ui(self):
        # 设置窗口无边框，点击任务栏图标，可以实现隐藏和显示
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint
                            | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint | Qt.WindowStaysOnTopHint)
        # 按当前分辨率计算窗口大小
        self.resize(self.desktop_screen_rect.width() * 0.6, self.desktop_screen_rect.height() * 0.75)
        # 不透明度
        self.setWindowOpacity(0.95)

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        # 设置所有间距为0
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(10, 0, 0, 0)

        self.init_bars()

        self.central_widget = CentralWidget(self)

        # 主布局添加所有部件，依次为标题栏、菜单栏、工具栏、承载了实际窗口内容的主控件，将窗口中央控件设置为包含所有的控件
        self.main_layout.addWidget(self.titlebar)
        self.main_layout.addWidget(self.toolbar)
        self.main_layout.addWidget(self.central_widget)
        self.setCentralWidget(self.main_widget)

    def init_bars(self):
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
        self.setWindowIcon(get_icon('window'))

    def setup_ui_by_ds_category(self, ds_categories):
        self.ds_categories = ds_categories
        self.current_ds_category: DsCategory = get_current_ds_category(self.ds_categories)

        # 首先处理bar
        self.menubar.switch_ds_category()
        self.toolbar.switch_ds_category()

        # 处理主窗体
        self.central_widget.setup_ui()

    def switch_ds_category(self, ds_category_action):
        ds_category = ds_category_action.text()
        # 切换数据源类型，如果类型一致，应提示
        if ds_category != self.current_ds_category.name:
            self.switch_ds_category_executor = SwitchDsCategoryExecutor(ds_category, self, self,
                                                                        SWITCH_DS_CATEGORY_TITLE,
                                                                        self.setup_ui_by_ds_category)
            self.switch_ds_category_executor.start()
        else:
            pop_ok(DS_CATEGORY_NO_CHANGE_MSG.format(ds_category), SWITCH_DS_CATEGORY_TITLE, self)
