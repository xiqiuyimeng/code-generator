# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSplitter, QFrame, QPushButton, \
    QListWidgetItem, QTabWidget

from src.constant.template_dialog_constant import TEMPLATE_INFO_TEXT, TEMPLATE_CONFIG_TEXT, TEMPLATE_FILE_TEXT, \
    TEMPLATE_NAME, TEMPLATE_DESC, ADD_FILE_BTN_TEXT, LOCATE_FILE_BTN_TEXT, CREATE_FILE_TITLE, \
    EDIT_TEMPLATE_BOX_TITLE, ADD_TEMPLATE_BOX_TITLE, READ_TEMPLATE_BOX_TITLE, TEMPLATE_OUTPUT_DIR_TAB_TEXT, \
    TEMPLATE_VAR_CONFIG_TAB_TEXT
from src.service.async_func.async_template_task import AddTemplateExecutor, EditTemplateExecutor, ReadTemplateExecutor
from src.service.system_storage.template_file_sqlite import TemplateFile
from src.service.system_storage.template_sqlite import Template
from src.view.custom_widget.text_editor import TextEditor
from src.view.dialog.simple_name_check_dialog import SimpleNameCheckDialog
from src.view.frame.stacked_dialog_frame import StackedDialogFrame
from src.view.list_widget.list_item_func import get_template_file_data, set_template_file_data
from src.view.list_widget.template_file_list_widget import TemplateFileListWidget
from src.view.tab.tab_widget.template_file_tab_widget import TemplateFileTabWidget
from src.view.widget.template.template_ouput_config_widget import TemplateOutputConfigWidget
from src.view.widget.template.template_var_config_widget import TemplateVarConfigWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:29'


class TemplateDetailDialogFrame(StackedDialogFrame):
    """模板详情对话框框架"""
    save_signal = pyqtSignal(Template)
    edit_signal = pyqtSignal(Template)

    def __init__(self, parent_dialog, dialog_title, template_names, template_id=None):
        self.dialog_data: Template = ...
        self.new_dialog_data: Template = ...

        # 第一个窗口，模板基本信息窗口
        self.template_info_widget: QWidget = ...
        self.template_info_layout: QVBoxLayout = ...
        # 模板说明输入控件
        self.template_desc_label: QLabel = ...
        self.template_desc_text_edit: TextEditor = ...

        # 第二个窗口，模板配置窗口
        self.config_tab_widget: QTabWidget = ...
        self.output_config_widget: TemplateOutputConfigWidget = ...
        self.var_config_widget: TemplateVarConfigWidget = ...

        # 第三个窗口，模板文件页窗口
        self.template_file_widget: QWidget = ...
        self.template_file_layout: QHBoxLayout = ...
        self.file_splitter: QSplitter = ...
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

        # 添加模板执行器
        self.add_template_executor: AddTemplateExecutor = ...
        # 编辑模板执行器
        self.edit_template_executor: EditTemplateExecutor = ...
        super().__init__(parent_dialog, dialog_title, template_names, template_id)

    def get_new_dialog_data(self) -> Template:
        return Template()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def fill_list_widget(self):
        self.list_widget.addItem(TEMPLATE_INFO_TEXT)
        self.list_widget.addItem(TEMPLATE_CONFIG_TEXT)
        self.list_widget.addItem(TEMPLATE_FILE_TEXT)

    def fill_stacked_widget(self):
        # 第一个窗口，模板名称、模板说明输入框
        self.template_info_widget = QWidget(self)
        self.stacked_widget.addWidget(self.template_info_widget)
        self.template_info_layout = QVBoxLayout()
        self.template_info_widget.setLayout(self.template_info_layout)
        # 基本信息输入表单
        self.setup_template_info_ui()

        # 第二个窗口，模板配置页
        self.config_tab_widget = QTabWidget(self)
        self.stacked_widget.addWidget(self.config_tab_widget)
        self.setup_template_config_ui()

        # 第三个窗口，模板文件页
        self.template_file_widget = QWidget(self)
        self.stacked_widget.addWidget(self.template_file_widget)
        self.template_file_layout = QHBoxLayout()
        self.template_file_widget.setLayout(self.template_file_layout)
        # 模板文件页
        self.setup_template_file_ui()

    def setup_template_info_ui(self):
        # 构建模板名称输入表单
        self.setup_name_form()
        self.template_info_layout.addLayout(self.name_layout)

        # 模板说明文本输入框
        self.template_desc_label = QLabel(self)
        self.template_desc_text_edit = TextEditor(self)
        self.name_layout.addRow(self.template_desc_label, self.template_desc_text_edit)

    def setup_template_config_ui(self):
        # 第一个页面为输出路径配置页
        self.output_config_widget = TemplateOutputConfigWidget(self.parent_dialog.parent_screen_rect)
        self.config_tab_widget.addTab(self.output_config_widget, TEMPLATE_OUTPUT_DIR_TAB_TEXT)
        # 第二个页面为模板变量配置页
        self.var_config_widget = TemplateVarConfigWidget(self.parent_dialog.parent_screen_rect)
        self.config_tab_widget.addTab(self.var_config_widget, TEMPLATE_VAR_CONFIG_TAB_TEXT)

    def setup_template_file_ui(self):
        # 构建模板文件页
        self.file_splitter = QSplitter(self)
        # 不隐藏控件
        self.file_splitter.setChildrenCollapsible(False)
        # 竖直方向分割器，子项添加为frame，如果直接添加控件，无法调控比例
        self.file_splitter.setOrientation(Qt.Horizontal)
        self.template_file_layout.addWidget(self.file_splitter)

        self.file_list_frame = QFrame(self.file_splitter)
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
        self.file_tab_frame = QFrame(self.file_splitter)
        self.file_tab_layout = QVBoxLayout(self.file_tab_frame)
        self.file_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.file_tab_widget = TemplateFileTabWidget(self.file_list_widget, self.file_tab_frame)
        self.file_tab_layout.addWidget(self.file_tab_widget)

        self.file_splitter.setStretchFactor(0, 1)
        self.file_splitter.setStretchFactor(1, 6)

    def setup_other_label_text(self):
        self.name_label.setText(TEMPLATE_NAME)
        self.template_desc_label.setText(TEMPLATE_DESC)
        self.create_new_file_button.setText(ADD_FILE_BTN_TEXT)
        self.locate_file_button.setText(LOCATE_FILE_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_input(self):
        # 收集基本信息数据
        self.new_dialog_data.template_name = self.name_input.text()
        self.new_dialog_data.template_desc = self.template_desc_text_edit.toPlainText()
        # 收集模板文件数据
        self.new_dialog_data.template_files = self.file_list_widget.collect_template_files()
        # 收集模板配置数据
        self.new_dialog_data.output_config_list = self.output_config_widget.config_table.collect_data()
        self.new_dialog_data.var_config_list = self.var_config_widget.config_table.collect_data()

    def button_available(self) -> bool:
        return all((self.new_dialog_data.template_name, self.name_available))

    def connect_child_signal(self):
        self.create_new_file_button.clicked.connect(lambda: self.open_create_file_dialog(CREATE_FILE_TITLE))
        self.locate_file_button.clicked.connect(self.locate_file)

    def open_create_file_dialog(self, dialog_title, current_file_name=None):
        self.file_name_check_dialog = SimpleNameCheckDialog(self.parent_dialog.parent_screen_rect, dialog_title,
                                                            self.file_list_widget.collect_item_text_list(),
                                                            current_file_name)
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
        current_tab_indexes = tuple(filter(lambda x: self.file_tab_widget.tabText(x) == original_file_name,
                                           range(self.file_tab_widget.count())))
        if current_tab_indexes:
            self.file_tab_widget.setTabText(current_tab_indexes[0], file_name)

    def add_template_file(self, file_name):
        template_file = TemplateFile()
        template_file.file_name = file_name
        # 添加列表项
        self.add_list_file_item(template_file)
        # 添加tab
        self.add_file_tab(template_file)

    def add_list_file_item(self, template_file):
        # 添加模板文件
        file_item = QListWidgetItem(template_file.file_name)
        self.file_list_widget.addItem(file_item)
        # 保存引用
        set_template_file_data(file_item, template_file)
        # 设置当前项
        self.file_list_widget.setCurrentItem(file_item)

    def add_file_tab(self, template_file):
        content_editor = TextEditor(self.file_tab_widget)
        self.file_tab_widget.addTab(content_editor, template_file.file_name)
        # 填充数据
        content_editor.setPlainText(template_file.file_content)
        self.file_tab_widget.setCurrentIndex(self.file_tab_widget.count() - 1)

    def locate_file(self):
        current_tab_text = self.file_tab_widget.tabText(self.file_tab_widget.currentIndex())
        if current_tab_text:
            current_index = tuple(filter(lambda x: self.file_list_widget.item(x).text() == current_tab_text,
                                         range(self.file_list_widget.count())))[0]
            self.file_list_widget.setCurrentRow(current_index)

    def save_func(self):
        # 手动收集数据
        self.collect_input()
        # 如果存在原数据，说明是编辑
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.edit_template_executor = EditTemplateExecutor(self.new_dialog_data, self.parent_dialog,
                                                               self.parent_dialog, EDIT_TEMPLATE_BOX_TITLE,
                                                               self.edit_post_process)
            self.edit_template_executor.start()
        else:
            self.add_template_executor = AddTemplateExecutor(self.new_dialog_data, self.parent_dialog,
                                                             self.parent_dialog, ADD_TEMPLATE_BOX_TITLE,
                                                             self.add_post_process)
            self.add_template_executor.start()

    def add_post_process(self):
        self.save_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    def edit_post_process(self):
        self.edit_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_read_storage_executor(self, callback):
        return ReadTemplateExecutor(self.dialog_data, self.parent_dialog, self.parent_dialog,
                                    READ_TEMPLATE_BOX_TITLE, callback)

    def get_old_name(self) -> str:
        return self.dialog_data.template_name

    def setup_echo_other_data(self):
        self.template_desc_text_edit.setPlainText(self.dialog_data.template_desc)
        # 回显文件列表
        [self.add_list_file_item(template_file) for template_file in self.dialog_data.template_files]
        # 回显模板文件列表数据，按照tab顺序
        reopen_tab_files = sorted(filter(lambda x: x.tab_opened, self.dialog_data.template_files),
                                  key=lambda x: x.tab_item_order)
        [self.add_file_tab(template_file) for template_file in reopen_tab_files]
        # 找出当前列表项
        current_files = tuple(filter(lambda x: x.is_current, self.dialog_data.template_files))
        if current_files:
            self.file_list_widget.setCurrentRow(self.dialog_data.template_files.index(current_files[0]))
        # 找出当前tab页
        if reopen_tab_files:
            current_tab_file = tuple(filter(lambda x: x.is_current_tab, reopen_tab_files))[0]
            self.file_tab_widget.setCurrentIndex(reopen_tab_files.index(current_tab_file))
        # 回显模板配置数据
        self.output_config_widget.config_table.fill_table(self.dialog_data.output_config_list)
        self.var_config_widget.config_table.fill_table(self.dialog_data.var_config_list)

    # ------------------------------ 后置处理 end ------------------------------ #
