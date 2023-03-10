# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel, QFormLayout, QTextEdit, QHBoxLayout, QWidget, QVBoxLayout, \
    QGridLayout, QPushButton, QSpacerItem, QFrame

from src.constant.type_mapping_dialog_constant import TYPE_MAPPING_TITLE, TYPE_MAPPING_NAME, DS_TYPE_TEXT, \
    TYPE_MAPPING_COMMENT_TEXT, TYPE_MAPPING_INFO_TEXT, TYPE_MAPPING_COL_TABLE_TEXT, SYNC_DS_COL_TYPE_BTN_TEXT, \
    ADD_COL_TYPE_MAPPING_BTN_TEXT, DEL_COL_TYPE_MAPPING_BTN_TEXT, ADD_MAPPING_GROUP_BTN_TEXT, \
    DEL_MAPPING_GROUP_BTN_TEXT, NO_COL_TYPES_PROMPT, \
    GET_COL_TYPES_TITLE, NO_DS_TYPE_PROMPT, GET_DS_TYPE_TITLE, CHECK_COL_TYPE_MAPPING_FRAGMENTARY_PROMPT, \
    CHECK_COL_TYPE_MAPPING_FRAGMENTARY_TITLE, READ_TYPE_MAPPING_BOX_TITLE, ADD_TYPE_MAPPING_BOX_TITLE, \
    EDIT_TYPE_MAPPING_BOX_TITLE, DS_COL_TYPE_LIST_BOX_TITLE
from src.service.async_func.async_ds_col_type_task import ListDsColTypeExecutor
from src.service.async_func.async_type_mapping_task import ReadTypeMappingExecutor, AddTypeMappingExecutor, \
    EditTypeMappingExecutor
from src.service.system_storage.type_mapping_sqlite import TypeMapping
from src.view.box.message_box import pop_fail
from src.view.custom_widget.ds_type_combo_box import DsTypeComboBox
from src.view.dialog.custom_stacked_widget_dialog import CustomStackedWidgetDialog
from src.view.table.table_widget.type_mapping_table_widget.col_type_mapping_table_widget import \
    ColTypeMappingTableWidget

_author_ = 'luwt'
_date_ = '2023/2/13 14:47'


