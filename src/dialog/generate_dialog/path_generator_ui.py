# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_generator.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

from src.constant.constant import CLEAR_CONFIG_BUTTON, PRE_STEP_BUTTON, GENERATE_BUTTON, \
    CANCEL_BUTTON, MYBATIS_TITLE, IS_LOMBOK, LOMBOK_DESC, \
    MODEL_PACKAGE, \
    MODEL_PACKAGE_DESC, MAPPER_PACKAGE, MAPPER_PACKAGE_DESC, MYBATIS_TAB_TITLE, SPRING_TAB_TITLE, SPRING_TITLE, \
    SPRING_GENERATOR_DESC, \
    SERVICE_PACKAGE, SERVICE_PACKAGE_DESC, SERVICE_IMPL_PACKAGE, SERVICE_IMPL_PACKAGE_DESC, \
    CONTROLLER_PACKAGE, CONTROLLER_PACKAGE_DESC, CHOOSE_DIRECTORY, MYBATIS_PATH_GENERATOR_DESC, OUTPUT_PATH, \
    OUTPUT_PATH_DESC
from src.func.path_generator_input import OutputPathInputHandler, clear_current_param, ModelPathInputHandler, \
    MapperPathInputHandler, ServicePathInputHandler, ServiceImplPathInputHandler, ControllerPathInputHandler
from src.sys.settings.font import set_font


