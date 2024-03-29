# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QStackedWidget, QFrame, QVBoxLayout, QLabel, QFormLayout

from src.constant.template_dialog_constant import TEMPLATE_CONFIG_LIST_BOX_TITLE, NO_TEMPLATE_CONFIG_ITEMS_TEXT, \
    NOT_FILL_ALL_REQUIRED_INPUT_TXT, REQUIRED_CHECK_BOX_TITLE, NO_TEMPLATE_PROMPT, NO_TEMPLATE_TITLE
from src.service.async_func.async_template_task import ListTemplateConfigExecutor
from src.view.box.message_box import pop_fail
from src.view.custom_widget.scrollable_widget import ScrollArea
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.widget.template.config_value_widget import get_config_value_widget, ConfigValueWidgetABC

_author_ = 'luwt'
_date_ = '2023/4/6 9:09'


class DynamicTemplateConfigDialogFrameABC(ChainDialogFrameABC):
    """动态模板配置对话框框架，根据模板配置动态生成页面"""

    def __init__(self, *args, template_config_list=None, template=None,
                 get_template_func=None, preview_mode=False):
        # 如果是预览模式，直接传递配置项列表
        self.template_config_list = template_config_list
        # 当前模板，记录当前使用的模板，方便对比，判断是否需要重新渲染页面
        self.template = template
        # 获取模板的方法
        self.get_template_func = get_template_func
        # 如果是预览模式，仅展示配置页效果，不添加按钮
        self.preview_mode = preview_mode
        # 配置项数据字典
        self.config_data_dict: dict = ...
        # 配置项列表
        self.config_widget_list: list = ...
        # 缓存内容页，key为模板id
        self.content_frame_dict: dict = ...
        self.stacked_widget: QStackedWidget = ...
        self.no_data_frame: QFrame = ...
        self.no_data_layout: QVBoxLayout = ...
        self.no_data_label: QLabel = ...
        self.content_scroll_area: ScrollArea = ...
        self.canvas_content_frame: QFrame = ...
        self.canvas_content_frame_layout: QFormLayout = ...
        self.list_template_config_executor: ListTemplateConfigExecutor = ...
        super().__init__(*args)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.content_frame_dict = dict()
        self.stacked_widget = QStackedWidget()
        self.frame_layout.addWidget(self.stacked_widget)
        # 如果是预览模式，且配置列表不为空，直接渲染；实际生成过程中调用，渲染页面需要后置
        if self.preview_mode:
            content_frame = self.do_get_content_frame()
            self.stacked_widget.addWidget(content_frame)

    def setup_stacked_ui(self):
        # 设置堆栈式窗口的当前控件
        self.stacked_widget.setCurrentWidget(self.get_content_frame())

    def get_content_frame(self):
        # 首先从缓存中获取框架，如果获取不到，再进行创建
        cache_content_frame_tuple = self.content_frame_dict.get(self.template.id)
        if not cache_content_frame_tuple:
            content_frame = self.do_get_content_frame()
            self.stacked_widget.addWidget(content_frame)
            cache_content_frame_tuple = content_frame, self.config_widget_list
            # 放入缓存
            self.content_frame_dict[self.template.id] = cache_content_frame_tuple
        else:
            # config_widget_list 赋值
            self.config_widget_list = cache_content_frame_tuple[1]
        return cache_content_frame_tuple[0]

    def do_get_content_frame(self):
        # 如果配置项列表存在，根据配置项动态渲染页面，否则创建无数据页面
        if self.get_config_list():
            self.setup_content_scroll_area()
            return self.content_scroll_area
        else:
            self.setup_no_data_frame()
            return self.no_data_frame

    def get_config_list(self) -> list:
        if self.preview_mode:
            return self.template_config_list
        else:
            return self.do_get_config_list()

    def do_get_config_list(self) -> list:
        ...

    def setup_content_scroll_area(self):
        self.content_scroll_area = ScrollArea()
        # 画布控件
        self.canvas_content_frame = QFrame(self)
        self.canvas_content_frame.setObjectName('canvas_content_frame')
        self.canvas_content_frame_layout = QVBoxLayout(self.canvas_content_frame)
        # 设置画布控件
        self.content_scroll_area.set_canvas_widget(self.canvas_content_frame)

        # 在真实控件之上，增加一个空白label，允许布局拉伸label，以保持真实控件的固定高度，避免变形
        self.canvas_content_frame_layout.addWidget(QLabel())

        if self.get_config_list():
            if not self.preview_mode:
                self.config_widget_list = list()
            for config in self.get_config_list():
                config_value_widget: ConfigValueWidgetABC = get_config_value_widget(config)
                # 为了美观，将控件高度固定
                config_value_widget.setFixedHeight(config_value_widget.sizeHint().height())
                self.canvas_content_frame_layout.addWidget(config_value_widget)
                if self.config_widget_list is not Ellipsis:
                    self.config_widget_list.append(config_value_widget)

        # 在真实控件之下，增加一个空白label，与上面的空白label对称，使得真实控件靠近中间
        self.canvas_content_frame_layout.addWidget(QLabel())

    def setup_no_data_frame(self):
        self.no_data_frame = QFrame()
        self.no_data_layout = QVBoxLayout(self.no_data_frame)
        self.no_data_label = QLabel(self.no_data_frame)
        self.no_data_label.setObjectName('no_config_data_label')
        self.no_data_label.setText(NO_TEMPLATE_CONFIG_ITEMS_TEXT)
        self.no_data_layout.addWidget(self.no_data_label)

    def get_blank_left_buttons(self) -> tuple:
        if self.preview_mode:
            return tuple()
        return super().get_blank_left_buttons()

    def setup_other_label_text(self):
        if self.preview_mode:
            return
        self.do_set_other_label_text()

    def do_set_other_label_text(self):
        ...

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        if self.preview_mode:
            return
        super().connect_other_signal()

    # ------------------------------ 信号槽处理 end ------------------------------ #

    def switch_frame(self, frame):
        # 只要不是回退，都需要收集数据
        if frame is not self.previous_frame:
            if self.config_widget_list is not Ellipsis:
                self.config_data_dict = {config.config.id: config.collect_data()
                                         for config in self.config_widget_list}
                # 找出必填的变量配置id
                required_var_ids = {config.id for config in self.get_config_list() if config.is_required}
                if required_var_ids:
                    # 如果还有未填完的值，提示
                    filled_var_ids = {config_id for config_id, config_value in self.config_data_dict.items()
                                      if config_value}
                    if not required_var_ids.issubset(filled_var_ids):
                        pop_fail(NOT_FILL_ALL_REQUIRED_INPUT_TXT, REQUIRED_CHECK_BOX_TITLE, self)
                        return
            # 更新父对话框数据
            self.update_parent_dialog_config_dict()
        # 如果是回退，清空数据
        elif frame is self.previous_frame:
            self.config_widget_list = ...
            self.config_data_dict = ...
        super().switch_frame(frame)

    def update_parent_dialog_config_dict(self):
        ...

    def show(self):
        super().show()
        # 当展示页面时，进行动态渲染页面
        if not self.preview_mode and self.get_template_func:
            template = self.get_template_func()
            if template is Ellipsis:
                pop_fail(NO_TEMPLATE_PROMPT, NO_TEMPLATE_TITLE, self)
                # 如果没有模板，没必要继续了
                self.parent_dialog.close()
                return
            if not self.template:
                # 如果当前模板不存在，记录当前模板，动态渲染页面
                self.template = template
                self.dynamic_render_content()
            else:
                # 如果当前模板已经存在，且获取到的模板不是当前模板，首先查看是否已经渲染过，如果没有渲染过，需要重新渲染页面
                if template.id != self.template.id:
                    self.template = template
                    if template.id in self.content_frame_dict:
                        self.setup_stacked_ui()
                    else:
                        self.dynamic_render_content()
                else:
                    # 如果获取到的模板是当前模板，不需要读取数据库渲染
                    self.setup_stacked_ui()

    def dynamic_render_content(self):
        # 根据 template_id 获取配置项，之所以在这里读取模板配置数据，而不是在模板列表，是为了尽量减少空间占用
        self.list_template_config_executor = ListTemplateConfigExecutor(self.template.id, self.parent_dialog,
                                                                        self.parent_dialog,
                                                                        TEMPLATE_CONFIG_LIST_BOX_TITLE,
                                                                        self.render_content)
        self.list_template_config_executor.start()

    def render_content(self, output_config_list, var_config_list):
        self.template.output_config_list = output_config_list
        self.template.var_config_list = var_config_list
        self.setup_stacked_ui()
        # 如果下一个框架依然拥有 template，传递值，避免下一个框架重复读取数据库
        if hasattr(self.next_frame, 'template'):
            setattr(self.next_frame, 'template', self.template)
