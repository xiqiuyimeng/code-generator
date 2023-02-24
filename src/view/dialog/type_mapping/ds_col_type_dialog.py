# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QListWidgetItem, QStackedWidget, QHBoxLayout, QLabel

from src.constant.type_mapping_dialog_constant import DS_COL_TYPE_LIST_TITLE, DS_COL_TYPE_LIST_BOX_TITLE, \
    SYNC_DS_TYPE_BUTTON_TEXT, ADD_DS_COL_TYPE_BUTTON_TEXT, ADD_COL_TYPE_LIST_TITLE, ADD_DS_COL_TYPE_NO_DS_TYPE, \
    ADD_DS_COL_TYPE_TITLE, SAVE_DATA_TIPS
from src.service.async_func.async_ds_col_type_task import ListDsColTypeExecutor, SaveDsColTypeExecutor
from src.service.system_storage.conn_type import ConnTypeEnum
from src.service.system_storage.struct_type import StructTypeEnum
from src.view.box.message_box import pop_fail
from src.view.dialog.custom_save_dialog import CustomSaveDialog
from src.view.dialog.type_mapping.save_ds_col_type_dialog import SaveDsColTypeDialog
from src.view.list_widget.col_type_list_widget import ColTypeListWidget
from src.view.list_widget.ds_type_list_widget import DsTypeListWidget

_author_ = 'luwt'
_date_ = '2023/2/13 10:03'


