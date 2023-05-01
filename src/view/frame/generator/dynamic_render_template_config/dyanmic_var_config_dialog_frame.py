# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QPushButton

from src.constant.generator_dialog_constant import BACK_TO_FILL_OUTPUT_CONFIG_TXT, GENERATE_TXT, PREVIEW_GENERATE_TXT
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.frame.generator.dynamic_render_template_config.dynamic_template_config_dialog_frame_abc import \
    DynamicTemplateConfigDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/13 17:20'


class DynamicVarConfigDialogFrame(DynamicTemplateConfigDialogFrameABC):
    """动态模板变量配置对话框框架"""

    def __init__(self, *args, **kwargs):
        self.preview_generate_button: QPushButton = ...
        self.preview_generate_frame: ChainDialogFrameABC = ...
        super().__init__(*args, **kwargs)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def do_get_config_list(self) -> list:
        return self.template.var_config_list

    def do_set_other_button(self) -> tuple:
        self.preview_generate_button = QPushButton()
        return self.preview_generate_button,

    def do_set_other_label_text(self):
        self.previous_frame_button.setText(BACK_TO_FILL_OUTPUT_CONFIG_TXT)
        self.next_frame_button.setText(GENERATE_TXT)
        self.preview_generate_button.setText(PREVIEW_GENERATE_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def do_connect_other_signal(self):
        self.preview_generate_button.clicked.connect(lambda: self.switch_frame(self.preview_generate_frame))

    # ------------------------------ 信号槽处理 end ------------------------------ #

    def set_preview_generate_frame(self, frame):
        self.preview_generate_frame = frame
