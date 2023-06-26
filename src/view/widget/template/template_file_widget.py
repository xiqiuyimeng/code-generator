# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSplitter, QFrame, QVBoxLayout, QPushButton

from src.constant.template_dialog_constant import ADD_FILE_BTN_TEXT, LOCATE_FILE_BTN_TEXT, CREATE_FILE_TITLE, \
    CHECK_TEMPLATE_FILE_PROMPT, CHECK_TEMPLATE_FILE_TITLE, CHECK_TP_FILE_CONFIG_PROMPT, CHECK_TP_FILE_CONFIG_TITLE, \
    CHECK_FILE_NAME_TP_PROMPT, CHECK_FILE_NAME_TP_TITLE
from src.service.system_storage.template_file_sqlite import TemplateFile
from src.view.box.message_box import pop_question
from src.view.dialog.simple_name_check_dialog import SimpleNameCheckDialog
from src.view.list_widget.list_item_func import get_template_file_data
from src.view.list_widget.template_file_list_widget import TemplateFileListWidget
from src.view.tab.tab_widget.template_file_tab_widget import TemplateFileTabWidget

_author_ = 'luwt'
_date_ = '2023/6/25 13:48'


class TemplateFileWidget(QWidget):
    """模板文件页，嵌入在堆栈式窗口中"""

    def __init__(self):
        super().__init__()
        self._layout: QHBoxLayout = ...
        self.splitter: QSplitter = ...
        self.file_list_frame: QFrame = ...
        self.file_list_layout: QVBoxLayout = ...
        # 文件列标顶部
        self.file_list_header_layout: QHBoxLayout = ...
        self.create_new_file_button: QPushButton = ...
        self.locate_file_button: QPushButton = ...
        # 文件列表
        self.file_list_widget: TemplateFileListWidget = ...
        # 文件tab页
        self.file_tab_frame: QFrame = ...
        self.file_tab_layout: QVBoxLayout = ...
        self.file_tab_widget: TemplateFileTabWidget = ...
        self.file_name_check_dialog: SimpleNameCheckDialog = ...

        self.setup_ui()
        self.setup_label_text()
        self.connect_signal()

    def setup_ui(self):
        self._layout = QHBoxLayout(self)
        self.splitter = QSplitter(self)
        # 不隐藏控件
        self.splitter.setChildrenCollapsible(False)
        # 竖直方向分割器，子项添加为frame，如果直接添加控件，无法调控比例
        self.splitter.setOrientation(Qt.Horizontal)
        self._layout.addWidget(self.splitter)

        self.file_list_frame = QFrame(self.splitter)
        self.file_list_layout = QVBoxLayout(self.file_list_frame)
        self.file_list_layout.setContentsMargins(0, 0, 0, 0)
        # 文件列表顶部按钮区
        self.file_list_header_layout = QHBoxLayout(self.file_list_frame)
        self.file_list_layout.addLayout(self.file_list_header_layout)
        self.create_new_file_button = QPushButton(self.file_list_frame)
        self.file_list_header_layout.addWidget(self.create_new_file_button)
        self.locate_file_button = QPushButton(self.file_list_frame)
        self.file_list_header_layout.addWidget(self.locate_file_button)
        # 文件列表
        self.file_list_widget = TemplateFileListWidget(self, self.open_create_file_dialog, self.file_list_frame)
        self.file_list_layout.addWidget(self.file_list_widget)

        # 文件tab页
        self.file_tab_frame = QFrame(self.splitter)
        self.file_tab_layout = QVBoxLayout(self.file_tab_frame)
        self.file_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.file_tab_widget = TemplateFileTabWidget(self.file_list_widget, self.file_tab_frame)
        self.file_tab_layout.addWidget(self.file_tab_widget)

        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 7)

    def setup_label_text(self):
        self.create_new_file_button.setText(ADD_FILE_BTN_TEXT)
        self.locate_file_button.setText(LOCATE_FILE_BTN_TEXT)

    def connect_signal(self):
        self.create_new_file_button.clicked.connect(lambda: self.open_create_file_dialog(CREATE_FILE_TITLE))
        self.locate_file_button.clicked.connect(self.file_list_widget.locate_file)

    def open_create_file_dialog(self, dialog_title, current_file_name=None):
        self.file_name_check_dialog = SimpleNameCheckDialog(self.file_list_widget.collect_item_text(),
                                                            dialog_title, current_file_name)
        if current_file_name:
            self.file_name_check_dialog.edit_signal.connect(self.edit_file_name)
        else:
            self.file_name_check_dialog.save_signal.connect(self.add_template_file)
        self.file_name_check_dialog.exec()

    def edit_file_name(self, file_name):
        # 编辑模板文件名称
        current_item = self.file_list_widget.currentItem()
        original_file_name = current_item.text()
        current_item.setText(file_name)
        # 修改文件对象中的名称
        get_template_file_data(current_item).file_name = file_name
        # 搜索tab页，修改tab部件名称
        current_tab_indexes = [tab_idx for tab_idx in range(self.file_tab_widget.count())
                               if self.file_tab_widget.tabText(tab_idx) == original_file_name]
        if current_tab_indexes:
            self.file_tab_widget.setTabText(current_tab_indexes[0], file_name)

    def add_template_file(self, file_name):
        template_file = TemplateFile()
        template_file.file_name = file_name
        # 添加列表项
        self.file_list_widget.add_list_file_item(template_file)
        # 添加tab
        self.file_tab_widget.add_file_tab(template_file)

    def collect_template_files(self):
        return self.file_list_widget.collect_template_files()

    def echo_template_files(self, template_files):
        self.file_list_widget.fill_list_widget(template_files)
        # 回显模板文件列表数据，按照tab顺序
        reopen_tab_files = sorted([file for file in template_files if file.tab_opened],
                                  key=lambda x: x.tab_item_order)
        for template_file in reopen_tab_files:
            self.file_tab_widget.add_file_tab(template_file)
        # 找出当前列表项
        current_files = [file for file in template_files if file.is_current]
        if current_files:
            self.file_list_widget.setCurrentRow(template_files.index(current_files[0]))
        # 找出当前tab页
        if reopen_tab_files:
            current_tab_file = [tab_file for tab_file in reopen_tab_files if tab_file.is_current_tab][0]
            self.file_tab_widget.setCurrentIndex(reopen_tab_files.index(current_tab_file))

    def check_file_completable(self, template_files):
        # 校验模板文件是否存在，模板文件是否关联了输出路径配置，模板文件名称模板是否存在，如果没有，提示
        template_completable = True
        if not template_files:
            template_completable = pop_question(CHECK_TEMPLATE_FILE_PROMPT, CHECK_TEMPLATE_FILE_TITLE, self)
        else:
            if [file for file in template_files if file.output_config_id is None]:
                template_completable = pop_question(CHECK_TP_FILE_CONFIG_PROMPT, CHECK_TP_FILE_CONFIG_TITLE, self)
            elif [file for file in template_files if not file.file_name_template]:
                template_completable = pop_question(CHECK_FILE_NAME_TP_PROMPT, CHECK_FILE_NAME_TP_TITLE, self)
        return template_completable

    def collect_unbind_config_files(self):
        return self.file_list_widget.collect_unbind_config_files()
