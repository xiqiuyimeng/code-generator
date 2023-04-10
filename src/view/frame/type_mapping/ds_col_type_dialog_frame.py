# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QStackedWidget, QListWidgetItem

from src.constant.type_mapping_dialog_constant import SAVE_DATA_TIPS, ADD_DS_COL_TYPE_BUTTON_TEXT, \
    ADD_DS_COL_TYPE_TITLE, ADD_COL_TYPE_LIST_TITLE, DS_COL_TYPE_LIST_BOX_TITLE
from src.service.async_func.async_ds_col_type_task import ListDsColTypeExecutor, SaveDsColTypeExecutor
from src.view.dialog.simple_name_check_dialog import SimpleNameCheckDialog
from src.view.frame.save_dialog_frame import SaveDialogFrame
from src.view.list_widget.col_type_list_widget import ColTypeListWidget
from src.view.list_widget.display_list_widget import DsTypeListWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:46'


class DsColTypeDialogFrame(SaveDialogFrame):
    """数据源列类型对话框框架，用以维护所有的数据类型和列类型"""

    def __init__(self, parent_dialog, dialog_title):
        self.ds_col_type_dict: dict = ...
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
        self.save_ds_col_type_dialog: SimpleNameCheckDialog = ...
        # 为了美观，将表格布局扩大，容纳5个元素，中间为空白占位label
        super().__init__(parent_dialog, dialog_title, quit_button_row_index=4)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 温馨提示
        self.tips_label = QLabel()
        self.tips_label.setObjectName('tips_label')
        self.tips_label.setText(SAVE_DATA_TIPS)
        self.frame_layout.addWidget(self.tips_label)

        self._layout = QHBoxLayout(self)
        self.frame_layout.addLayout(self._layout)

        self.ds_type_list_widget = DsTypeListWidget(self)
        self._layout.addWidget(self.ds_type_list_widget)
        # 构建堆栈式窗口
        self.stacked_widget = QStackedWidget(self)
        self._layout.addWidget(self.stacked_widget)

    def setup_other_button(self):
        self.add_ds_col_type_button = QPushButton(self)
        self.button_layout.addWidget(self.add_ds_col_type_button, 0, 0, 1, 1)

    def setup_other_label_text(self):
        self.add_ds_col_type_button.setText(ADD_DS_COL_TYPE_BUTTON_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.ds_type_list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)
        self.add_ds_col_type_button.clicked.connect(lambda: self.open_save_col_type_dialog(ADD_DS_COL_TYPE_TITLE))

    def open_save_col_type_dialog(self, dialog_title, col_type=None):
        current_ds_type = self.ds_type_list_widget.currentItem().text()
        # 打开添加数据源列类型对话框
        self.save_ds_col_type_dialog = SimpleNameCheckDialog(self.parent_dialog.parent_screen_rect, dialog_title,
                                                             self.ds_col_type_dict.get(current_ds_type), col_type)
        if col_type:
            self.save_ds_col_type_dialog.edit_signal.connect(self.edit_ds_col_type)
        else:
            self.save_ds_col_type_dialog.save_signal.connect(self.add_ds_col_type)
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
                                                               ADD_COL_TYPE_LIST_TITLE,
                                                               self.parent_dialog.close)
        self.save_ds_col_type_executor.start()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_ds_col_type_executor = ListDsColTypeExecutor(self, self, DS_COL_TYPE_LIST_BOX_TITLE,
                                                               self.list_col_type_callback)
        self.list_ds_col_type_executor.start()

    def list_col_type_callback(self, col_type_dict: dict):
        if col_type_dict:
            self.ds_col_type_dict = col_type_dict
            self.fill_ds_types()
            self.fill_col_types()

    def fill_ds_types(self):
        self.ds_type_list_widget.fill_list_widget(self.ds_col_type_dict.keys())
        self.ds_type_list_widget.setCurrentRow(0)

    def fill_col_types(self):
        for col_types in self.ds_col_type_dict.values():
            col_type_list_widget = ColTypeListWidget(col_types, self.open_save_col_type_dialog, self)
            [col_type_list_widget.addItem(col_type) for col_type in col_types]
            self.stacked_widget.addWidget(col_type_list_widget)

    # ------------------------------ 后置处理 end ------------------------------ #