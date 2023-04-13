# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QFrame, QVBoxLayout, QLabel, QFormLayout

from src.constant.generator_dialog_constant import BACK_TO_SELECT_TEMPLATE_TXT, GENERATE_TXT, PREVIEW_GENERATE_TXT
from src.constant.template_dialog_constant import TEMPLATE_CONFIG_LIST_BOX_TITLE, NO_TEMPLATE_CONFIG_ITEMS_TEXT, \
    NOT_FILL_ALL_REQUIRED_INPUT_TXT, REQUIRED_CHECK_BOX_TITLE
from src.service.async_func.async_template_task import ListTemplateConfigExecutor
from src.view.box.message_box import pop_fail
from src.view.custom_widget.scrollable_widget import ScrollArea
from src.view.frame.generator.chain_dialog_frame import ChainDialogFrameABC
from src.view.widget.template.config_value_widget import get_config_value_widget, ConfigValueWidgetABC

_author_ = 'luwt'
_date_ = '2023/4/6 9:09'


class DynamicTemplateConfigDialogFrame(ChainDialogFrameABC):
    """动态模板配置对话框框架，根据模板配置动态生成页面"""

    def __init__(self, *args, get_template_func=None, template_config_list=None, preview_mode=False):
        self.get_template_func = get_template_func
        self.template_config_list = template_config_list
        # 如果是预览模式，仅展示配置页效果，不添加按钮
        self.preview_mode = preview_mode
        # 模板id值，默认0，主要作用是记录当前使用的模板，方便对比，判断是否需要重新渲染页面
        self.template_id = 0
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
        self.preview_generate_button: QPushButton = ...
        self.preview_generate_frame: ChainDialogFrameABC = ...
        self.list_template_config_executor: ListTemplateConfigExecutor = ...
        super().__init__(*args, 4)

    # ------------------------------ 创建ui界面 start ------------------------------ #

    def setup_content_ui(self):
        self.content_frame_dict = dict()
        self.stacked_widget = QStackedWidget()
        self.frame_layout.addWidget(self.stacked_widget)
        # 如果是预览模式，且配置列表不为空，直接渲染；实际生成过程中调用，渲染页面需要后置
        if self.preview_mode:
            self.setup_stacked_ui()

    def setup_stacked_ui(self):
        self.stacked_widget.setCurrentWidget(self.get_content_frame())

    def get_content_frame(self):
        cache_content_frame_tuple = self.content_frame_dict.get(self.template_id)
        if not cache_content_frame_tuple:
            content_frame = self.do_get_content_frame()
            self.stacked_widget.addWidget(content_frame)
            cache_content_frame_tuple = content_frame, self.config_widget_list
            # 放入缓存
            self.content_frame_dict[self.template_id] = cache_content_frame_tuple
        else:
            # config_widget_list 赋值
            self.config_widget_list = cache_content_frame_tuple[1]
        return cache_content_frame_tuple[0]

    def do_get_content_frame(self):
        if self.template_config_list:
            self.setup_content_scroll_area()
            return self.content_scroll_area
        else:
            self.setup_no_data_frame()
            return self.no_data_frame

    def setup_content_scroll_area(self):
        self.content_scroll_area = ScrollArea()
        # 画布控件
        self.canvas_content_frame = QFrame()
        self.canvas_content_frame_layout = QVBoxLayout(self.canvas_content_frame)
        # 设置画布控件
        self.content_scroll_area.set_canvas_widget(self.canvas_content_frame)

        # 在真实控件之上，增加一个空白label，允许布局拉伸label，以保持真实控件的固定高度，避免变形
        self.canvas_content_frame_layout.addWidget(QLabel())

        if self.template_config_list:
            if not self.preview_mode:
                self.config_widget_list = list()
            for config in self.template_config_list:
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
        self.no_data_label.setText(NO_TEMPLATE_CONFIG_ITEMS_TEXT)
        self.no_data_layout.addWidget(self.no_data_label)

    def setup_other_button(self):
        if self.preview_mode:
            return
        super().setup_other_button()
        self.preview_generate_button = QPushButton()
        self.button_layout.addWidget(self.preview_generate_button, 0, 2, 1, 1)

    def setup_other_label_text(self):
        if self.preview_mode:
            return
        self.previous_frame_button.setText(BACK_TO_SELECT_TEMPLATE_TXT)
        self.next_frame_button.setText(GENERATE_TXT)
        self.preview_generate_button.setText(PREVIEW_GENERATE_TXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        if self.preview_mode:
            return
        super().connect_other_signal()
        self.preview_generate_button.clicked.connect(lambda: self.switch_frame(self.preview_generate_frame))

    # ------------------------------ 信号槽处理 end ------------------------------ #

    # ------------------------------ 后置处理 start ------------------------------ #

    def post_process(self):
        # 清除焦点
        self.dialog_quit_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    # ------------------------------ 后置处理 end ------------------------------ #

    def switch_frame(self, frame):
        # 只要不是回退，都需要收集数据
        if frame is not self.previous_frame:
            self.config_data_dict = dict([(config.config.output_var_name, config.collect_data())
                                          for config in self.config_widget_list])
            # 找出必填的变量名称
            required_var_names = set(map(lambda x: x.output_var_name,
                                         filter(lambda x: x.is_required, self.template_config_list)))
            if required_var_names:
                # 如果还有未填完的值，提示
                filled_var_names = set(map(lambda x: x[0], filter(lambda x: x[1], self.config_data_dict.items())))
                if required_var_names != filled_var_names:
                    pop_fail(NOT_FILL_ALL_REQUIRED_INPUT_TXT, REQUIRED_CHECK_BOX_TITLE, self)
                    return
        super().switch_frame(frame)

    def show(self):
        super().show()
        # 当展示页面时，进行动态渲染页面
        if self.get_template_func:
            template = self.get_template_func()
            if template is not Ellipsis and template.id != self.template_id:
                # 记录当前使用的模板id
                self.template_id = template.id
                self.dynamic_render_content()

    def dynamic_render_content(self):
        # 根据 template_id 获取配置项
        self.list_template_config_executor = ListTemplateConfigExecutor(self.template_id, self.parent_dialog,
                                                                        self.parent_dialog,
                                                                        TEMPLATE_CONFIG_LIST_BOX_TITLE,
                                                                        self.render_content)
        self.list_template_config_executor.start()

    def render_content(self, template_config_list):
        self.template_config_list = template_config_list
        self.setup_stacked_ui()

    def set_preview_generate_frame(self, frame):
        self.preview_generate_frame = frame
