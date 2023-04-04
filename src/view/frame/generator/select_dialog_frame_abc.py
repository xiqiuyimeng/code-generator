# -*- coding: utf-8 -*-
from src.service.async_func.async_task_abc import LoadingMaskThreadExecutor
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.list_widget.list_widget_abc import ListWidgetABC

_author_ = 'luwt'
_date_ = '2023/4/4 17:01'


class SelectDialogFrame(ChainDialogFrameABC):

    def __init__(self, *args):
        self.data_list: list = ...
        # 展示数据列表
        self.list_widget: ListWidgetABC = ...
        # 读取数据列表执行器
        self.list_data_executor: LoadingMaskThreadExecutor = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        # 展示数据列表
        self.list_widget = ListWidgetABC(self)
        self.frame_layout.addWidget(self.list_widget)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        self.list_data_executor = self.get_list_data_executor()
        self.list_data_executor.start()

    def get_list_data_executor(self) -> LoadingMaskThreadExecutor: ...

    def fill_list_widget(self, data_list):
        """填充页面列表，获取数据库数据以后的回调函数"""
        if data_list:
            self.data_list = data_list
            self.list_widget.addItems(self.get_item_names())
            # 默认选中第一个元素
            self.list_widget.setCurrentRow(0)

    def get_item_names(self) -> iter: ...

    # ------------------------------ 后置处理 end ------------------------------ #
