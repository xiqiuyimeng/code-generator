# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressBar, QFormLayout, QLabel, QPushButton

from src.constant.generator_dialog_constant import PREPARE_PROGRESS_LABEL_TXT, GENERATE_PROGRESS_LABEL_TXT, \
    GENERATE_LOG_LABEL_TXT, BACK_TO_FILL_TEMPLATE_VAR_CONFIG_BTN_TXT, GENERATE_TO_FILE_BTN_TXT, \
    PREVIEW_GENERATE_BTN_TXT, GENERATE_TO_FILE_TITLE, PREVIEW_GENERATE_TITLE, NO_FILE_TO_PREVIEW_PROMPT
from src.service.async_func.async_generate_task import GenerateExecutor, PreviewGenerateExecutor
from src.view.box.message_box import pop_fail
from src.view.custom_widget.scrollable_widget import ScrollableTextBrowser
from src.view.dialog.generator.preview_file_dialog import PreviewFileDialog
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/25 9:37'


class GenerateDialogFrame(ChainDialogFrameABC):
    """生成页对话框框架"""

    def __init__(self, *args):
        # 存放预览数据字典，k：文件名称，v：（文件内容、文件目录路径解析结果）
        self.preview_data_dict: dict = ...
        self.generator_layout: QFormLayout = ...
        # 准备工作进度label
        self.prepare_progress_label: QLabel = ...
        # 准备工作进度条
        self.prepare_progress_bar: QProgressBar = ...
        # 生成进度label
        self.generate_progress_label: QLabel = ...
        # 生成进度条
        self.generate_progress_bar: QProgressBar = ...
        # 生成工作日志label
        self.generate_log_label: QLabel = ...
        # 生成工作日志展示区
        self.generate_log_browser: ScrollableTextBrowser = ...
        # 预览生成按钮
        self.preview_generate_button: QPushButton = ...
        # 按钮列表，在生成期间需要禁用
        self.need_disable_button_list: list = ...
        # 生成执行器
        self.generate_executor: GenerateExecutor = ...
        # 预览生成执行器
        self.preview_generate_executor: PreviewGenerateExecutor = ...
        # 预览对话框
        self.preview_file_dialog: PreviewFileDialog = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.generator_layout = QFormLayout(self)
        self.frame_layout.addLayout(self.generator_layout)

        # 准备工作进度
        self.prepare_progress_label = QLabel(self)
        self.prepare_progress_bar = QProgressBar(self)
        self.prepare_progress_bar.setAlignment(Qt.AlignCenter)
        self.generator_layout.addRow(self.prepare_progress_label, self.prepare_progress_bar)

        # 生成进度
        self.generate_progress_label = QLabel(self)
        self.generate_progress_bar = QProgressBar(self)
        self.generate_progress_bar.setAlignment(Qt.AlignCenter)
        self.generator_layout.addRow(self.generate_progress_label, self.generate_progress_bar)

        # 工作日志
        self.generate_log_label = QLabel(self)
        self.generate_log_label.setAlignment(Qt.AlignTop)
        self.generate_log_browser = ScrollableTextBrowser(self)
        self.generator_layout.addRow(self.generate_log_label, self.generate_log_browser)

    def get_blank_left_buttons(self):
        left_buttons = super().get_blank_left_buttons()
        # 增加预览生成按钮
        self.preview_generate_button = QPushButton(self)
        return *left_buttons, self.preview_generate_button

    def setup_other_label_text(self):
        self.prepare_progress_label.setText(PREPARE_PROGRESS_LABEL_TXT)
        self.generate_progress_label.setText(GENERATE_PROGRESS_LABEL_TXT)
        self.generate_log_label.setText(GENERATE_LOG_LABEL_TXT)
        self.previous_frame_button.setText(BACK_TO_FILL_TEMPLATE_VAR_CONFIG_BTN_TXT)
        self.next_frame_button.setText(GENERATE_TO_FILE_BTN_TXT)
        self.preview_generate_button.setText(PREVIEW_GENERATE_BTN_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        self.previous_frame_button.clicked.connect(lambda: self.switch_frame(self.previous_frame))
        # 生成到文件
        self.next_frame_button.clicked.connect(self.generate_to_file)
        # 预览生成
        self.preview_generate_button.clicked.connect(self.preview_generate)

    def switch_frame(self, frame):
        # 在返回上一页时，清空当前页数据
        self.before_generate_work()
        super().switch_frame(frame)

    def generate_to_file(self):
        self.collect_need_disable_buttons()
        type_mapping_id = self.parent_dialog.type_mapping.id if self.parent_dialog.type_mapping else None
        self.generate_executor = GenerateExecutor(self.parent_dialog.selected_data, type_mapping_id,
                                                  self.parent_dialog.template,
                                                  self.parent_dialog.output_config_input_dict,
                                                  self.parent_dialog.var_config_input_dict,
                                                  self.need_disable_button_list,
                                                  self.prepare_progress_bar.setValue,
                                                  self.generate_progress_bar.setValue,
                                                  self.generate_log_browser.append,
                                                  self.parent_dialog, GENERATE_TO_FILE_TITLE)
        self.before_generate_work()
        # 开始生成
        self.generate_executor.start()

    def before_generate_work(self):
        # 初始化进度条
        self.prepare_progress_bar.setValue(0)
        self.generate_progress_bar.setValue(0)
        # 清空日志输出
        self.generate_log_browser.clear()

    def collect_need_disable_buttons(self):
        if self.need_disable_button_list is Ellipsis:
            # 收集按钮列表
            self.need_disable_button_list = [self.previous_frame_button, self.next_frame_button,
                                             self.preview_generate_button, self.dialog_quit_button]

    def preview_generate(self):
        self.collect_need_disable_buttons()
        type_mapping_id = self.parent_dialog.type_mapping.id if self.parent_dialog.type_mapping else None
        self.preview_generate_executor = PreviewGenerateExecutor(self.parent_dialog.selected_data, type_mapping_id,
                                                                 self.parent_dialog.template,
                                                                 self.parent_dialog.output_config_input_dict,
                                                                 self.parent_dialog.var_config_input_dict,
                                                                 self.need_disable_button_list,
                                                                 self.prepare_progress_bar.setValue,
                                                                 self.generate_progress_bar.setValue,
                                                                 self.generate_log_browser.append,
                                                                 self.parent_dialog, PREVIEW_GENERATE_TITLE,
                                                                 self.open_preview_dialog,
                                                                 generate_file_callback=self.collect_preview_data)
        self.before_generate_work()
        self.preview_data_dict = dict()
        self.preview_generate_executor.start()

    def open_preview_dialog(self):
        # 如果没有需要预览的文件，提示
        if not self.preview_data_dict:
            pop_fail(NO_FILE_TO_PREVIEW_PROMPT, PREVIEW_GENERATE_TITLE, self)
            return
        self.preview_file_dialog = PreviewFileDialog(self.preview_data_dict)
        self.preview_file_dialog.exec()

    def collect_preview_data(self, file_name, file_content, file_path_tuple):
        self.preview_data_dict[file_name] = file_content, file_path_tuple

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 初始化进度条
        self.before_generate_work()

    # ------------------------------ 后置处理 end ------------------------------ #