class PathGeneratorUI:
    """路径生成器配置：指定路径，完整的包名，文件将直接生成到指定路径下"""

    def __init__(self, dialog):
        self.parent = dialog
        # 存储指定路径输出的配置
        self.path_output_dict = dict()
        self._translate = self.parent._translate
        self.button_width = self.parent.screen_rect.width() * 0.15
        self.line_edit_width = self.parent.screen_rect.width() * 0.55
        self.setup_tab_ui()

    def setup_tab_ui(self):
        """
        构建选择项目生成器的tab标签界面
        :param self: 弹窗确认生成器配置页的主窗口对象
        """
        self.widget = QtWidgets.QWidget(self.parent.frame)
        self.widget.setObjectName("little_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")
        # mybatis标签页
        self.setup_mybatis_tab_ui()
        # spring标签页
        self.setup_spring_tab_ui()
        self.tabWidget.addTab(self.mybatis_tab, "")
        self.tabWidget.addTab(self.spring_tab, "")
        self.verticalLayout_2.addWidget(self.tabWidget)

        self.tabWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        # 按钮部分
        self.splitter = QtWidgets.QSplitter(self.widget)
        # 分隔线隐藏
        self.splitter.setHandleWidth(0)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.splitter)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.buttonBox_2 = QtWidgets.QDialogButtonBox(self.splitter)
        self.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName("buttonBox_2")
        self.verticalLayout_2.addWidget(self.splitter)

        # 按钮点击事件
        self.buttonBox.accepted.connect(lambda: clear_current_param(self))
        self.buttonBox.rejected.connect(lambda: self.pre_step())
        self.buttonBox_2.accepted.connect(lambda: self.parent.generate(self.path_output_dict))
        self.buttonBox_2.rejected.connect(self.parent.close)
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
        :param self: 弹窗确认生成器配置页的主窗口对象
        :return:
        """
        self.mybatis_tab = QtWidgets.QWidget()
        self.mybatis_tab.setObjectName("mybatis_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.mybatis_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mybatis_title = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_title.setObjectName("mybatis_title")
        self.verticalLayout_3.addWidget(self.mybatis_title)
        self.mybatis_first_blank = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_first_blank.setText("")
        self.mybatis_first_blank.setObjectName("mybatis_first_blank")
        self.verticalLayout_3.addWidget(self.mybatis_first_blank)
        self.mybatis_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_desc.setObjectName("mybatis_desc")
        self.verticalLayout_3.addWidget(self.mybatis_desc)
        self.mybatis_second_blank = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_second_blank.setText("")
        self.mybatis_second_blank.setObjectName("mybatis_second_blank")
        self.verticalLayout_3.addWidget(self.mybatis_second_blank)
        # lombok
        self.splitter_lombok = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_lombok.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_lombok.setObjectName("splitter_lombok")
        self.splitter_lombok.setHandleWidth(0)
        self.lombok = QtWidgets.QLabel(self.splitter_lombok)
        self.lombok.setObjectName("lombok")
        self.lombok_comboBox = QtWidgets.QComboBox(self.splitter_lombok)
        self.lombok_comboBox.setObjectName("lombok_comboBox")
        # 计算lombok按钮宽度
        self.lombok_comboBox.setFixedWidth(self.button_width)
        self.lombok_comboBox.addItem("")
        self.lombok_comboBox.addItem("")
        self.verticalLayout_3.addWidget(self.splitter_lombok)
        self.lombok_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.lombok_desc.setObjectName("lombok_desc")
        self.verticalLayout_3.addWidget(self.lombok_desc)
        # output_path
        self.splitter_output = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_output.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_output.setObjectName("splitter_output")
        self.splitter_output.setHandleWidth(0)
        self.output = QtWidgets.QLabel(self.splitter_output)
        self.output.setObjectName("output")
        self.output_button = QtWidgets.QPushButton(self.splitter_output)
        self.output_button.setObjectName("output_button")
        # 按钮宽度
        self.output_button.setFixedWidth(self.button_width)
        self.output_lineEdit = QtWidgets.QLineEdit(self.splitter_output)
        self.output_lineEdit.setObjectName("output_lineEdit")
        # 计算输入框宽度
        self.output_lineEdit.setFixedWidth(self.line_edit_width)
        self.verticalLayout_3.addWidget(self.splitter_output)
        self.output_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.output_desc.setObjectName("output_desc")
        self.verticalLayout_3.addWidget(self.output_desc)
        # mybatis_third_blank
        self.mybatis_third_blank = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_third_blank.setObjectName("mybatis_third_blank")
        self.mybatis_third_blank.setText("")
        self.verticalLayout_3.addWidget(self.mybatis_third_blank)
        # model
        self.splitter_model = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_model.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_model.setObjectName("splitter_model")
        self.splitter_model.setHandleWidth(0)
        self.model = QtWidgets.QLabel(self.splitter_model)
        self.model.setObjectName("model")
        self.model_lineEdit = QtWidgets.QLineEdit(self.splitter_model)
        self.model_lineEdit.setObjectName("model_lineEdit")
        self.model_lineEdit.setFixedWidth(self.line_edit_width)
        # 初始不可用
        self.model_lineEdit.setDisabled(True)
        self.verticalLayout_3.addWidget(self.splitter_model)
        self.model_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.model_desc.setObjectName("model_desc")
        self.verticalLayout_3.addWidget(self.model_desc)
        # mapper
        self.splitter_mapper = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_mapper.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_mapper.setObjectName("splitter_mapper")
        self.splitter_mapper.setHandleWidth(0)
        self.mapper = QtWidgets.QLabel(self.splitter_mapper)
        self.mapper.setObjectName("mapper")
        self.mapper_lineEdit = QtWidgets.QLineEdit(self.splitter_mapper)
        self.mapper_lineEdit.setObjectName("mapper_lineEdit")
        self.mapper_lineEdit.setFixedWidth(self.line_edit_width)
        # 初始不可用
        self.mapper_lineEdit.setDisabled(True)
        self.verticalLayout_3.addWidget(self.splitter_mapper)
        self.mapper_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.mapper_desc.setObjectName("mapper_desc")
        self.verticalLayout_3.addWidget(self.mapper_desc)
        # mybatis_fourth_blank
        self.mybatis_fourth_blank = QtWidgets.QLabel(self.mybatis_tab)
        self.mybatis_fourth_blank.setObjectName("mybatis_fourth_blank")
        self.mybatis_fourth_blank.setText("")
        self.verticalLayout_3.addWidget(self.mybatis_fourth_blank)

    def setup_spring_tab_ui(self):
        """
        构建spring生成器配置标签页
        :param self: 弹窗确认生成器配置页的主窗口对象
        :return:
        """
        self.spring_tab = QtWidgets.QWidget()
        self.spring_tab.setObjectName("spring_tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.spring_tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.spring_title = QtWidgets.QLabel(self.spring_tab)
        self.spring_title.setObjectName("spring_title")
        self.verticalLayout_4.addWidget(self.spring_title)
        self.spring_first_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_first_blank.setText("")
        self.spring_first_blank.setObjectName("spring_first_blank")
        self.verticalLayout_4.addWidget(self.spring_first_blank)
        self.spring_desc = QtWidgets.QLabel(self.spring_tab)
        self.spring_desc.setObjectName("spring_desc")
        self.verticalLayout_4.addWidget(self.spring_desc)
        self.spring_second_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_second_blank.setText("")
        self.spring_second_blank.setObjectName("spring_second_blank")
        self.verticalLayout_4.addWidget(self.spring_second_blank)
        self.spring_third_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_third_blank.setText("")
        self.spring_third_blank.setObjectName("spring_third_blank")
        self.verticalLayout_4.addWidget(self.spring_third_blank)
        self.spring_fourth_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_fourth_blank.setText("")
        self.spring_fourth_blank.setObjectName("spring_fourth_blank")
        self.verticalLayout_4.addWidget(self.spring_fourth_blank)
        self.spring_fifth_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_fifth_blank.setText("")
        self.spring_fifth_blank.setObjectName("spring_fifth_blank")
        self.verticalLayout_4.addWidget(self.spring_fifth_blank)
        # service
        self.splitter_service = QtWidgets.QSplitter(self.spring_tab)
        self.splitter_service.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_service.setObjectName("splitter_service")
        self.splitter_service.setHandleWidth(0)
        self.service = QtWidgets.QLabel(self.splitter_service)
        self.service.setObjectName("service")
        self.service_lineEdit = QtWidgets.QLineEdit(self.splitter_service)
        self.service_lineEdit.setObjectName("service_lineEdit")
        self.service_lineEdit.setFixedWidth(self.line_edit_width)
        # 初始不可用
        self.service_lineEdit.setDisabled(True)
        self.verticalLayout_4.addWidget(self.splitter_service)
        self.service_desc = QtWidgets.QLabel(self.spring_tab)
        self.service_desc.setObjectName("service_desc")
        self.verticalLayout_4.addWidget(self.service_desc)
        # service_impl
        self.splitter_service_impl = QtWidgets.QSplitter(self.spring_tab)
        self.splitter_service_impl.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_service_impl.setObjectName("splitter_service_impl")
        self.splitter_service_impl.setHandleWidth(0)
        self.service_impl = QtWidgets.QLabel(self.splitter_service_impl)
        self.service_impl.setObjectName("service_impl")
        self.service_impl_lineEdit = QtWidgets.QLineEdit(self.splitter_service_impl)
        self.service_impl_lineEdit.setObjectName("service_impl_lineEdit")
        self.service_impl_lineEdit.setFixedWidth(self.line_edit_width)
        # 初始不可用
        self.service_impl_lineEdit.setDisabled(True)
        self.verticalLayout_4.addWidget(self.splitter_service_impl)
        self.service_impl_desc = QtWidgets.QLabel(self.spring_tab)
        self.service_impl_desc.setObjectName("service_impl_desc")
        self.verticalLayout_4.addWidget(self.service_impl_desc)
        # controller
        self.splitter_controller = QtWidgets.QSplitter(self.spring_tab)
        self.splitter_controller.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_controller.setObjectName("splitter_controller")
        self.splitter_controller.setHandleWidth(0)
        self.controller = QtWidgets.QLabel(self.splitter_controller)
        self.controller.setObjectName("controller")
        self.controller_lineEdit = QtWidgets.QLineEdit(self.splitter_controller)
        self.controller_lineEdit.setObjectName("controller_lineEdit")
        self.controller_lineEdit.setFixedWidth(self.line_edit_width)
        # 初始不可用
        self.controller_lineEdit.setDisabled(True)
        self.verticalLayout_4.addWidget(self.splitter_controller)
        self.controller_desc = QtWidgets.QLabel(self.spring_tab)
        self.controller_desc.setObjectName("controller_desc")
        self.verticalLayout_4.addWidget(self.controller_desc)

        self.spring_sixth_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_sixth_blank.setText("")
        self.spring_sixth_blank.setObjectName("spring_sixth_blank")
        self.verticalLayout_4.addWidget(self.spring_sixth_blank)
        self.spring_seventh_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_seventh_blank.setText("")
        self.spring_seventh_blank.setObjectName("spring_seventh_blank")
        self.verticalLayout_4.addWidget(self.spring_seventh_blank)
        self.spring_eighth_blank = QtWidgets.QLabel(self.spring_tab)
        self.spring_eighth_blank.setText("")
        self.spring_eighth_blank.setObjectName("spring_eighth_blank")
        self.verticalLayout_4.addWidget(self.spring_eighth_blank)

    def retranslateUi(self):
        """
        对界面上的文字样式控制
        :param self: 弹窗确认生成器配置页的主窗口对象
        """
        self.mybatis_title.setText(MYBATIS_TITLE)
        self.mybatis_desc.setWordWrap(True)
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mybatis_tab),
                                          self._translate("Dialog", MYBATIS_TAB_TITLE))
        self.spring_title.setText(SPRING_TITLE)
        self.spring_desc.setText(SPRING_GENERATOR_DESC)
        self.service.setText(SERVICE_PACKAGE)
        self.service_desc.setText(SERVICE_PACKAGE_DESC)
        self.service_impl.setText(SERVICE_IMPL_PACKAGE)
        self.service_impl_desc.setText(SERVICE_IMPL_PACKAGE_DESC)
        self.controller.setText(CONTROLLER_PACKAGE)
        self.controller_desc.setText(CONTROLLER_PACKAGE_DESC)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.spring_tab),
                                          self._translate("Dialog", SPRING_TAB_TITLE))
        # 按钮
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(CLEAR_CONFIG_BUTTON)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setFont(set_font())
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(PRE_STEP_BUTTON)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setFont(set_font())
        # 生成按钮
        self.generate_button = self.buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok)
        self.generate_button.setText(GENERATE_BUTTON)
        self.generate_button.setFont(set_font())
        self.generate_button.setDisabled(True)
        self.buttonBox_2.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)
        self.buttonBox_2.button(QtWidgets.QDialogButtonBox.Cancel).setFont(set_font())
        # 选择文件夹按钮
        self.output_button.setText(CHOOSE_DIRECTORY)

    def pre_step(self):
        # 隐藏选择生成器界面
        self.widget.hide()
        # 展示树控件
        self.parent.tree_widget.show()
