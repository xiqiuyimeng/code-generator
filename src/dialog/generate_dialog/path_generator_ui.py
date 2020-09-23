# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_generator.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

from src.constant.constant import CLEAR_CONFIG_BUTTON, PRE_STEP_BUTTON, GENERATE_BUTTON, \
    CANCEL_BUTTON, MYBATIS_TITLE, IS_LOMBOK, LOMBOK_DESC, MODEL_PACKAGE, \
    MODEL_PACKAGE_DESC, MAPPER_PACKAGE, MAPPER_PACKAGE_DESC, MYBATIS_TAB_TITLE, SPRING_TAB_TITLE, SPRING_TITLE, \
    SPRING_GENERATOR_DESC, SERVICE_PACKAGE, SERVICE_PACKAGE_DESC, SERVICE_IMPL_PACKAGE, SERVICE_IMPL_PACKAGE_DESC, \
    CONTROLLER_PACKAGE, CONTROLLER_PACKAGE_DESC, CHOOSE_DIRECTORY, MYBATIS_PATH_GENERATOR_DESC, OUTPUT_PATH, \
    OUTPUT_PATH_DESC, ASK_TITLE, ASK_PROMPT
from src.func.path_generator_input import OutputPathInputHandler, clear_current_param, ModelPathInputHandler, \
    MapperPathInputHandler, ServicePathInputHandler, ServiceImplPathInputHandler, ControllerPathInputHandler, \
    check_path_mybatis_lineEdit
from src.little_widget.message_box import pop_question
from src.scrollable_widget.scrollable_widget import MyScrollArea