class TypeMappingDetailDialog(CustomStackedWidgetDialog):
    add_data_signal = pyqtSignal(TypeMapping)
    edit_data_signal = pyqtSignal(TypeMapping)
    
    def __init__(self, screen_rect, type_mapping_names, type_mapping_id=None):
        self.dialog_data: TypeMapping = ...
        self.new_dialog_data: TypeMapping = ...

        # 第一个窗口，类型映射信息窗口
        self.mapping_info_widget: QWidget = ...
        self.mapping_info_layout: QVBoxLayout = ...
        # 基本信息输入表单的布局
        self.type_mapping_info_layout: QHBoxLayout = ...
        # 数据源类型下拉框表单布局
        self.ds_type_combo_box_layout: QFormLayout = ...
        self.ds_type_label: QLabel = ...
        self.ds_type_combo_box: DsTypeComboBox = ...
        # 数据源类型映射备注输入布局
        self.type_mapping_comment_layout: QFormLayout = ...
        self.type_mapping_comment_label: QLabel = ...
        self.type_mapping_comment_text_edit: QTextEdit = ...

        # 第二个窗口，列类型映射表格窗口
        self.col_type_widget: QWidget = ...
        self.col_type_layout: QVBoxLayout = ...
        # 数据源列类型映射表格上方按钮区布局
        self.col_type_button_layout: QGridLayout = ...
        # 同步数据源列类型按钮
        self.sync_ds_col_type_button: QPushButton = ...
        # 添加列类型映射按钮
        self.add_mapping_button: QPushButton = ...
        # 删除列类型映射按钮
        self.del_mapping_button: QPushButton = ...
        # 添加列类型映射组按钮
        self.add_mapping_group_button: QPushButton = ...
        # 删除列类型映射组按钮
        self.del_mapping_group_button: QPushButton = ...
        # 表格frame
        self.table_frame: QFrame = ...
        # 表格frame的layout
        self.table_frame_layout: QVBoxLayout = ...
        # 数据源类型列类型映射表格
        self.col_type_table_widget: ColTypeMappingTableWidget = ...

        # 读取数据库中保存的数据列类型列表执行器
        self.list_ds_col_type_executor: ListDsColTypeExecutor = ...
        # 当前获取到的数据列类型字典
        self.ds_col_type_dict: dict = ...
        # 添加类型映射执行器
        self.add_type_mapping_executor: AddTypeMappingExecutor = ...
        # 编辑类型映射执行器
        self.edit_type_mapping_executor: EditTypeMappingExecutor = ...
        super().__init__(screen_rect, TYPE_MAPPING_TITLE, type_mapping_names, type_mapping_id)

    def get_new_dialog_data(self) -> TypeMapping:
        return TypeMapping()

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def resize_dialog(self):
        self.resize(self.parent_screen_rect.width() * 0.7, self.parent_screen_rect.height() * 0.7)

    def fill_list_widget(self):
        self.list_widget.addItem(TYPE_MAPPING_INFO_TEXT)
        self.list_widget.addItem(TYPE_MAPPING_COL_TABLE_TEXT)

    def fill_stacked_widget(self):
        # 第一个窗口，备注文本输入框
        self.mapping_info_widget = QWidget(self.frame)
        self.stacked_widget.addWidget(self.mapping_info_widget)
        self.mapping_info_layout = QVBoxLayout()
        self.mapping_info_widget.setLayout(self.mapping_info_layout)
        # 基本信息输入表单
        self.setup_mapping_info_widget()

        # 第二个窗口，类型映射列类型表格
        self.col_type_widget = QWidget(self.frame)
        self.stacked_widget.addWidget(self.col_type_widget)
        self.col_type_layout = QVBoxLayout()
        self.col_type_widget.setLayout(self.col_type_layout)
        # 类型映射，列类型表格
        self.setup_col_type_widget()

    def setup_mapping_info_widget(self):
        # 构建映射名称输入表单
        self.setup_name_form()
        self.type_mapping_info_layout = QHBoxLayout()
        self.type_mapping_info_layout.addLayout(self.name_layout)
        self.type_mapping_info_layout.addSpacerItem(QSpacerItem(20, 1))

        # 构建数据源类型下拉框
        self.ds_type_combo_box_layout = QFormLayout()
        self.ds_type_label = QLabel(self.frame)

        self.ds_type_combo_box = DsTypeComboBox(self.frame)
        self.ds_type_combo_box_layout.addRow(self.ds_type_label, self.ds_type_combo_box)
        self.type_mapping_info_layout.addLayout(self.ds_type_combo_box_layout)
        self.mapping_info_layout.addLayout(self.type_mapping_info_layout)

        # 备注文本输入框
        self.type_mapping_comment_layout = QFormLayout()
        self.type_mapping_comment_label = QLabel(self.frame)
        self.type_mapping_comment_text_edit = QTextEdit(self.frame)
        self.type_mapping_comment_layout.addRow(self.type_mapping_comment_label,
                                                self.type_mapping_comment_text_edit)
        self.mapping_info_layout.addLayout(self.type_mapping_comment_layout)

    def setup_col_type_widget(self):
        # 首先构建按钮布局
        self.col_type_button_layout = QGridLayout()
        self.col_type_layout.addLayout(self.col_type_button_layout)

        # 增加间距
        self.col_type_layout.setSpacing(20)

        # 构建按钮
        self.sync_ds_col_type_button = QPushButton(self.frame)
        self.col_type_button_layout.addWidget(self.sync_ds_col_type_button, 0, 0, 1, 1)
        self.add_mapping_button = QPushButton(self.frame)
        self.col_type_button_layout.addWidget(self.add_mapping_button, 0, 1, 1, 1)
        self.del_mapping_button = QPushButton(self.frame)
        self.col_type_button_layout.addWidget(self.del_mapping_button, 0, 2, 1, 1)
        self.add_mapping_group_button = QPushButton(self.frame)
        self.col_type_button_layout.addWidget(self.add_mapping_group_button, 0, 3, 1, 1)
        self.del_mapping_group_button = QPushButton(self.frame)
        self.col_type_button_layout.addWidget(self.del_mapping_group_button, 0, 4, 1, 1)

        # 构建表格
        self.table_frame = QFrame(self.frame)
        self.table_frame_layout = QVBoxLayout(self.table_frame)
        # 将表格布局边距清空
        self.table_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.col_type_table_widget = ColTypeMappingTableWidget(self.table_frame)
        self.table_frame_layout.addWidget(self.col_type_table_widget)
        self.col_type_layout.addWidget(self.table_frame)

    def setup_other_label_text(self):
        self.name_label.setText(TYPE_MAPPING_NAME)
        self.ds_type_label.setText(DS_TYPE_TEXT)
        self.type_mapping_comment_label.setText(TYPE_MAPPING_COMMENT_TEXT)
        self.sync_ds_col_type_button.setText(SYNC_DS_COL_TYPE_BTN_TEXT)
        self.add_mapping_button.setText(ADD_COL_TYPE_MAPPING_BTN_TEXT)
        self.del_mapping_button.setText(DEL_COL_TYPE_MAPPING_BTN_TEXT)
        self.add_mapping_group_button.setText(ADD_MAPPING_GROUP_BTN_TEXT)
        self.del_mapping_group_button.setText(DEL_MAPPING_GROUP_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def collect_input(self):
        # 收集基本信息数据
        self.new_dialog_data.mapping_name = self.name_input.text()
        self.new_dialog_data.ds_type = self.ds_type_combo_box.currentText()
        self.new_dialog_data.comment = self.type_mapping_comment_text_edit.toPlainText()
        self.new_dialog_data.max_col_type_group_num = self.col_type_table_widget.header_widget.max_group_num
        self.new_dialog_data.type_mapping_cols = self.col_type_table_widget.collect_data()

    def button_available(self) -> bool:
        return all((self.new_dialog_data.mapping_name, self.new_dialog_data.ds_type, self.name_available))

    def connect_child_signal(self):
        self.ds_type_combo_box.currentIndexChanged.connect(self.check_input)
        # 连接表格信号，动态渲染删除类型映射按钮状态
        self.col_type_table_widget.header_check_changed.connect(self.set_del_mapping_button_available)
        # 连接表头信号，动态渲染删除类型映射组按钮状态
        self.col_type_table_widget.header_widget.group_num_changed.connect(self.set_del_mapping_group_button_available)

        # 按钮点击信号
        self.sync_ds_col_type_button.clicked.connect(self.sync_ds_col_types)
        # 添加类型映射
        self.add_mapping_button.clicked.connect(self.col_type_table_widget.add_type_mapping)
        # 删除类型映射
        self.del_mapping_button.clicked.connect(self.col_type_table_widget.del_type_mapping)
        # 添加映射组
        self.add_mapping_group_button.clicked.connect(self.col_type_table_widget.add_type_mapping_group)
        # 删除映射组
        self.del_mapping_group_button.clicked.connect(self.col_type_table_widget.del_type_mapping_group)

    def set_del_mapping_button_available(self, checked):
        # 当表格存在行，再动态渲染删除映射按钮状态，否则置为不可用
        if self.col_type_table_widget.rowCount():
            self.del_mapping_button.setDisabled(not checked)
        else:
            self.del_mapping_button.setDisabled(True)

    def set_del_mapping_group_button_available(self, max_group_num):
        # 删除类型映射组按钮，根据是否存在额外组来决定
        if max_group_num > 0:
            self.del_mapping_group_button.setDisabled(False)
        else:
            self.del_mapping_group_button.setDisabled(True)

    def sync_ds_col_types(self):
        """根据数据源类型获取所有的列类型，如果获取不到，弹窗提示应维护数据源列类型数据"""
        ds_type = self.ds_type_combo_box.currentText()
        if ds_type:
            col_types = self.ds_col_type_dict.get(ds_type)
            if col_types:
                self.col_type_table_widget.sync_col_types(col_types)
            else:
                pop_fail(NO_COL_TYPES_PROMPT, GET_COL_TYPES_TITLE, self.frame)
        else:
            # 如果还未选择数据源类型，提示
            pop_fail(NO_DS_TYPE_PROMPT, GET_DS_TYPE_TITLE, self.frame)

    def save_func(self):
        # 检查表格中数据是否可以提交
        fragmentary_data_prompt_list = self.col_type_table_widget.check_fragmentary_data()
        if fragmentary_data_prompt_list:
            pop_fail(CHECK_COL_TYPE_MAPPING_FRAGMENTARY_PROMPT.format("\n".join(fragmentary_data_prompt_list)),
                     CHECK_COL_TYPE_MAPPING_FRAGMENTARY_TITLE, self)
            return
        # 手动收集数据
        self.collect_input()
        # 如果存在原数据，说明是编辑
        if self.dialog_data:
            self.new_dialog_data.id = self.dialog_data.id
            self.edit_type_mapping_executor = EditTypeMappingExecutor(self.new_dialog_data, self, self,
                                                                      EDIT_TYPE_MAPPING_BOX_TITLE,
                                                                      self.edit_post_process)
            self.edit_type_mapping_executor.start()
        else:
            self.add_type_mapping_executor = AddTypeMappingExecutor(self.new_dialog_data, self, self,
                                                                    ADD_TYPE_MAPPING_BOX_TITLE,
                                                                    self.add_post_process)
            self.add_type_mapping_executor.start()

    def add_post_process(self):
        self.add_data_signal.emit(self.new_dialog_data)
        self.close()

    def edit_post_process(self):
        self.edit_data_signal.emit(self.new_dialog_data)
        self.close()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        # 获取数据源列类型
        self.list_ds_col_type_executor = ListDsColTypeExecutor(self, self, DS_COL_TYPE_LIST_BOX_TITLE,
                                                               self.list_col_type_callback)
        self.list_ds_col_type_executor.start()

    def list_col_type_callback(self, col_type_dict: dict):
        self.ds_col_type_dict = col_type_dict

    def get_read_storage_executor(self, callback):
        return ReadTypeMappingExecutor(self.dialog_data, self, self, READ_TYPE_MAPPING_BOX_TITLE, callback)

    def init_lineedit_button_status(self):
        super().init_lineedit_button_status()
        # 设置删除按钮状态
        self.init_del_button_status()

    def init_del_button_status(self):
        # 删除类型映射按钮，初始应该是不可用状态
        self.set_del_mapping_button_available(False)
        # 删除类型映射组按钮状态
        self.set_del_mapping_group_button_available(self.col_type_table_widget.header_widget.max_group_num)

    def get_old_name(self) -> str:
        return self.dialog_data.mapping_name

    def setup_echo_other_data(self):
        self.ds_type_combo_box.echo_ds_type(self.dialog_data.ds_type)
        self.type_mapping_comment_text_edit.setPlainText(self.dialog_data.comment)
        # 回显表格数据
        self.col_type_table_widget.fill_table(self.dialog_data)

    # ------------------------------ 后置处理 end ------------------------------ #
