# -*- coding: utf-8 -*-
"""
点击生成按钮，弹窗的第二步页面，负责配置生成器的输出配置
"""
from PyQt5 import QtWidgets, QtCore

from src.constant.constant import CLEAR_CONFIG_BUTTON, PRE_STEP_BUTTON, GENERATE_BUTTON, \
    CANCEL_BUTTON, MYBATIS_TITLE, IS_LOMBOK, MYBATIS_GENERATOR_DESC, LOMBOK_DESC, \
    JAVA_PATH, JAVA_PATH_DESC, JAVA_SRC_PATH, JAVA_SRC_PATH_DESC, MODEL_PACKAGE, \
    MODEL_PACKAGE_DESC, MAPPER_PACKAGE, MAPPER_PACKAGE_DESC, XML_PATH, XML_PATH_DESC, \
    MYBATIS_TAB_TITLE, SPRING_TAB_TITLE, SPRING_TITLE, SPRING_GENERATOR_DESC, \
    SERVICE_PACKAGE, SERVICE_PACKAGE_DESC, SERVICE_IMPL_PACKAGE, SERVICE_IMPL_PACKAGE_DESC, \
    CONTROLLER_PACKAGE, CONTROLLER_PACKAGE_DESC, CHOOSE_DIRECTORY, WARNING_TITLE, PARAM_WARNING_MSG
from src.func.project_generator_input import JavaInputHandler, JavaSrcInputHandler, ModelInputHandler, \
    MapperInputHandler, XmlInputHandler, ServiceInputHandler, ServiceImplInputHandler, ControllerInputHandler, \
    clear_current_param, check_params
from src.little_widget.message_box import pop_warning
from src.sys.settings.font import set_label_font, set_title_font, set_font

_author_ = 'luwt'
_date_ = '2020/7/18 11:47'


