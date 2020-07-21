# -*- coding: utf-8 -*-
"""
点击生成按钮，弹窗的第二步页面，负责配置生成器的输出配置
"""
from PyQt5 import QtWidgets, QtCore

from src.constant.constant import CLEAR_CONFIG_BUTTON, PRE_STEP_BUTTON, GENERATE_BUTTON, \
    CANCEL_BUTTON, MYBATIS_TITLE, IS_LOMBOK, MYBATIS_GENERATOR_DESC, LOMBOK_DESC, \
    JAVA_PATH, JAVA_PATH_DESC, JAVA_SRC_PATH, JAVA_SRC_PATH_DESC, MODEL_PACKAGE, \
    MODEL_PACKAGE_DESC, MAPPER_PACKAGE, MAPPER_PACKAGE_DESC, XML_PATH, XML_PATH_DESC,\
    MYBATIS_TAB_TITLE, SPRING_TAB_TITLE, SPRING_TITLE, SPRING_GENERATOR_DESC, \
    SERVICE_PACKAGE, SERVICE_PACKAGE_DESC, SERVICE_IMPL_PACKAGE, SERVICE_IMPL_PACKAGE_DESC, \
    CONTROLLER_PACKAGE, CONTROLLER_PACKAGE_DESC, CHOOSE_DIRECTORY
from src.sys.settings.font import set_label_font, set_title_font

_author_ = 'luwt'
_date_ = '2020/7/18 11:47'


def setup_tab_ui(confirm_select_ui):
    """
    构建选择生成器的tab标签界面
    :param confirm_select_ui: 弹窗确认生成器配置页的主窗口对象
    """
    confirm_select_ui.widget_generator = QtWidgets.QWidget(confirm_select_ui.dialog)
    confirm_select_ui.widget_generator.setObjectName("little_widget")
    confirm_select_ui.verticalLayout_2 = QtWidgets.QVBoxLayout(confirm_select_ui.widget_generator)
    confirm_select_ui.verticalLayout_2.setObjectName("verticalLayout_2")
    confirm_select_ui.tabWidget = QtWidgets.QTabWidget(confirm_select_ui.widget_generator)
    confirm_select_ui.tabWidget.setObjectName("tabWidget")
    # mybatis标签页
    setup_mybatis_tab_ui(confirm_select_ui)
    # spring标签页
    setup_spring_tab_ui(confirm_select_ui)

    confirm_select_ui.tabWidget.addTab(confirm_select_ui.spring_tab, "")
    confirm_select_ui.verticalLayout_2.addWidget(confirm_select_ui.tabWidget)
    # 按钮部分
    confirm_select_ui.splitter = QtWidgets.QSplitter(confirm_select_ui.widget_generator)
    confirm_select_ui.splitter.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter.setObjectName("splitter")
    confirm_select_ui.buttonBox = QtWidgets.QDialogButtonBox(confirm_select_ui.splitter)
    confirm_select_ui.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    confirm_select_ui.buttonBox.setObjectName("buttonBox")
    confirm_select_ui.buttonBox.setLayoutDirection(QtCore.Qt.RightToLeft)
    confirm_select_ui.buttonBox_2 = QtWidgets.QDialogButtonBox(confirm_select_ui.splitter)
    confirm_select_ui.buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
    confirm_select_ui.buttonBox_2.setObjectName("buttonBox_2")
    confirm_select_ui.verticalLayout_2.addWidget(confirm_select_ui.splitter)
    confirm_select_ui.verticalLayout.addWidget(confirm_select_ui.widget_generator)

    # 按钮点击事件
    confirm_select_ui.buttonBox.accepted.connect(confirm_select_ui.clear_current_param)
    confirm_select_ui.buttonBox.rejected.connect(confirm_select_ui.pre_step)
    confirm_select_ui.buttonBox_2.accepted.connect(confirm_select_ui.generate)
    confirm_select_ui.buttonBox_2.rejected.connect(confirm_select_ui.close)
    # 选择文件夹按钮
    confirm_select_ui.java_button.clicked.connect(confirm_select_ui.choose_java_dir)
    confirm_select_ui.java_src_button.clicked.connect(confirm_select_ui.choose_java_src_dir)
    confirm_select_ui.model_button.clicked.connect(confirm_select_ui.choose_model_dir)
    confirm_select_ui.mapper_button.clicked.connect(confirm_select_ui.choose_mapper_dir)
    confirm_select_ui.xml_button.clicked.connect(confirm_select_ui.choose_xml_dir)
    confirm_select_ui.service_button.clicked.connect(confirm_select_ui.choose_service_dir)
    confirm_select_ui.service_impl_button.clicked.connect(confirm_select_ui.choose_service_impl_dir)
    confirm_select_ui.controller_button.clicked.connect(confirm_select_ui.choose_controller_dir)

    # 输入框文本编辑事件
    confirm_select_ui.java_lineEdit.textEdited.connect(confirm_select_ui.input_java_path)
    confirm_select_ui.java_src_lineEdit.textEdited.connect(confirm_select_ui.input_java_src_path)
    confirm_select_ui.model_lineEdit.textEdited.connect(confirm_select_ui.input_model_path)
    confirm_select_ui.mapper_lineEdit.textEdited.connect(confirm_select_ui.input_mapper_path)
    confirm_select_ui.xml_lineEdit.textEdited.connect(confirm_select_ui.input_xml_path)
    confirm_select_ui.service_lineEdit.textEdited.connect(confirm_select_ui.input_service_path)
    confirm_select_ui.service_impl_lineEdit.textEdited.connect(confirm_select_ui.input_service_impl_path)
    confirm_select_ui.controller_lineEdit.textEdited.connect(confirm_select_ui.input_controller_path)

    # 填充文字
    fill_text(confirm_select_ui)


