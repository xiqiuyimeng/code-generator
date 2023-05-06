# -*- coding: utf-8 -*-
from src.constant.generator_dialog_constant import BACK_TO_SELECTED_DATA_BTN_TXT, CHOOSE_TEMPLATE_BTN_TXT
from src.constant.type_mapping_dialog_constant import TYPE_MAPPING_BOX_TITLE
from src.service.async_func.async_type_mapping_task import ListTypeMappingExecutor
from src.view.frame.generator.select_list.select_dialog_frame_abc import SelectDialogFrame

_author_ = 'luwt'
_date_ = '2023/4/4 16:35'


class SelectTypeMappingDialogFrame(SelectDialogFrame):
    """选择类型映射对话框框架"""

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_label_text(self):
        self.previous_frame_button.setText(BACK_TO_SELECTED_DATA_BTN_TXT)
        self.next_frame_button.setText(CHOOSE_TEMPLATE_BTN_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def get_list_data_executor(self) -> ListTypeMappingExecutor:
        return ListTypeMappingExecutor(self.parent_dialog, self.parent_dialog,
                                       TYPE_MAPPING_BOX_TITLE, self.fill_list_widget)

    def get_item_names(self) -> iter:
        return map(lambda x: x.mapping_name, self.data_list)

    # ------------------------------ 后置处理 end ------------------------------ #
