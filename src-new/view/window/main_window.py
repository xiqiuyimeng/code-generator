# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStatusBar

from constant.constant import SWITCH_DS_TYPE_TITLE, DS_TYPE_NO_CHANGE_MSG
from constant.icon_enum import get_icon
from service.async_func.async_system_task.async_system_db_task import InitDsTypeExecutor, SwitchDsTypeExecutor
from service.async_func.async_system_task.system_operation_queue import SystemOperationQueue
from service.init.frame_type_init import get_current_datasource_type
from service.system_storage.datasource_type_sqlite import DatasourceType
from service.util.tree_node import Tree
from view.bar.menubar import Menubar
from view.bar.titlebar import TitleBar
from view.bar.toolbar import ToolBar
from view.box.message_box import pop_ok
from view.window.central_widget import CentralWidget

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

        # 保存选中对象
        self.tree_data = Tree()

        self.datasource_types = ...
        self.current_ds_type = ...
        self.init_ds_type_executor = ...

        # 缓存树结构需要使用的icon
        self.tree_icon_dict = dict()

        # 保存操作记录的队列
        self.operation_queue = SystemOperationQueue()

        self.setup_ui()

        # 初始化 datasource_type
        self.init_ds_type_executor = InitDsTypeExecutor(self.setup_ui_by_ds_type,
                                                        self, self, SWITCH_DS_TYPE_TITLE)
        self.init_ds_type_executor.start()

        # 切换数据源类型线程
        self.switch_ds_type_executor = ...

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

    def setup_ui_by_ds_type(self, ds_types):
        self.datasource_types = ds_types
        self.current_ds_type: DatasourceType = get_current_datasource_type(self.datasource_types)

        # 首先处理bar
        self.menubar.switch_ds_type()
        self.toolbar.switch_ds_type()

        # 处理主窗体
        self.central_widget.setup_ui()

    def switch_ds_type(self, ds_type_action):
        ds_type = ds_type_action.text()
        # 切换数据源类型，如果类型一致，应提示
        if ds_type != self.current_ds_type.name:
            self.switch_ds_type_executor = SwitchDsTypeExecutor(ds_type, self.setup_ui_by_ds_type,
                                                                self, self, SWITCH_DS_TYPE_TITLE)
            self.switch_ds_type_executor.start()
        else:
            pop_ok(DS_TYPE_NO_CHANGE_MSG.format(ds_type), SWITCH_DS_TYPE_TITLE, self)