def setup_mybatis_tab_ui(confirm_select_ui):
    """
    构建mybatis生成器配置标签页
    :param confirm_select_ui: 弹窗确认生成器配置页的主窗口对象
    :return:
    """
    confirm_select_ui.mybatis_tab = QtWidgets.QWidget()
    confirm_select_ui.mybatis_tab.setObjectName("mybatis_tab")
    confirm_select_ui.verticalLayout_3 = QtWidgets.QVBoxLayout(confirm_select_ui.mybatis_tab)
    confirm_select_ui.verticalLayout_3.setObjectName("verticalLayout_3")
    confirm_select_ui.mybatis_title = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.mybatis_title.setObjectName("mybatis_title")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.mybatis_title)
    confirm_select_ui.mybatis_first_blank = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.mybatis_first_blank.setText("")
    confirm_select_ui.mybatis_first_blank.setObjectName("mybatis_first_blank")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.mybatis_first_blank)
    confirm_select_ui.mybatis_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.mybatis_desc.setObjectName("mybatis_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.mybatis_desc)
    confirm_select_ui.mybatis_second_blank = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.mybatis_second_blank.setText("")
    confirm_select_ui.mybatis_second_blank.setObjectName("mybatis_second_blank")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.mybatis_second_blank)
    # lombok
    confirm_select_ui.splitter_lombok = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_lombok.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_lombok.setObjectName("splitter_lombok")
    confirm_select_ui.lombok = QtWidgets.QLabel(confirm_select_ui.splitter_lombok)
    confirm_select_ui.lombok.setObjectName("lombok")
    confirm_select_ui.lombok_comboBox = QtWidgets.QComboBox(confirm_select_ui.splitter_lombok)
    confirm_select_ui.lombok_comboBox.setObjectName("lombok_comboBox")
    confirm_select_ui.lombok_comboBox.addItem("")
    confirm_select_ui.lombok_comboBox.addItem("")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_lombok)
    confirm_select_ui.lombok_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.lombok_desc.setObjectName("lombok_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.lombok_desc)
    # java_path
    confirm_select_ui.splitter_java = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_java.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_java.setObjectName("splitter_java")
    confirm_select_ui.java = QtWidgets.QLabel(confirm_select_ui.splitter_java)
    confirm_select_ui.java.setObjectName("java")
    confirm_select_ui.java_button = QtWidgets.QPushButton(confirm_select_ui.splitter_java)
    confirm_select_ui.java_button.setObjectName("java_button")
    confirm_select_ui.java_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_java)
    confirm_select_ui.java_lineEdit.setObjectName("java_lineEdit")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_java)
    confirm_select_ui.java_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.java_desc.setObjectName("java_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.java_desc)
    # java_src
    confirm_select_ui.splitter_java_src = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_java_src.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_java_src.setObjectName("splitter_java_src")
    confirm_select_ui.java_src = QtWidgets.QLabel(confirm_select_ui.splitter_java_src)
    confirm_select_ui.java_src.setObjectName("java_src")
    confirm_select_ui.java_src_button = QtWidgets.QPushButton(confirm_select_ui.splitter_java_src)
    confirm_select_ui.java_src_button.setObjectName("java_src_button")
    # 初始不可用
    confirm_select_ui.java_src_button.setDisabled(True)
    confirm_select_ui.java_src_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_java_src)
    confirm_select_ui.java_src_lineEdit.setObjectName("java_src_lineEdit")
    # 初始不可用
    confirm_select_ui.java_src_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_java_src)
    confirm_select_ui.java_src_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.java_src_desc.setObjectName("java_src_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.java_src_desc)
    # model
    confirm_select_ui.splitter_model = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_model.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_model.setObjectName("splitter_model")
    confirm_select_ui.model = QtWidgets.QLabel(confirm_select_ui.splitter_model)
    confirm_select_ui.model.setObjectName("model")
    confirm_select_ui.model_button = QtWidgets.QPushButton(confirm_select_ui.splitter_model)
    confirm_select_ui.model_button.setObjectName("model_button")
    # 初始不可用
    confirm_select_ui.model_button.setDisabled(True)
    confirm_select_ui.model_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_model)
    confirm_select_ui.model_lineEdit.setObjectName("model_lineEdit")
    # 初始不可用
    confirm_select_ui.model_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_model)
    confirm_select_ui.model_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.model_desc.setObjectName("model_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.model_desc)
    # mapper
    confirm_select_ui.splitter_mapper = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_mapper.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_mapper.setObjectName("splitter_mapper")
    confirm_select_ui.mapper = QtWidgets.QLabel(confirm_select_ui.splitter_mapper)
    confirm_select_ui.mapper.setObjectName("mapper")
    confirm_select_ui.mapper_button = QtWidgets.QPushButton(confirm_select_ui.splitter_mapper)
    confirm_select_ui.mapper_button.setObjectName("mapper_button")
    # 初始不可用
    confirm_select_ui.mapper_button.setDisabled(True)
    confirm_select_ui.mapper_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_mapper)
    confirm_select_ui.mapper_lineEdit.setObjectName("mapper_lineEdit")
    # 初始不可用
    confirm_select_ui.mapper_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_mapper)
    confirm_select_ui.mapper_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.mapper_desc.setObjectName("mapper_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.mapper_desc)
    # xml
    confirm_select_ui.splitter_xml = QtWidgets.QSplitter(confirm_select_ui.mybatis_tab)
    confirm_select_ui.splitter_xml.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_xml.setObjectName("splitter_xml")
    confirm_select_ui.xml = QtWidgets.QLabel(confirm_select_ui.splitter_xml)
    confirm_select_ui.xml.setObjectName("xml")
    confirm_select_ui.xml_button = QtWidgets.QPushButton(confirm_select_ui.splitter_xml)
    confirm_select_ui.xml_button.setObjectName("xml_button")
    # 初始不可用
    confirm_select_ui.xml_button.setDisabled(True)
    confirm_select_ui.xml_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_xml)
    confirm_select_ui.xml_lineEdit.setObjectName("xml_lineEdit")
    # 初始不可用
    confirm_select_ui.xml_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.splitter_xml)
    confirm_select_ui.xml_desc = QtWidgets.QLabel(confirm_select_ui.mybatis_tab)
    confirm_select_ui.xml_desc.setObjectName("xml_desc")
    confirm_select_ui.verticalLayout_3.addWidget(confirm_select_ui.xml_desc)

    confirm_select_ui.tabWidget.addTab(confirm_select_ui.mybatis_tab, "")
    confirm_select_ui.spring_tab = QtWidgets.QWidget()
    confirm_select_ui.spring_tab.setObjectName("spring_tab")
    confirm_select_ui.verticalLayout_4 = QtWidgets.QVBoxLayout(confirm_select_ui.spring_tab)
    confirm_select_ui.verticalLayout_4.setObjectName("verticalLayout_4")