class PathGeneratorUI:
    """路径生成器配置：指定路径，完整的包名，文件将直接生成到指定路径下"""

    def __init__(self, dialog):
        self.parent = dialog
        # 存储指定路径输出的配置
        self.path_output_dict = dict()
        self._translate = self.parent._translate
        self.setup_tab_ui()

    def setup_tab_ui(self):
        """
        构建选择项目生成器的tab标签界面
        """
        self.widget = QtWidgets.QWidget(self.parent.generate_frame)
        self.widget.setObjectName("little_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        # mybatis标签页
        self.setup_mybatis_tab_ui()
        # spring标签页
        self.setup_spring_tab_ui()
        self.tabWidget.addTab(self.mybatis_tab, MYBATIS_TAB_TITLE)
        self.tabWidget.addTab(self.spring_tab, SPRING_TAB_TITLE)
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.tabWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 按钮部分
        self.button_widget = QtWidgets.QWidget(self.widget)
        self.button_widget.setObjectName("button_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.button_widget)
        self.gridLayout.setObjectName("gridLayout")
        self.clear_button = QtWidgets.QPushButton(self.button_widget)
        self.clear_button.setObjectName("clear_button")
        self.gridLayout.addWidget(self.clear_button, 0, 0, 1, 1)
        self.pre_step_button = QtWidgets.QPushButton(self.button_widget)
        self.pre_step_button.setObjectName("pre_step_button")
        self.gridLayout.addWidget(self.pre_step_button, 0, 1, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.button_widget)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout.addWidget(self.button_blank, 0, 2, 1, 1)
        self.generate_button = QtWidgets.QPushButton(self.button_widget)
        self.generate_button.setObjectName("generate_button")
        self.gridLayout.addWidget(self.generate_button, 0, 3, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.button_widget)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 0, 4, 1, 1)
        self.verticalLayout_2.addWidget(self.button_widget)
        # 切换页面事件
        self.tabWidget.currentChanged.connect(self.switch_tab)
        # 按钮点击事件
        self.clear_button.clicked.connect(lambda: clear_current_param(self))
        self.pre_step_button.clicked.connect(self.pre_step)
        self.generate_button.clicked.connect(self.generate)
        self.cancel_button.clicked.connect(self.parent.close)
        # # 选择文件夹按钮
        self.output_button.clicked.connect(lambda: OutputPathInputHandler().choose_dir(self))

        # 输入框文本编辑事件
        self.output_lineEdit.textEdited.connect(lambda: OutputPathInputHandler().input(self))
        self.model_lineEdit.textEdited.connect(lambda: ModelPathInputHandler().input(self))
        self.mapper_lineEdit.textEdited.connect(lambda: MapperPathInputHandler().input(self))
        self.service_lineEdit.textEdited.connect(lambda: ServicePathInputHandler().input(self))
        self.service_impl_lineEdit.textEdited.connect(lambda: ServiceImplPathInputHandler().input(self))
        self.controller_lineEdit.textEdited.connect(lambda: ControllerPathInputHandler().input(self))

        # 填充文字
        self.retranslateUi()

    def setup_mybatis_tab_ui(self):
        """
        构建mybatis生成器配置标签页
        """
        self.mybatis_tab = QtWidgets.QWidget()
        self.mybatis_tab.setObjectName("mybatis_tab")
        self.verticalLayout_scroll_mybatis = QtWidgets.QVBoxLayout(self.mybatis_tab)
        self.verticalLayout_scroll_mybatis.setObjectName("verticalLayout_scroll_mybatis")
        self.mybatis_scrollArea = MyScrollArea(self.mybatis_tab)
        self.mybatis_scrollArea.setWidgetResizable(True)
        self.mybatis_scrollArea.setObjectName("mybatis_scrollArea")
        self.mybatis_scroll_widget = QtWidgets.QWidget()
        self.mybatis_scroll_widget.setObjectName("mybatis_scroll_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mybatis_scroll_widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mybatis_title = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.mybatis_title.setObjectName("mybatis_title")
        self.verticalLayout_3.addWidget(self.mybatis_title)
        self.mybatis_desc = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.mybatis_desc.setObjectName("mybatis_desc")
        self.verticalLayout_3.addWidget(self.mybatis_desc)
        self.mybatis_blank = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.mybatis_blank.setObjectName("mybatis_blank")
        self.verticalLayout_3.addWidget(self.mybatis_blank)
        # 表格布局
        self.mybatis_gridLayout = QtWidgets.QGridLayout()
        self.mybatis_gridLayout.setObjectName("mybatis_gridLayout")
        # lombok
        self.lombok = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.lombok.setObjectName("lombok")
        self.mybatis_gridLayout.addWidget(self.lombok, 0, 0, 1, 1)
        self.lombok_blank = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.lombok_blank.setObjectName("lombok_blank")
        self.mybatis_gridLayout.addWidget(self.lombok_blank, 0, 1, 1, 1)
        self.lombok_splitter = QtWidgets.QSplitter(self.mybatis_scroll_widget)
        self.lombok_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.lombok_splitter.setObjectName("lombok_splitter")
        self.lombok_splitter.setHandleWidth(0)
        self.mybatis_gridLayout.addWidget(self.lombok_splitter, 0, 2, 1, 1)
        self.lombok_comboBox_blank = QtWidgets.QLabel(self.lombok_splitter)
        self.lombok_comboBox_blank.setObjectName("lombok_comboBox_blank")
        self.lombok_comboBox = QtWidgets.QComboBox(self.lombok_splitter)
        self.lombok_comboBox.setMaximumWidth(100)
        self.lombok_comboBox.setObjectName("lombok_comboBox")
        self.lombok_comboBox.addItem("")
        self.lombok_comboBox.addItem("")
        self.lombok_desc = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.lombok_desc.setObjectName("lombok_desc")
        # label跨越三列
        self.mybatis_gridLayout.addWidget(self.lombok_desc, 1, 0, 1, 3)
        # output_path
        self.output = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.output.setObjectName("output")
        self.mybatis_gridLayout.addWidget(self.output, 2, 0, 1, 1)
        self.output_button = QtWidgets.QPushButton(self.mybatis_scroll_widget)
        self.output_button.setObjectName("output_button")
        self.mybatis_gridLayout.addWidget(self.output_button, 2, 1, 1, 1)
        self.output_lineEdit = QtWidgets.QLineEdit(self.mybatis_scroll_widget)
        self.output_lineEdit.setObjectName("output_lineEdit")
        self.mybatis_gridLayout.addWidget(self.output_lineEdit, 2, 2, 1, 1)
        self.output_desc = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.output_desc.setObjectName("output_desc")
        # label跨越三列
        self.mybatis_gridLayout.addWidget(self.output_desc, 3, 0, 1, 3)
        # model
        self.model = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.model.setObjectName("model")
        self.mybatis_gridLayout.addWidget(self.model, 4, 0, 1, 1)
        # 初始输入框不可用
        self.model_lineEdit = QtWidgets.QLineEdit(self.mybatis_scroll_widget)
        self.model_lineEdit.setObjectName("model_lineEdit")
        self.model_lineEdit.setDisabled(True)
        self.mybatis_gridLayout.addWidget(self.model_lineEdit, 4, 2, 1, 1)
        self.model_desc = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.model_desc.setObjectName("model_desc")
        # label跨越三列
        self.mybatis_gridLayout.addWidget(self.model_desc, 5, 0, 1, 3)
        # mapper
        self.mapper = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.mapper.setObjectName("mapper")
        self.mybatis_gridLayout.addWidget(self.mapper, 6, 0, 1, 1)
        # 初始输入框不可用
        self.mapper_lineEdit = QtWidgets.QLineEdit(self.mybatis_scroll_widget)
        self.mapper_lineEdit.setObjectName("mapper_lineEdit")
        self.mapper_lineEdit.setDisabled(True)
        self.mybatis_gridLayout.addWidget(self.mapper_lineEdit, 6, 2, 1, 1)
        self.mapper_desc = QtWidgets.QLabel(self.mybatis_scroll_widget)
        self.mapper_desc.setObjectName("mapper_desc")
        # label跨越三列
        self.mybatis_gridLayout.addWidget(self.mapper_desc, 7, 0, 1, 3)

        self.verticalLayout_3.addLayout(self.mybatis_gridLayout)
        self.mybatis_scroll_widget.setLayout(self.verticalLayout_3)
        self.mybatis_scrollArea.setWidget(self.mybatis_scroll_widget)
        self.verticalLayout_scroll_mybatis.addWidget(self.mybatis_scrollArea)
        self.mybatis_tab.setLayout(self.verticalLayout_scroll_mybatis)

    def setup_spring_tab_ui(self):
        """
        构建spring生成器配置标签页
        """
        self.spring_tab = QtWidgets.QWidget()
        self.spring_tab.setObjectName("spring_tab")
        self.verticalLayout_scroll_spring = QtWidgets.QVBoxLayout(self.spring_tab)
        self.verticalLayout_scroll_spring.setObjectName("verticalLayout_scroll_spring")
        self.spring_scrollArea = MyScrollArea(self.spring_tab)
        self.spring_scrollArea.setWidgetResizable(True)
        self.spring_scrollArea.setObjectName("spring_scrollArea")
        self.spring_scroll_widget = QtWidgets.QWidget()
        self.spring_scroll_widget.setObjectName("spring_scroll_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.spring_scroll_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.spring_title = QtWidgets.QLabel(self.spring_scroll_widget)
        self.spring_title.setObjectName("spring_title")
        self.verticalLayout_4.addWidget(self.spring_title)
        self.spring_desc = QtWidgets.QLabel(self.spring_scroll_widget)
        self.spring_desc.setObjectName("spring_desc")
        self.verticalLayout_4.addWidget(self.spring_desc)
        self.spring_blank = QtWidgets.QLabel(self.spring_scroll_widget)
        self.spring_blank.setObjectName("spring_blank")
        self.verticalLayout_4.addWidget(self.spring_blank)
        # 表格布局
        self.spring_gridLayout = QtWidgets.QGridLayout()
        self.spring_gridLayout.setObjectName("spring_gridLayout")
        # service
        self.service = QtWidgets.QLabel(self.spring_scroll_widget)
        self.service.setObjectName("service")
        self.spring_gridLayout.addWidget(self.service, 0, 0, 1, 1)
        self.service_blank = QtWidgets.QLabel(self.spring_scroll_widget)
        self.service_blank.setObjectName("service_blank")
        self.service_blank.setText("\t")
        self.spring_gridLayout.addWidget(self.service_blank, 0, 1, 1, 1)
        self.service_lineEdit = QtWidgets.QLineEdit(self.spring_scroll_widget)
        self.service_lineEdit.setObjectName("service_lineEdit")
        # 初始输入框不可用
        self.service_lineEdit.setDisabled(True)
        self.spring_gridLayout.addWidget(self.service_lineEdit, 0, 2, 1, 1)
        self.service_desc = QtWidgets.QLabel(self.spring_scroll_widget)
        self.service_desc.setObjectName("service_desc")
        # label跨越三列
        self.spring_gridLayout.addWidget(self.service_desc, 1, 0, 1, 3)
        # service_impl
        self.service_impl = QtWidgets.QLabel(self.spring_scroll_widget)
        self.service_impl.setObjectName("service_impl")
        self.spring_gridLayout.addWidget(self.service_impl, 2, 0, 1, 1)
        # 初始不可用
        self.service_impl_lineEdit = QtWidgets.QLineEdit(self.spring_scroll_widget)
        self.service_impl_lineEdit.setObjectName("service_impl_lineEdit")
        self.service_impl_lineEdit.setDisabled(True)
        self.spring_gridLayout.addWidget(self.service_impl_lineEdit, 2, 2, 1, 1)
        self.service_impl_desc = QtWidgets.QLabel(self.spring_scroll_widget)
        self.service_impl_desc.setObjectName("service_impl_desc")
        # label跨越三列
        self.spring_gridLayout.addWidget(self.service_impl_desc, 3, 0, 1, 3)
        # controller
        self.controller = QtWidgets.QLabel(self.spring_scroll_widget)
        self.controller.setObjectName("controller")
        self.spring_gridLayout.addWidget(self.controller, 4, 0, 1, 1)
        # 初始输入框不可用
        self.controller_lineEdit = QtWidgets.QLineEdit(self.spring_scroll_widget)
        self.controller_lineEdit.setObjectName("controller_lineEdit")
        self.controller_lineEdit.setDisabled(True)
        self.spring_gridLayout.addWidget(self.controller_lineEdit, 4, 2, 1, 1)
        self.controller_desc = QtWidgets.QLabel(self.spring_scroll_widget)
        self.controller_desc.setObjectName("controller_desc")
        # label跨越三列
        self.spring_gridLayout.addWidget(self.controller_desc, 5, 0, 1, 3)

        self.verticalLayout_4.addLayout(self.spring_gridLayout)
        self.spring_scrollArea.setWidget(self.spring_scroll_widget)
        self.verticalLayout_scroll_spring.addWidget(self.spring_scrollArea)
        self.spring_tab.setLayout(self.verticalLayout_scroll_spring)

    def retranslateUi(self):
        """
        对界面上的文字样式控制
        """
        self.mybatis_title.setText(MYBATIS_TITLE)
        self.mybatis_desc.setText(MYBATIS_PATH_GENERATOR_DESC)
        self.lombok.setText(IS_LOMBOK)
        self.lombok_comboBox.setItemText(0, "True")
        self.lombok_comboBox.setItemText(1, "False")
        self.lombok_desc.setText(LOMBOK_DESC)
        self.output.setText(OUTPUT_PATH)
        self.output_desc.setText(OUTPUT_PATH_DESC)
        self.model.setText(MODEL_PACKAGE)
        self.model_desc.setText(MODEL_PACKAGE_DESC)
        self.mapper.setText(MAPPER_PACKAGE)
        self.mapper_desc.setText(MAPPER_PACKAGE_DESC)
        self.spring_title.setText(SPRING_TITLE)
        self.spring_desc.setText(SPRING_GENERATOR_DESC)
        self.service.setText(SERVICE_PACKAGE)
        self.service_desc.setText(SERVICE_PACKAGE_DESC)
        self.service_impl.setText(SERVICE_IMPL_PACKAGE)
        self.service_impl_desc.setText(SERVICE_IMPL_PACKAGE_DESC)
        self.controller.setText(CONTROLLER_PACKAGE)
        self.controller_desc.setText(CONTROLLER_PACKAGE_DESC)
        # 按钮
        self.clear_button.setText(CLEAR_CONFIG_BUTTON)
        self.pre_step_button.setText(PRE_STEP_BUTTON)
        # 生成按钮
        self.generate_button.setText(GENERATE_BUTTON)
        self.generate_button.setDisabled(True)
        self.cancel_button.setText(CANCEL_BUTTON)
        # 选择文件夹按钮
        self.output_button.setText(CHOOSE_DIRECTORY)

    def switch_tab(self, idx):
        """切换页面事件，如果切换到spring页，检查mybatis页是否已经有值，若没有值，弹窗询问是否返回mybatis页"""
        if idx == 1 and not check_path_mybatis_lineEdit(self) and pop_question(ASK_TITLE, ASK_PROMPT):
            self.tabWidget.setCurrentIndex(0)

    def pre_step(self):
        # 隐藏选择生成器界面
        self.widget.hide()
        # 展示树控件
        self.parent.tree_widget.show()

    def generate(self):
        # lombok选值
        self.path_output_dict['lombok'] = eval(self.lombok_comboBox.currentText())
        self.parent.generate(self.path_output_dict)
