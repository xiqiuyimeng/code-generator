# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.help.help_constant import TEMPLATE_COPY_FUNC_HELP
from src.constant.template_dialog_constant import HAS_FUNC_TEMPLATE_LIST_BOX_TITLE, TEMPLATE_FUNC_TITLE, \
    COPY_FUNC_DUPLICATE_PROMPT, COPY_FUNC_BOX_TITLE, COPY_FUNC_SUCCESS_PROMPT, COPY_FUNC_SUCCESS_BOX_TITLE
from src.service.async_func.async_template_task import ListHasFuncTemplateExecutor
from src.view.box.message_box import pop_question, pop_ok
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.frame.template.template_copy_func_list_frame import TemplateCopyFuncListFrame
from src.view.list_widget.has_func_template_list_widget import HasFuncTemplateListWidget

_author_ = 'luwt'
_date_ = '2023/6/25 17:40'


class TemplateCopyFuncDialogFrame(DialogFrameABC):
    """复制模板方法对话框框架，模板列表"""
    copy_func_list_signal = pyqtSignal(list)

    def __init__(self, excluded_template_id, func_names, *args):
        # 模板id，当前正在编辑的模板id，也就是需要排除的模板id
        self.excluded_template_id = excluded_template_id
        # 当前模板已经存在的模板方法名称列表
        self.func_names: list = func_names
        # 存放 template_id: frame
        self.template_id_frame_dict = dict()
        self.template_list_widget: HasFuncTemplateListWidget = ...
        self.list_has_func_template_executor: ListHasFuncTemplateExecutor = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.template_list_widget = HasFuncTemplateListWidget(self, self.switch_frame)
        self.frame_layout.addWidget(self.template_list_widget)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def get_help_info_type(self) -> str:
        return TEMPLATE_COPY_FUNC_HELP

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_has_func_template_executor = ListHasFuncTemplateExecutor(self.excluded_template_id,
                                                                           self.parent_dialog, self.parent_dialog,
                                                                           HAS_FUNC_TEMPLATE_LIST_BOX_TITLE,
                                                                           self.fill_list_widget)
        self.list_has_func_template_executor.start()

    def fill_list_widget(self, template_list):
        self.template_list_widget.fill_list_widget(template_list)

    # ------------------------------ 后置处理 end ------------------------------ #

    def switch_frame(self, template_id, template_name):
        # 从缓存中取frame，如果没有，那么创建frame
        frame = self.template_id_frame_dict.get(template_id)
        if not frame:
            frame = self.create_template_func_frame(template_id, template_name)
            self.template_id_frame_dict[template_id] = frame
        # 切换页面
        self.parent_dialog.layout().removeWidget(self)
        self.hide()
        self.parent_dialog.layout().addWidget(frame)
        if frame.isHidden():
            frame.show()

    def create_template_func_frame(self, template_id, template_name):
        return TemplateCopyFuncListFrame(template_id, self, self.copy_template_func_list,
                                         self.parent_dialog, TEMPLATE_FUNC_TITLE.format(template_name))

    def copy_template_func_list(self, func_list):
        # 首先检查是否存在重复的，重复需要提示是否覆盖
        duplicate_func_list = [func for func in func_list if func.func_name in self.func_names]
        if duplicate_func_list:
            # 如果选择跳过，那么应该将这些从方法列表移除
            duplicate_func_names = [func.func_name for func in duplicate_func_list]
            prompt = COPY_FUNC_DUPLICATE_PROMPT.format('\n    '.join(duplicate_func_names))
            if not pop_question(prompt, COPY_FUNC_BOX_TITLE, self.parent_dialog):
                for duplicate_func in duplicate_func_list:
                    func_list.remove(duplicate_func)
        # 发射信号
        self.copy_func_list_signal.emit(func_list)
        # 将这些方法名称加入到已存在方法名称列表
        add_func_names = [func.func_name for func in func_list if func.func_name not in self.func_names]
        self.func_names.extend(add_func_names)
        # 提示成功
        pop_ok(COPY_FUNC_SUCCESS_PROMPT.format(len(func_list)), COPY_FUNC_SUCCESS_BOX_TITLE, self.parent_dialog)
