# -*- coding: utf-8 -*-
from src.constant.constant import SAVE_DS_INFO_TITLE
from src.view.dialog.name_check_dialog import NameCheckDialog

_author_ = 'luwt'
_date_ = '2022/5/29 17:55'


class AbstractDsInfoDialog(NameCheckDialog):
    """数据源对话框抽象类，整体对话框结构应为四部分：标题区、名称表单区、数据源信息表单区、按钮区"""

    def __init__(self, dialog_title, screen_rect, ds_name_list, data_id=None):
        # 数据源内容信息布局
        self.ds_info_layout = ...
        # 框架布局，分四部分，第一部分为标题部分，第二部分为数据源名称表单部分，第三部分为数据源内容信息部分、第四部分为按钮部分
        super().__init__(screen_rect, dialog_title, ds_name_list, data_id, data_id is not None)

    def setup_other_content_ui(self):
        # 构建数据源内容信息录入界面
        self.setup_ds_content_info_ui()
        self.frame_layout.addLayout(self.ds_info_layout)

    def setup_ds_content_info_ui(self): ...

    def ds_info_no_change(self):
        super().dialog_data_no_change(SAVE_DS_INFO_TITLE)

