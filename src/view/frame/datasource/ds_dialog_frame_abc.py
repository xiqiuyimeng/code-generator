# -*- coding: utf-8 -*-
from src.view.frame.name_check_dialog_frame import NameCheckDialogFrame

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class DsDialogFrameABC(NameCheckDialogFrame):
    """数据源对话框框架抽象类，整体结构应为四部分：标题区、名称表单区、数据源信息表单区、按钮区"""

    def __init__(self, parent_dialog, dialog_title, ds_name_list, data_id=None, **kwargs):
        # 数据源内容信息布局
        self.ds_info_layout = ...
        # 框架布局，分四部分，第一部分为标题部分，第二部分为数据源名称表单部分，第三部分为数据源内容信息部分、第四部分为按钮部分
        super().__init__(parent_dialog, dialog_title, ds_name_list, data_id, data_id is not None, **kwargs)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_other_content_ui(self):
        # 构建数据源内容信息录入界面
        self.setup_ds_content_info_ui()
        self.frame_layout.addLayout(self.ds_info_layout)

    def setup_ds_content_info_ui(self): ...

    # ------------------------------ 创建ui界面 end ------------------------------ #