class ProjectGeneratorUI:
    """项目生成器配置：完整的项目路径，包名等等，文件将直接生成到项目中"""

    def __init__(self, dialog):
        self.parent = dialog
        # 存储指定项目的输出配置
        self.project_output_dict = dict()
        self._translate = self.parent._translate
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
        self.tabWidget.setFont(set_font())

        self.tabWidget.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.tabWidget.setStyleSheet("QTabWidget:pane{border-style:solid;border-radius:25px;background-color:LightYellow;}")
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
        self.buttonBox.rejected.connect(self.pre_step)
        self.buttonBox_2.accepted.connect(lambda: self.parent.generate(self, self.project_output_dict))
        self.buttonBox_2.rejected.connect(self.parent.close)
        # 选择文件夹按钮
        self.java_button.clicked.connect(lambda: JavaInputHandler().choose_dir(self))
        self.java_src_button.clicked.connect(lambda: JavaSrcInputHandler().choose_dir(self))
        self.model_button.clicked.connect(lambda: ModelInputHandler().choose_dir(self))
        self.mapper_button.clicked.connect(lambda: MapperInputHandler().choose_dir(self))
        self.xml_button.clicked.connect(lambda: XmlInputHandler().choose_dir(self))
        self.service_button.clicked.connect(lambda: ServiceInputHandler().choose_dir(self))
        self.service_impl_button.clicked.connect(lambda: ServiceImplInputHandler().choose_dir(self))
        self.controller_button.clicked.connect(lambda: ControllerInputHandler().choose_dir(self))
    
        # 输入框文本编辑事件
        self.java_lineEdit.textEdited.connect(lambda: JavaInputHandler().input(self))
        self.java_src_lineEdit.textEdited.connect(lambda: JavaSrcInputHandler().input(self))
        self.model_lineEdit.textEdited.connect(lambda: ModelInputHandler().input(self))
        self.mapper_lineEdit.textEdited.connect(lambda: MapperInputHandler().input(self))
        self.xml_lineEdit.textEdited.connect(lambda: XmlInputHandler().input(self))
        self.service_lineEdit.textEdited.connect(lambda: ServiceInputHandler().input(self))
        self.service_impl_lineEdit.textEdited.connect(lambda: ServiceImplInputHandler().input(self))
        self.controller_lineEdit.textEdited.connect(lambda: ControllerInputHandler().input(self))
    
        # 填充文字
        self.retranslateUi()

    def setup_mybatis_tab_ui(self):
        """
        构建mybatis生成器配置标签页
        :param self: 弹窗确认生成器配置页的主窗口对象
        :return:
        """
        self.mybatis_tab = QtWidgets.QWidget()
        self.mybatis_tab.setFont(set_font())
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
        self.lombok_comboBox.setFixedWidth(100)
        self.lombok_comboBox.addItem("")
        self.lombok_comboBox.addItem("")
        self.verticalLayout_3.addWidget(self.splitter_lombok)
        self.lombok_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.lombok_desc.setObjectName("lombok_desc")
        self.verticalLayout_3.addWidget(self.lombok_desc)
        # java_path
        self.splitter_java = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_java.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_java.setObjectName("splitter_java")
        self.splitter_java.setHandleWidth(0)
        self.java = QtWidgets.QLabel(self.splitter_java)
        self.java.setObjectName("java")
        self.java_button = QtWidgets.QPushButton(self.splitter_java)
        self.java_button.setObjectName("java_button")
        self.java_button.setFixedWidth(120)
        self.java_lineEdit = QtWidgets.QLineEdit(self.splitter_java)
        self.java_lineEdit.setObjectName("java_lineEdit")
        self.java_lineEdit.setFixedWidth(500)
        self.verticalLayout_3.addWidget(self.splitter_java)
        self.java_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.java_desc.setObjectName("java_desc")
        self.verticalLayout_3.addWidget(self.java_desc)
        # java_src
        self.splitter_java_src = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_java_src.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_java_src.setObjectName("splitter_java_src")
        self.splitter_java_src.setHandleWidth(0)
        self.java_src = QtWidgets.QLabel(self.splitter_java_src)
        self.java_src.setObjectName("java_src")
        self.java_src_button = QtWidgets.QPushButton(self.splitter_java_src)
        self.java_src_button.setObjectName("java_src_button")
        self.java_src_button.setFixedWidth(120)
        # 初始不可用
        self.java_src_button.setDisabled(True)
        self.java_src_lineEdit = QtWidgets.QLineEdit(self.splitter_java_src)
        self.java_src_lineEdit.setObjectName("java_src_lineEdit")
        self.java_src_lineEdit.setFixedWidth(500)
        # 初始不可用
        self.java_src_lineEdit.setDisabled(True)
        self.verticalLayout_3.addWidget(self.splitter_java_src)
        self.java_src_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.java_src_desc.setObjectName("java_src_desc")
        self.verticalLayout_3.addWidget(self.java_src_desc)
        # model
        self.splitter_model = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_model.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_model.setObjectName("splitter_model")
        self.splitter_model.setHandleWidth(0)
        self.model = QtWidgets.QLabel(self.splitter_model)
        self.model.setObjectName("model")
        self.model_button = QtWidgets.QPushButton(self.splitter_model)
        self.model_button.setObjectName("model_button")
        self.model_button.setFixedWidth(120)
        # 初始不可用
        self.model_button.setDisabled(True)
        self.model_lineEdit = QtWidgets.QLineEdit(self.splitter_model)
        self.model_lineEdit.setObjectName("model_lineEdit")
        self.model_lineEdit.setFixedWidth(500)
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
        self.mapper_button = QtWidgets.QPushButton(self.splitter_mapper)
        self.mapper_button.setObjectName("mapper_button")
        self.mapper_button.setFixedWidth(120)
        # 初始不可用
        self.mapper_button.setDisabled(True)
        self.mapper_lineEdit = QtWidgets.QLineEdit(self.splitter_mapper)
        self.mapper_lineEdit.setObjectName("mapper_lineEdit")
        self.mapper_lineEdit.setFixedWidth(500)
        # 初始不可用
        self.mapper_lineEdit.setDisabled(True)
        self.verticalLayout_3.addWidget(self.splitter_mapper)
        self.mapper_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.mapper_desc.setObjectName("mapper_desc")
        self.verticalLayout_3.addWidget(self.mapper_desc)
        # xml
        self.splitter_xml = QtWidgets.QSplitter(self.mybatis_tab)
        self.splitter_xml.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_xml.setObjectName("splitter_xml")
        self.splitter_xml.setHandleWidth(0)
        self.xml = QtWidgets.QLabel(self.splitter_xml)
        self.xml.setObjectName("xml")
        self.xml_button = QtWidgets.QPushButton(self.splitter_xml)
        self.xml_button.setObjectName("xml_button")
        self.xml_button.setFixedWidth(120)
        # 初始不可用
        self.xml_button.setDisabled(True)
        self.xml_lineEdit = QtWidgets.QLineEdit(self.splitter_xml)
        self.xml_lineEdit.setObjectName("xml_lineEdit")
        self.xml_lineEdit.setFixedWidth(500)
        # 初始不可用
        self.xml_lineEdit.setDisabled(True)
        self.verticalLayout_3.addWidget(self.splitter_xml)
        self.xml_desc = QtWidgets.QLabel(self.mybatis_tab)
        self.xml_desc.setObjectName("xml_desc")
        self.verticalLayout_3.addWidget(self.xml_desc)

    def setup_spring_tab_ui(self):
        """
        构建spring生成器配置标签页
        :param self: 弹窗确认生成器配置页的主窗口对象
        :return:
        """
        self.spring_tab = QtWidgets.QWidget()
        self.spring_tab.setFont(set_font())
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
        self.service_button = QtWidgets.QPushButton(self.splitter_service)
        self.service_button.setObjectName("service_button")
        self.service_button.setFixedWidth(120)
        # 初始不可用
        self.service_button.setDisabled(True)
        self.service_lineEdit = QtWidgets.QLineEdit(self.splitter_service)
        self.service_lineEdit.setObjectName("service_lineEdit")
        self.service_lineEdit.setFixedWidth(500)
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
        self.service_impl_button = QtWidgets.QPushButton(self.splitter_service_impl)
        self.service_impl_button.setObjectName("service_impl_button")
        self.service_impl_button.setFixedWidth(120)
        # 初始不可用
        self.service_impl_button.setDisabled(True)
        self.service_impl_lineEdit = QtWidgets.QLineEdit(self.splitter_service_impl)
        self.service_impl_lineEdit.setObjectName("service_impl_lineEdit")
        self.service_impl_lineEdit.setFixedWidth(500)
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
        self.controller_button = QtWidgets.QPushButton(self.splitter_controller)
        self.controller_button.setObjectName("controller_button")
        self.controller_button.setFixedWidth(120)
        # 初始不可用
        self.controller_button.setDisabled(True)
        self.controller_lineEdit = QtWidgets.QLineEdit(self.splitter_controller)
        self.controller_lineEdit.setObjectName("controller_lineEdit")
        self.controller_lineEdit.setFixedWidth(500)
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
        self.mybatis_title.setText(
            self._translate("Dialog", set_title_font(MYBATIS_TITLE)))
        self.mybatis_desc.setText(self._translate("Dialog", MYBATIS_GENERATOR_DESC))
        self.lombok.setText(self._translate("Dialog", set_label_font(IS_LOMBOK)))
        self.lombok_comboBox.setItemText(0, self._translate("Dialog", "True"))
        self.lombok_comboBox.setItemText(1, self._translate("Dialog", "False"))
        self.lombok_desc.setText(self._translate("Dialog", LOMBOK_DESC))
        self.java.setText(self._translate("Dialog", set_label_font(JAVA_PATH)))
        self.java_desc.setText(self._translate("Dialog", JAVA_PATH_DESC))
        self.java_src.setText(self._translate("Dialog", set_label_font(JAVA_SRC_PATH)))
        self.java_src_desc.setText(self._translate("Dialog", JAVA_SRC_PATH_DESC))
        self.model.setText(self._translate("Dialog", set_label_font(MODEL_PACKAGE)))
        self.model_desc.setText(self._translate("Dialog", MODEL_PACKAGE_DESC))
        self.mapper.setText(self._translate("Dialog", set_label_font(MAPPER_PACKAGE)))
        self.mapper_desc.setText(self._translate("Dialog", MAPPER_PACKAGE_DESC))
        self.xml.setText(self._translate("Dialog", set_label_font(XML_PATH)))
        self.xml_desc.setText(self._translate("Dialog", XML_PATH_DESC))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mybatis_tab),
                                          self._translate("Dialog", MYBATIS_TAB_TITLE))
        self.spring_title.setText(
            self._translate("Dialog", set_title_font(SPRING_TITLE)))
        self.spring_desc.setText(self._translate("Dialog", SPRING_GENERATOR_DESC))
        self.service.setText(self._translate("Dialog", set_label_font(SERVICE_PACKAGE)))
        self.service_desc.setText(self._translate("Dialog", SERVICE_PACKAGE_DESC))
        self.service_impl.setText(self._translate("Dialog", set_label_font(SERVICE_IMPL_PACKAGE)))
        self.service_impl_desc.setText(self._translate("Dialog", SERVICE_IMPL_PACKAGE_DESC))
        self.controller.setText(self._translate("Dialog", set_label_font(CONTROLLER_PACKAGE)))
        self.controller_desc.setText(self._translate("Dialog", CONTROLLER_PACKAGE_DESC))
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
        self.generate_button.setDisabled(True)
        self.generate_button.setFont(set_font())
        self.buttonBox_2.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)
        self.buttonBox_2.button(QtWidgets.QDialogButtonBox.Cancel).setFont(set_font())
        # 选择文件夹按钮
        self.java_button.setText(CHOOSE_DIRECTORY)
        self.java_src_button.setText(CHOOSE_DIRECTORY)
        self.model_button.setText(CHOOSE_DIRECTORY)
        self.mapper_button.setText(CHOOSE_DIRECTORY)
        self.xml_button.setText(CHOOSE_DIRECTORY)
        self.service_button.setText(CHOOSE_DIRECTORY)
        self.service_impl_button.setText(CHOOSE_DIRECTORY)
        self.controller_button.setText(CHOOSE_DIRECTORY)

    def pre_step(self):
        # 隐藏选择生成器界面
        self.widget.hide()
        # 展示树控件
        self.parent.tree_widget.show()

    def generate(self):
        # lombok选值
        self.project_output_dict['lombok'] = eval(self.lombok_comboBox.currentText())
        # 检验输入是否正确，只做警告提示
        wrong_params = check_params(self)
        if wrong_params:
            reply = pop_warning(WARNING_TITLE, PARAM_WARNING_MSG.format(wrong_params))
            if not reply:
                return
        self.parent.generate(self.project_output_dict)