def setup_spring_tab_ui(confirm_select_ui):
    """
    构建spring生成器配置标签页
    :param confirm_select_ui: 弹窗确认生成器配置页的主窗口对象
    :return:
    """
    confirm_select_ui.spring_title = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_title.setObjectName("spring_title")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_title)
    confirm_select_ui.spring_first_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_first_blank.setText("")
    confirm_select_ui.spring_first_blank.setObjectName("spring_first_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_first_blank)
    confirm_select_ui.spring_desc = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_desc.setObjectName("spring_desc")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_desc)
    confirm_select_ui.spring_second_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_second_blank.setText("")
    confirm_select_ui.spring_second_blank.setObjectName("spring_second_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_second_blank)
    confirm_select_ui.spring_third_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_third_blank.setText("")
    confirm_select_ui.spring_third_blank.setObjectName("spring_third_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_third_blank)
    confirm_select_ui.spring_fourth_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_fourth_blank.setText("")
    confirm_select_ui.spring_fourth_blank.setObjectName("spring_fourth_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_fourth_blank)
    confirm_select_ui.spring_fifth_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_fifth_blank.setText("")
    confirm_select_ui.spring_fifth_blank.setObjectName("spring_fifth_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_fifth_blank)
    # service
    confirm_select_ui.splitter_service = QtWidgets.QSplitter(confirm_select_ui.spring_tab)
    confirm_select_ui.splitter_service.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_service.setObjectName("splitter_service")
    confirm_select_ui.service = QtWidgets.QLabel(confirm_select_ui.splitter_service)
    confirm_select_ui.service.setObjectName("service")
    confirm_select_ui.service_button = QtWidgets.QPushButton(confirm_select_ui.splitter_service)
    confirm_select_ui.service_button.setObjectName("service_button")
    # 初始不可用
    confirm_select_ui.service_button.setDisabled(True)
    confirm_select_ui.service_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_service)
    confirm_select_ui.service_lineEdit.setObjectName("service_lineEdit")
    # 初始不可用
    confirm_select_ui.service_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.splitter_service)
    confirm_select_ui.service_desc = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.service_desc.setObjectName("service_desc")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.service_desc)
    # service_impl
    confirm_select_ui.splitter_service_impl = QtWidgets.QSplitter(confirm_select_ui.spring_tab)
    confirm_select_ui.splitter_service_impl.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_service_impl.setObjectName("splitter_service_impl")
    confirm_select_ui.service_impl = QtWidgets.QLabel(confirm_select_ui.splitter_service_impl)
    confirm_select_ui.service_impl.setObjectName("service_impl")
    confirm_select_ui.service_impl_button = QtWidgets.QPushButton(confirm_select_ui.splitter_service_impl)
    confirm_select_ui.service_impl_button.setObjectName("service_impl_button")
    # 初始不可用
    confirm_select_ui.service_impl_button.setDisabled(True)
    confirm_select_ui.service_impl_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_service_impl)
    confirm_select_ui.service_impl_lineEdit.setObjectName("service_impl_lineEdit")
    # 初始不可用
    confirm_select_ui.service_impl_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.splitter_service_impl)
    confirm_select_ui.service_impl_desc = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.service_impl_desc.setObjectName("service_impl_desc")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.service_impl_desc)
    # controller
    confirm_select_ui.splitter_controller = QtWidgets.QSplitter(confirm_select_ui.spring_tab)
    confirm_select_ui.splitter_controller.setOrientation(QtCore.Qt.Horizontal)
    confirm_select_ui.splitter_controller.setObjectName("splitter_controller")
    confirm_select_ui.controller = QtWidgets.QLabel(confirm_select_ui.splitter_controller)
    confirm_select_ui.controller.setObjectName("controller")
    confirm_select_ui.controller_button = QtWidgets.QPushButton(confirm_select_ui.splitter_controller)
    confirm_select_ui.controller_button.setObjectName("controller_button")
    # 初始不可用
    confirm_select_ui.controller_button.setDisabled(True)
    confirm_select_ui.controller_lineEdit = QtWidgets.QLineEdit(confirm_select_ui.splitter_controller)
    confirm_select_ui.controller_lineEdit.setObjectName("controller_lineEdit")
    # 初始不可用
    confirm_select_ui.controller_lineEdit.setDisabled(True)
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.splitter_controller)
    confirm_select_ui.controller_desc = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.controller_desc.setObjectName("controller_desc")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.controller_desc)

    confirm_select_ui.spring_sixth_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_sixth_blank.setText("")
    confirm_select_ui.spring_sixth_blank.setObjectName("spring_sixth_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_sixth_blank)
    confirm_select_ui.spring_seventh_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_seventh_blank.setText("")
    confirm_select_ui.spring_seventh_blank.setObjectName("spring_seventh_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_seventh_blank)
    confirm_select_ui.spring_eighth_blank = QtWidgets.QLabel(confirm_select_ui.spring_tab)
    confirm_select_ui.spring_eighth_blank.setText("")
    confirm_select_ui.spring_eighth_blank.setObjectName("spring_eighth_blank")
    confirm_select_ui.verticalLayout_4.addWidget(confirm_select_ui.spring_eighth_blank)


def fill_text(confirm_select_ui):
    """
    对界面上的文字样式控制
    :param confirm_select_ui: 弹窗确认生成器配置页的主窗口对象
    :return:
    """
    confirm_select_ui.mybatis_title.setText(
        confirm_select_ui._translate("Dialog", set_title_font(MYBATIS_TITLE)))
    confirm_select_ui.mybatis_desc.setText(confirm_select_ui._translate("Dialog", MYBATIS_GENERATOR_DESC))
    confirm_select_ui.lombok.setText(confirm_select_ui._translate("Dialog", set_label_font(IS_LOMBOK)))
    confirm_select_ui.lombok_comboBox.setItemText(0, confirm_select_ui._translate("Dialog", "True"))
    confirm_select_ui.lombok_comboBox.setItemText(1, confirm_select_ui._translate("Dialog", "False"))
    confirm_select_ui.lombok_desc.setText(confirm_select_ui._translate("Dialog", LOMBOK_DESC))
    confirm_select_ui.java.setText(confirm_select_ui._translate("Dialog", set_label_font(JAVA_PATH)))
    confirm_select_ui.java_desc.setText(confirm_select_ui._translate("Dialog", JAVA_PATH_DESC))
    confirm_select_ui.java_src.setText(confirm_select_ui._translate("Dialog", set_label_font(JAVA_SRC_PATH)))
    confirm_select_ui.java_src_desc.setText(confirm_select_ui._translate("Dialog", JAVA_SRC_PATH_DESC))
    confirm_select_ui.model.setText(confirm_select_ui._translate("Dialog", set_label_font(MODEL_PACKAGE)))
    confirm_select_ui.model_desc.setText(confirm_select_ui._translate("Dialog", MODEL_PACKAGE_DESC))
    confirm_select_ui.mapper.setText(confirm_select_ui._translate("Dialog", set_label_font(MAPPER_PACKAGE)))
    confirm_select_ui.mapper_desc.setText(confirm_select_ui._translate("Dialog", MAPPER_PACKAGE_DESC))
    confirm_select_ui.xml.setText(confirm_select_ui._translate("Dialog", set_label_font(XML_PATH)))
    confirm_select_ui.xml_desc.setText(confirm_select_ui._translate("Dialog", XML_PATH_DESC))
    confirm_select_ui.tabWidget.setTabText(confirm_select_ui.tabWidget.indexOf(confirm_select_ui.mybatis_tab),
                                      confirm_select_ui._translate("Dialog", MYBATIS_TAB_TITLE))
    confirm_select_ui.spring_title.setText(
        confirm_select_ui._translate("Dialog", set_title_font(SPRING_TITLE)))
    confirm_select_ui.spring_desc.setText(confirm_select_ui._translate("Dialog", SPRING_GENERATOR_DESC))
    confirm_select_ui.service.setText(confirm_select_ui._translate("Dialog", set_label_font(SERVICE_PACKAGE)))
    confirm_select_ui.service_desc.setText(confirm_select_ui._translate("Dialog", SERVICE_PACKAGE_DESC))
    confirm_select_ui.service_impl.setText(confirm_select_ui._translate("Dialog", set_label_font(SERVICE_IMPL_PACKAGE)))
    confirm_select_ui.service_impl_desc.setText(confirm_select_ui._translate("Dialog", SERVICE_IMPL_PACKAGE_DESC))
    confirm_select_ui.controller.setText(confirm_select_ui._translate("Dialog", set_label_font(CONTROLLER_PACKAGE)))
    confirm_select_ui.controller_desc.setText(confirm_select_ui._translate("Dialog", CONTROLLER_PACKAGE_DESC))
    confirm_select_ui.tabWidget.setTabText(confirm_select_ui.tabWidget.indexOf(confirm_select_ui.spring_tab),
                                      confirm_select_ui._translate("Dialog", SPRING_TAB_TITLE))
    # 按钮
    confirm_select_ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(CLEAR_CONFIG_BUTTON)
    confirm_select_ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(PRE_STEP_BUTTON)
    # 生成按钮
    confirm_select_ui.generate_button = confirm_select_ui.buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok)
    confirm_select_ui.generate_button.setText(GENERATE_BUTTON)
    confirm_select_ui.generate_button.setDisabled(True)
    confirm_select_ui.buttonBox_2.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)
    # 选择文件夹按钮
    confirm_select_ui.java_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.java_src_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.model_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.mapper_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.xml_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.service_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.service_impl_button.setText(CHOOSE_DIRECTORY)
    confirm_select_ui.controller_button.setText(CHOOSE_DIRECTORY)
