# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLabel, QLineEdit, QAction, QGridLayout, QComboBox, QStackedWidget, QWidget, QFormLayout, \
    QPushButton

from src.constant.template_dialog_constant import CONFIG_NAME_TEXT, VAR_NAME_TEXT, WIDGET_LABEL_TEXT, \
    CONFIG_DESC_TEXT, IS_REQUIRED_TEXT, DEFAULT_VALUE_TEXT, PLACEHOLDER_TEXT, VALUE_RANGE_TEXT, \
    ADD_VALUE_BTN_TEXT, CONFIG_INPUT_WIDGET_TYPE_DICT, ADD_RANGE_VALUE_BOX_TITLE, VAR_NAME_REG_RULE, \
    VAR_NAME_PLACEHOLDER_TEXT
from src.service.system_storage.template_config_sqlite import TemplateConfig, RequiredEnum
from src.view.custom_widget.text_editor import TextEditor
from src.view.dialog.simple_name_check_dialog import SimpleNameCheckDialog
from src.view.frame.frame_func import set_name_input_style, reset_name_input_style
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame
from src.view.list_widget.range_value_list_widget import ValueRangeListWidget

_author_ = 'luwt'
_date_ = '2023/4/3 14:20'


class TemplateConfigDialogFrame(NameCheckDialogFrame):
    """模板配置信息对话框框架，不读取数据库数据，保存功能仅发送信号，不涉及数据库修改"""
    save_signal = pyqtSignal(TemplateConfig)
    edit_signal = pyqtSignal(TemplateConfig)

    def __init__(self, parent_dialog, dialog_title, name_list, var_names, template_config=None):
        self.var_names = var_names
        self.old_var_name: str = ...
        self.var_name_available: bool = ...
        self.var_name_label: QLabel = ...
        self.var_name_input: QLineEdit = ...
        self.var_name_checker: QLabel = ...
        self.var_name_check_action: QAction = ...
        self.echo_data_complete = False

        self.widget_layout: QGridLayout = ...
        # 配置项说明
        self.desc_label: QLabel = ...
        self.desc_input: TextEditor = ...
        # 配置项控件
        self.widget_label: QLabel = ...
        self.value_combo_box: QComboBox = ...
        # 是否必填
        self.is_required_label: QLabel = ...
        self.is_required_combox: QComboBox = ...
        # 堆栈式窗口
        self.stacked_widget: QStackedWidget = ...
        # 目前有四种窗口
        self.input_widget: QWidget = ...
        self.input_layout: QGridLayout = ...
        self.text_edit_widget: QWidget = ...
        self.text_edit_layout: QGridLayout = ...
        self.combox_widget: QWidget = ...
        self.combox_layout: QGridLayout = ...
        self.choose_dir_widget: QWidget = ...
        # 默认值
        self.default_value_label: QLabel = ...
        self.default_value_input: QLineEdit = ...
        self.default_text_edit_value_label: QLabel = ...
        self.default_text_edit_value_input: TextEditor = ...
        self.default_value_combo_box_layout: QFormLayout = ...
        self.default_combox_value_label: QLabel = ...
        self.default_value_combo_box: QComboBox = ...
        # 占位文本
        self.placeholder_label: QLabel = ...
        self.placeholder_input: QLineEdit = ...
        # 取值范围
        self.value_range_label: QLabel = ...
        self.value_range_list_widget: ValueRangeListWidget = ...
        # 取值范围下拉框，添加值按钮
        self.add_value_button: QPushButton = ...
        self.save_range_value_dialog: SimpleNameCheckDialog = ...
        super().__init__(parent_dialog, dialog_title, name_list, template_config, read_storage=False)

    def get_new_dialog_data(self) -> TemplateConfig:
        return TemplateConfig()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_content_ui(self):
        self.var_name_label = QLabel(self)
        self.var_name_input = QLineEdit(self)
        self.var_name_input.setObjectName('var_name_input')

        self.name_layout.addRow(self.var_name_label, self.var_name_input)

        self.var_name_checker = QLabel(self)
        self.name_layout.addRow(self.placeholder_blank, self.var_name_checker)

        # 配置项说明
        self.desc_label = QLabel()
        self.desc_input = TextEditor()
        self.name_layout.addRow(self.desc_label, self.desc_input)

        self.widget_layout = QGridLayout()
        self.frame_layout.addLayout(self.widget_layout)

        # 配置项控件
        self.widget_label = QLabel()
        self.widget_layout.addWidget(self.widget_label, 0, 0, 1, 1)
        self.value_combo_box = QComboBox()
        self.widget_layout.addWidget(self.value_combo_box, 0, 1, 1, 1)
        # 空白项
        self.widget_layout.addWidget(QLabel(), 0, 2, 1, 1)
        # 是否必填
        self.is_required_label = QLabel()
        self.widget_layout.addWidget(self.is_required_label, 0, 3, 1, 1)
        self.is_required_combox = QComboBox()
        self.widget_layout.addWidget(self.is_required_combox, 0, 4, 1, 1)

        # 堆栈式窗口
        self.stacked_widget = QStackedWidget()
        self.widget_layout.addWidget(self.stacked_widget, 1, 0, 1, 5)

        # 输入框窗口
        self.setup_input_widget()
        # 文本编辑区窗口
        self.setup_text_edit_widget()
        # 下拉框窗口
        self.setup_combox_widget()
        # 选择文件夹对话框窗口
        self.setup_choose_dir_widget()

    def setup_input_widget(self):
        self.input_widget = QWidget()
        self.input_layout = QGridLayout(self.input_widget)
        self.stacked_widget.addWidget(self.input_widget)
        # 默认值
        self.default_value_label = QLabel()
        self.input_layout.addWidget(self.default_value_label, 0, 0, 1, 1)
        self.default_value_input = QLineEdit()
        self.input_layout.addWidget(self.default_value_input, 0, 1, 1, 1)
        # 占位文本
        self.placeholder_label = QLabel()
        self.input_layout.addWidget(self.placeholder_label, 1, 0, 1, 1)
        self.placeholder_input = QLineEdit()
        self.input_layout.addWidget(self.placeholder_input, 1, 1, 1, 1)

        self.input_layout.setColumnStretch(0, 2)
        self.input_layout.setColumnStretch(1, 11)

    def setup_text_edit_widget(self):
        self.text_edit_widget = QWidget()
        self.text_edit_layout = QGridLayout(self.text_edit_widget)
        self.stacked_widget.addWidget(self.text_edit_widget)
        # 默认值
        self.default_text_edit_value_label = QLabel()
        self.text_edit_layout.addWidget(self.default_text_edit_value_label, 0, 0, 1, 1)
        self.default_text_edit_value_input = TextEditor()
        self.text_edit_layout.addWidget(self.default_text_edit_value_input, 0, 1, 1, 1)

        self.text_edit_layout.setColumnStretch(0, 2)
        self.text_edit_layout.setColumnStretch(1, 11)

    def setup_combox_widget(self):
        self.combox_widget = QWidget()
        self.combox_layout = QGridLayout(self.combox_widget)
        # 设置列比例
        self.combox_layout.setColumnStretch(0, 1)
        self.combox_layout.setColumnStretch(1, 3)
        self.combox_layout.setColumnStretch(2, 3)
        self.stacked_widget.addWidget(self.combox_widget)
        # 取值范围
        self.value_range_label = QLabel()
        self.combox_layout.addWidget(self.value_range_label, 0, 0, 1, 1)
        self.value_range_list_widget = ValueRangeListWidget(self.open_save_range_value_dialog, self.combox_widget)
        self.combox_layout.addWidget(self.value_range_list_widget, 0, 1, 3, 1)
        # 默认值
        self.default_value_combo_box_layout = QFormLayout()
        self.combox_layout.addLayout(self.default_value_combo_box_layout, 0, 2, 1, 1)
        self.default_combox_value_label = QLabel()
        self.default_value_combo_box = QComboBox()
        self.default_value_combo_box_layout.addRow(self.default_combox_value_label, self.default_value_combo_box)

        # 添加值按钮
        self.add_value_button = QPushButton()
        self.combox_layout.addWidget(self.add_value_button, 1, 2, 1, 1)

    def setup_choose_dir_widget(self):
        self.choose_dir_widget = QWidget()
        self.stacked_widget.addWidget(self.choose_dir_widget)

    def setup_other_label_text(self):
        self.name_label.setText(CONFIG_NAME_TEXT)
        self.var_name_label.setText(VAR_NAME_TEXT)

        self.widget_label.setText(WIDGET_LABEL_TEXT)
        self.desc_label.setText(CONFIG_DESC_TEXT)
        self.is_required_label.setText(IS_REQUIRED_TEXT)

        self.fill_combo_box()

        self.default_value_label.setText(DEFAULT_VALUE_TEXT)
        self.default_text_edit_value_label.setText(DEFAULT_VALUE_TEXT)
        self.default_combox_value_label.setText(DEFAULT_VALUE_TEXT)
        self.placeholder_label.setText(PLACEHOLDER_TEXT)
        self.value_range_label.setText(VALUE_RANGE_TEXT)
        self.add_value_button.setText(ADD_VALUE_BTN_TEXT)

    def fill_combo_box(self):
        self.value_combo_box.addItems(CONFIG_INPUT_WIDGET_TYPE_DICT)
        self.value_combo_box.setCurrentIndex(0)

        self.is_required_combox.addItem('是')
        self.is_required_combox.addItem('否')
        self.is_required_combox.setCurrentIndex(0)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_child_signal(self):
        self.connect_text_edit_signal()
        self.desc_input.textChanged.connect(self.check_input)
        self.default_text_edit_value_input.textChanged.connect(self.check_input)
        self.is_required_combox.currentIndexChanged.connect(self.check_input)
        self.default_value_combo_box.currentIndexChanged.connect(self.check_input)
        self.value_combo_box.currentIndexChanged.connect(self.switch_stacked_widget)
        self.value_range_list_widget.changed_signal.connect(self.value_range_changed)
        self.add_value_button.clicked.connect(self.add_range_value)

    def connect_text_edit_signal(self):
        self.var_name_input.textEdited.connect(self.check_var_name_available)
        self.var_name_input.textEdited.connect(self.check_input)
        self.default_value_input.textEdited.connect(self.check_input)
        self.placeholder_input.textEdited.connect(self.check_input)

    def check_var_name_available(self, var_name):
        if self.var_name_check_action is Ellipsis:
            self.var_name_check_action = QAction(self)
        if var_name:
            self.var_name_available = self.do_check_var_name_available(var_name)
            set_name_input_style(self.var_name_available, var_name, self.old_var_name, 'var_name_input',
                                 self.var_name_input, self.var_name_check_action, self.var_name_checker)
        else:
            reset_name_input_style(self.var_name_input, self.var_name_checker, self.var_name_check_action)

    def do_check_var_name_available(self, var_name):
        if self.old_var_name:
            return (self.old_var_name != var_name and var_name not in self.var_names) or self.old_var_name == var_name
        else:
            return var_name not in self.var_names

    def button_available(self) -> bool:
        return self.name_input.displayText() and self.name_available \
            and self.var_name_input.displayText() and self.var_name_available

    def check_data_changed(self) -> bool:
        # 编辑时，回显数据导致的事件变化应忽略
        return (not self.dialog_data) or (self.echo_data_complete and self.new_dialog_data != self.dialog_data)

    def switch_stacked_widget(self, idx):
        idx = idx - 1 if idx > 1 else 0
        self.stacked_widget.setCurrentIndex(idx)
        self.check_input()

    def value_range_changed(self):
        # 重新刷新默认值下拉框值列表
        item_text_list = self.value_range_list_widget.collect_item_text_list()
        self.default_value_combo_box.clear()
        self.default_value_combo_box.addItems(item_text_list)
        self.check_input()

    def add_range_value(self):
        # 添加下拉框值列表项
        self.open_save_range_value_dialog(ADD_RANGE_VALUE_BOX_TITLE)

    def open_save_range_value_dialog(self, dialog_title, range_value=None):
        self.save_range_value_dialog = SimpleNameCheckDialog(self.parent_dialog.parent_screen_rect, dialog_title,
                                                             self.value_range_list_widget.collect_item_text_list(),
                                                             range_value)
        if range_value:
            self.save_range_value_dialog.edit_signal.connect(self.edit_combox_range_value)
        else:
            self.save_range_value_dialog.save_signal.connect(self.add_combox_range_value)
        self.save_range_value_dialog.exec()

    def edit_combox_range_value(self, value):
        self.value_range_list_widget.currentItem().setText(value)

    def add_combox_range_value(self, value):
        self.value_range_list_widget.addItem(value)

    def collect_input(self):
        self.new_dialog_data.config_name = self.name_input.displayText()
        self.new_dialog_data.output_var_name = self.var_name_input.displayText()
        self.new_dialog_data.config_value_widget = self.value_combo_box.currentText()
        required_text = self.is_required_combox.currentText()
        self.new_dialog_data.is_required = RequiredEnum.required.value \
            if required_text == '是' else RequiredEnum.not_required.value
        self.new_dialog_data.config_desc = self.desc_input.toPlainText()
        # 如果是文本输入类型控件，那么需要收集占位文本、默认值，如果是下拉框，收集默认值，下拉值列表
        current_widget_idx = self.value_combo_box.currentIndex()
        if current_widget_idx <= 1:
            # 清除下拉值列表
            self.new_dialog_data.range_values = ''
            # 收集数据
            self.new_dialog_data.placeholder_text = self.placeholder_input.displayText()
            self.new_dialog_data.default_value = self.default_value_input.displayText()
        elif current_widget_idx == 2:
            # 清除下拉值列表、占位文本
            self.new_dialog_data.placeholder_text = ''
            self.new_dialog_data.range_values = ''
            self.new_dialog_data.default_value = self.default_text_edit_value_input.toPlainText()
        elif current_widget_idx == 3:
            # 清除占位文本
            self.new_dialog_data.placeholder_text = ''
            # 收集数据
            self.new_dialog_data.default_value = self.default_value_combo_box.currentText()
            range_values = self.value_range_list_widget.collect_item_text_list()
            self.new_dialog_data.range_values = ",".join(range_values)
        elif current_widget_idx == 4:
            # 清除占位文本、默认值、下拉值列表
            self.new_dialog_data.placeholder_text = ''
            self.new_dialog_data.default_value = ''
            self.new_dialog_data.range_values = ''

    def save_func(self):
        # 原数据存在，说明是编辑
        if self.dialog_data:
            self.edit_signal.emit(self.new_dialog_data)
        else:
            self.save_signal.emit(self.new_dialog_data)
        self.parent_dialog.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 设置回显数据完成
        self.echo_data_complete = True

    def setup_other_input_limit_rule(self):
        self.var_name_input.setMaxLength(50)
        # 变量命名需要严格要求
        self.var_name_input.setValidator(QRegExpValidator(QRegExp(VAR_NAME_REG_RULE)))

    def setup_other_placeholder_text(self):
        self.var_name_input.setPlaceholderText(VAR_NAME_PLACEHOLDER_TEXT)

    def check_edit(self):
        """判断是否是编辑"""
        return self.dialog_data

    def get_old_name(self) -> str:
        return self.dialog_data.config_name

    def setup_echo_other_data(self):
        self.old_var_name = self.dialog_data.output_var_name
        self.var_name_input.setText(self.old_var_name)
        self.value_combo_box.setCurrentText(self.dialog_data.config_value_widget)
        self.is_required_combox.setCurrentText('是' if self.dialog_data.is_required else '否')
        self.desc_input.setPlainText(self.dialog_data.config_desc)
        # 如果是文本输入类型控件，那么需要回显占位文本、默认值，如果是下拉框，回显默认值，下拉值列表
        current_widget_idx = self.value_combo_box.currentIndex()
        if current_widget_idx <= 1:
            # 回显数据
            self.placeholder_input.setText(self.dialog_data.placeholder_text)
            self.default_value_input.setText(self.dialog_data.default_value)
        elif current_widget_idx == 2:
            # 回显数据
            self.default_text_edit_value_input.setPlainText(self.dialog_data.default_value)
        elif current_widget_idx == 3:
            # 回显数据
            range_values = self.dialog_data.range_values.split(',')
            self.value_range_list_widget.addItems(range_values)
            self.default_value_combo_box.setCurrentText(self.dialog_data.default_value)

    # ------------------------------ 后置处理 end ------------------------------ #

