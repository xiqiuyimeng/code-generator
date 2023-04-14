# -*- coding: utf-8 -*-
from src.constant.generator_dialog_constant import BACK_TO_SELECT_TEMPLATE_TXT, FILL_TEMPLATE_VAR_CONFIG_TXT
from src.view.frame.generator.dynamic_render_template_config.dynamic_template_config_dialog_frame_abc import \
    DynamicTemplateConfigDialogFrameABC

_author_ = 'luwt'
_date_ = '2023/4/13 17:20'


class DynamicOutputConfigDialogFrame(DynamicTemplateConfigDialogFrameABC):
    """动态模板输出路径配置对话框框架"""

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def do_get_config_list(self) -> list:
        return self.template.output_config_list

    def do_set_other_label_text(self):
        self.previous_frame_button.setText(BACK_TO_SELECT_TEMPLATE_TXT)
        self.next_frame_button.setText(FILL_TEMPLATE_VAR_CONFIG_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #
