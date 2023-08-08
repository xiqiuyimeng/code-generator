# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFormLayout, QLabel, QProgressBar

from src.constant.generator_dialog_constant import SAVE_PREVIEW_FILE_PROGRESS_TEXT
from src.service.async_func.async_generate_task import SaveFileExecutor
from src.view.frame.dialog_frame_abc import DialogFrameABC

_author_ = 'luwt'
_date_ = '2023/5/6 14:28'


class SaveFileDialogFrame(DialogFrameABC):

    def __init__(self, save_file_dict, *args):
        self.save_file_dict = save_file_dict
        self.content_layout: QFormLayout = ...
        self.save_progress_label: QLabel = ...
        self.save_progress_bar: QProgressBar = ...
        # 保存到文件的执行器
        self.save_file_executor: SaveFileExecutor = ...
        super().__init__(*args, need_help_button=False)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def setup_content_ui(self):
        self.content_layout = QFormLayout(self)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.addLayout(self.content_layout)
        self.save_progress_label = QLabel(self)
        self.save_progress_bar = QProgressBar(self)
        self.save_progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addRow(self.save_progress_label, self.save_progress_bar)

    def setup_other_label_text(self):
        self.save_progress_label.setText(SAVE_PREVIEW_FILE_PROGRESS_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        super().post_process()
        self.save_progress_bar.setValue(0)
        # 开始保存
        self.save_file_executor = SaveFileExecutor(self.save_file_dict, self.dialog_quit_button,
                                                   self.save_progress_bar.setValue, self, self.dialog_title)
        self.save_file_executor.start()

    # ------------------------------ 后置处理 end ------------------------------ #