class DsColTypeDialog(CustomSaveDialog):
    """数据源列类型对话框，用以维护所有的数据类型和列类型"""

    def __init__(self, screen_rect):
        self.ds_col_type_dict: dict = ...
        # 同步数据源类型
        self.sync_ds_type_button: QPushButton = ...
        # 添加新的数据源列类型按钮
        self.add_ds_col_type_button: QPushButton = ...
        # 读取数据源列类型列表执行器
        self.list_ds_col_type_executor: ListDsColTypeExecutor = ...
        # 保存数据源列类型列表执行器
        self.save_ds_col_type_executor: SaveDsColTypeExecutor = ...
        self.tips_label: QLabel = ...
        self._layout: QHBoxLayout = ...
        # 堆栈式窗口
        self.stacked_widget: QStackedWidget = ...
        self.ds_type_list_widget: DsTypeListWidget = ...
        # 添加编辑数据源列类型项对话框
        self.save_ds_col_type_dialog: SaveDsColTypeDialog = ...
        # 为了美观，将表格布局扩大，容纳5个元素，中间为空白占位label
        super().__init__(screen_rect, DS_COL_TYPE_LIST_TITLE, quit_button_row_index=4)

    def resize_dialog(self):
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def setup_content_ui(self):
        # 温馨提示
        self.tips_label = QLabel()
        self.tips_label.setObjectName('tips_label')
        self.tips_label.setText(SAVE_DATA_TIPS)
        self.frame_layout.addWidget(self.tips_label)

        self._layout = QHBoxLayout(self.frame)
        self.frame_layout.addLayout(self._layout)

        self.ds_type_list_widget = DsTypeListWidget(self.frame)
        self._layout.addWidget(self.ds_type_list_widget)
        # 构建堆栈式窗口
        self.stacked_widget = QStackedWidget(self.frame)
        self._layout.addWidget(self.stacked_widget)

    def setup_other_button(self):
        self.sync_ds_type_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.sync_ds_type_button, 0, 0, 1, 1)
        self.add_ds_col_type_button = QPushButton(self.frame)
        self.button_layout.addWidget(self.add_ds_col_type_button, 0, 1, 1, 1)

    def setup_other_label_text(self):
        self.sync_ds_type_button.setText(SYNC_DS_TYPE_BUTTON_TEXT)
        self.add_ds_col_type_button.setText(ADD_DS_COL_TYPE_BUTTON_TEXT)

    def connect_other_signal(self):
        self.ds_type_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.sync_ds_type_button.clicked.connect(self.sync_ds_types)
        self.add_ds_col_type_button.clicked.connect(self.add_ds_type_item)

    def sync_ds_types(self):
        # 同步最新的数据源类型
        if self.ds_col_type_dict is Ellipsis:
            self.ds_col_type_dict = dict()
        # 所有的数据源类型字典
        all_ds_type_dict = dict()
        for conn_type in ConnTypeEnum:
            conn_type_name = conn_type.value.display_name
            all_ds_type_dict[conn_type_name] = self.ds_col_type_dict.get(conn_type_name, list())
        for struct_type in StructTypeEnum:
            struct_type_name = struct_type.value.display_name
            all_ds_type_dict[struct_type_name] = self.ds_col_type_dict.get(struct_type_name, list())

        self.ds_col_type_dict = all_ds_type_dict
        # 清空列表控件和堆栈式窗口
        self.ds_type_list_widget.clear()
        self.clear_stacked_widget()
        # 以最新的数据源类型来渲染列表
        self.fill_ds_types()
        self.fill_col_types()

    def clear_stacked_widget(self):
        if self.stacked_widget.count():
            for index in range(self.stacked_widget.count()):
                child_widget = self.stacked_widget.widget(0)
                self.stacked_widget.removeWidget(child_widget)

    def fill_ds_types(self):
        self.ds_type_list_widget.fill_list_widget(self.ds_col_type_dict.keys())
        self.ds_type_list_widget.setCurrentRow(0)

    def fill_col_types(self):
        for col_types in self.ds_col_type_dict.values():
            col_type_list_widget = ColTypeListWidget(col_types, self.open_save_col_type_dialog, self.frame)
            [col_type_list_widget.addItem(col_type) for col_type in col_types]
            self.stacked_widget.addWidget(col_type_list_widget)

    def list_col_type_callback(self, col_type_dict: dict):
        if col_type_dict:
            self.ds_col_type_dict = col_type_dict
            self.fill_ds_types()
            self.fill_col_types()

    def add_ds_type_item(self):
        if self.ds_type_list_widget.currentRow() < 0:
            pop_fail(ADD_DS_COL_TYPE_NO_DS_TYPE, ADD_DS_COL_TYPE_TITLE, self)
        else:
            self.open_save_col_type_dialog(ADD_DS_COL_TYPE_TITLE)

    def open_save_col_type_dialog(self, dialog_title, col_type=None):
        current_ds_type = self.ds_type_list_widget.currentItem().text()
        # 打开添加数据源列类型对话框
        self.save_ds_col_type_dialog = SaveDsColTypeDialog(self.parent_screen_rect,
                                                           dialog_title,
                                                           self.ds_col_type_dict.get(current_ds_type),
                                                           col_type)
        if col_type:
            self.save_ds_col_type_dialog.edit_col_type_signal.connect(self.edit_ds_col_type)
        else:
            self.save_ds_col_type_dialog.add_col_type_signal.connect(self.add_ds_col_type)
        self.save_ds_col_type_dialog.exec()

    def edit_ds_col_type(self, col_type):
        # 获取当前的列类型列表控件
        col_type_list_widget = self.stacked_widget.currentWidget()
        col_type_item = col_type_list_widget.currentItem()
        col_types = self.ds_col_type_dict.get(self.ds_type_list_widget.currentItem().text())
        col_types[col_types.index(col_type_item.text())] = col_type
        col_type_item.setText(col_type)

    def add_ds_col_type(self, col_type):
        # 获取当前的列类型列表控件
        col_type_list_widget = self.stacked_widget.currentWidget()
        col_type_list_widget.addItem(QListWidgetItem(col_type))
        col_types = self.ds_col_type_dict.get(self.ds_type_list_widget.currentItem().text())
        col_types.append(col_type)

    def save_func(self):
        self.save_ds_col_type_executor = SaveDsColTypeExecutor(self.ds_col_type_dict, self, self,
                                                               ADD_COL_TYPE_LIST_TITLE, self.close)
        self.save_ds_col_type_executor.start()

    def post_process(self):
        self.list_ds_col_type_executor = ListDsColTypeExecutor(self, self, DS_COL_TYPE_LIST_BOX_TITLE,
                                                               self.list_col_type_callback)
        self.list_ds_col_type_executor.start()
