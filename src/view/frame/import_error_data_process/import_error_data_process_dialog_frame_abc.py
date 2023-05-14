# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout

from src.constant.export_import_constant import SELECT_ALL_BTN_TEXT, UNSELECT_ALL_BTN_TEXT
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.list_widget.import_error_data_list_widget import ImportErrorDataListWidget

_author_ = 'luwt'
_date_ = '2023/5/12 11:35'


class ImportErrorDataProcessDialogFrameABC(DialogFrameABC):

    def __init__(self, error_data_rows, import_success_callback, *args):
        self.error_data_rows = error_data_rows
        # 回调方法，渲染页面
        self.import_success_callback = import_success_callback
        self.top_button_layout: QGridLayout = ...
        self.select_all_button: QPushButton = ...
        self.unselect_all_button: QPushButton = ...
        self.top_button_blank_label: QLabel = ...
        self.skip_button: QPushButton = ...
        self.process_button: QPushButton = ...
        self.list_widget: ImportErrorDataListWidget = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 顶层按钮区
        self.top_button_layout = QGridLayout(self)
        self.frame_layout.addLayout(self.top_button_layout)

        self.select_all_button = QPushButton(self)
        self.top_button_layout.addWidget(self.select_all_button, 0, 0, 1, 1)
        self.unselect_all_button = QPushButton(self)
        self.top_button_layout.addWidget(self.unselect_all_button, 0, 1, 1, 1)
        self.top_button_blank_label = QLabel(self)
        self.top_button_layout.addWidget(self.top_button_blank_label, 0, 2, 1, 2)
        self.skip_button = QPushButton(self)
        self.top_button_layout.addWidget(self.skip_button, 0, 3, 1, 1)
        self.process_button = QPushButton(self)
        self.top_button_layout.addWidget(self.process_button, 0, 4, 1, 1)

        # 列表区
        self.list_widget = ImportErrorDataListWidget(self)
        self.frame_layout.addWidget(self.list_widget)

        self.list_widget.fill_list_widget(self.error_data_rows)

    def setup_other_label_text(self):
        self.select_all_button.setText(SELECT_ALL_BTN_TEXT)
        self.unselect_all_button.setText(UNSELECT_ALL_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.select_all_button.clicked.connect(self.list_widget.select_all_items)
        self.unselect_all_button.clicked.connect(self.list_widget.unselect_all_items)
        self.skip_button.clicked.connect(self.skip_data)
        self.process_button.clicked.connect(self.process_data)

    def skip_data(self):
        self.list_widget.remove_selected_items()
        self.allow_close()

    def process_data(self):
        selected_data_list = self.list_widget.get_selected_data_list()
        if selected_data_list:
            self.do_process_data(selected_data_list)

    def do_process_data(self, selected_data_list): ...

    def allow_close(self):
        # 检查是否可以关闭，依据为，当前列表中是否存在未处理的数据
        if not self.list_widget.count():
            self.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

