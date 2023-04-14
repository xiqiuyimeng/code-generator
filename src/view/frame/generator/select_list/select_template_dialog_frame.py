# -*- coding: utf-8 -*-
from src.constant.generator_dialog_constant import BACK_TO_SELECT_TYPE_MAPPING_TXT, FILL_TEMPLATE_OUTPUT_CONFIG_TXT
from src.constant.template_dialog_constant import TEMPLATE_LIST_BOX_TITLE
from src.service.async_func.async_template_task import ListTemplateExecutor
from src.view.frame.generator.select_list.select_dialog_frame_abc import SelectDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/4 16:35'


class SelectTemplateDialogFrame(SelectDialogFrame):
    """选择模板对话框框架"""

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_label_text(self):
        self.previous_frame_button.setText(BACK_TO_SELECT_TYPE_MAPPING_TXT)
        self.next_frame_button.setText(FILL_TEMPLATE_OUTPUT_CONFIG_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_list_data_executor(self) -> ListTemplateExecutor:
        return ListTemplateExecutor(self.parent_dialog, self.parent_dialog,
                                    TEMPLATE_LIST_BOX_TITLE, self.fill_list_widget)

    def get_item_names(self) -> iter:
        return map(lambda x: x.template_name, self.data_list)

    # ------------------------------ 后置处理 end ------------------------------ #
