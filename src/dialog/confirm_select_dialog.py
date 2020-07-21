# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'confirm_select_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
"""
点击生成按钮，弹窗页面。
第一个页面为选择表字段展示页面。
第二个页面为生成器输出配置页面
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog

from src.constant.constant import CONFIRM_TREE_HEADER_LABELS, NEXT_STEP_BUTTON, \
    CANCEL_BUTTON, COLLAPSE_BUTTON, EXPAND_BUTTON, CHOOSE_DIRECTORY, \
    WARNING_TITLE, PARAM_WARNING_MSG
from src.dialog.generate_result_dialog import GenerateResultDialog
from src.dialog.select_generator_ui import setup_tab_ui
from src.func.confirm_select_function import check_params, \
    set_java_path, fill_java_src, make_tree, clear_java_path_input, clear_src_input, clear_model_package_input, \
    clear_mapper_package_input, clear_xml_input, clear_service_package_input, clear_service_impl_package_input, \
    clear_controller_package_input, clear_spring_input, clear_mybatis_input, set_generate_button_available
from src.little_widget.message_box import pop_warning
from src.sys.settings.font import set_font


class DisplaySelectedDialog(QDialog):

    def __init__(self, gui, selected_data):
        super().__init__()
        self.dialog = self
        # 维护主界面窗口对象
        self.gui = gui
        # 选中的数据，以此来渲染树
        self.selected_data = selected_data
        # 输出配置，也就是在第二步中选择的数据
        self.output_config_dict = dict()
        self._translate = _translate = QtCore.QCoreApplication.translate
        self.setup_ui()

    def setup_ui(self):
        self.dialog.setObjectName("Dialog")
        # 固定大小，不允许缩放
        self.dialog.setFixedSize(1000, 800)

        self.dialog.setFont(set_font())

        self.verticalLayout = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(self.dialog)
        self.widget.setObjectName("little_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(self.widget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        # 字体
        self.treeWidget.setFont(set_font())
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.first_splitter = QtWidgets.QSplitter(self.widget)
        self.first_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.first_splitter.setObjectName("first_splitter")
        # 按钮
        self.first_buttonBox_2 = QtWidgets.QDialogButtonBox(self.first_splitter)
        self.first_buttonBox_2.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.first_buttonBox_2.setObjectName("first_buttonBox_2")
        self.first_buttonBox_2.setLayoutDirection(Qt.RightToLeft)
        self.first_buttonBox = QtWidgets.QDialogButtonBox(self.first_splitter)
        self.first_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.first_buttonBox.setObjectName("first_buttonBox")
        self.verticalLayout_2.addWidget(self.first_splitter)
        self.verticalLayout.addWidget(self.widget)

        # 去掉窗口右上角的问号
        self.dialog.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)

        # 按钮响应事件
        self.first_buttonBox.accepted.connect(self.next_step)
        self.first_buttonBox.rejected.connect(self.dialog.close)
        self.first_buttonBox_2.accepted.connect(self.expand_collapse)
        make_tree(self)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.treeWidget.headerItem().setText(0, self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.expand_collapse_button = self.first_buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok)
        self.expand_collapse_button.setText(COLLAPSE_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(NEXT_STEP_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)

    def expand_collapse(self):
        # 如果当前是展开，就关闭所有项，并将按钮文字改为展开所有，
        #  如果是关闭状态，就展开所有项，将按钮文字改为关闭所有
        if self.expand_collapse_button.text() == EXPAND_BUTTON:
            self.expand_collapse_button.setText(COLLAPSE_BUTTON)
            self.treeWidget.expandAll()
        else:
            self.expand_collapse_button.setText(EXPAND_BUTTON)
            self.treeWidget.collapseAll()

    def next_step(self):
        # 隐藏树控件
        self.widget.hide()
        # 打开下一页
        if hasattr(self, 'widget_generator'):
            self.widget_generator.show()
        else:
            setup_tab_ui(self)

    def pre_step(self):
        # 隐藏选择生成器界面
        self.widget_generator.hide()
        # 展示树控件
        self.widget.show()

    def clear_current_param(self):
        # spring tab页，清空spring页
        if self.tabWidget.currentIndex() == 1:
            clear_spring_input(self)
        else:
            # lombok置为默认的True
            self.lombok_comboBox.setCurrentIndex(0)
            clear_spring_input(self)
            clear_mybatis_input(self)

    def generate(self):
        # lombok选值
        self.output_config_dict['lombok'] = eval(self.lombok_comboBox.currentText())
        # 检验输入是否正确，只做警告提示
        wrong_params = check_params(self)
        if wrong_params:
            reply = pop_warning(WARNING_TITLE, PARAM_WARNING_MSG.format(wrong_params))
            if not reply:
                return
        dialog = GenerateResultDialog(self.gui, self.output_config_dict, self.selected_data)
        dialog.close_parent_signal.connect(self.dialog.close)
        dialog.exec()

    def choose_java_dir(self):
        """选择java项目地址"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, '/')
        self.java_lineEdit.setText(directory)
        set_java_path(self, directory)
        set_generate_button_available(self)

    def input_java_path(self):
        """java项目地址输入框"""
        if self.java_lineEdit.text():
            set_java_path(self, self.java_lineEdit.text())
        else:
            # 如果清空了输入框，那么就其余输入都关闭
            clear_java_path_input(self)
        set_generate_button_available(self)

    def choose_java_src_dir(self):
        """选择java源码包相对路径"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.java_path)
        self.abs_java_src = directory
        java_src = directory[len(self.java_path) + 1:]
        self.java_src_lineEdit.setText(java_src)
        fill_java_src(self, java_src)
        set_generate_button_available(self)

    def input_java_src_path(self):
        """java源码相对路径输入框"""
        java_src = self.java_src_lineEdit.text()
        if java_src:
            self.abs_java_src = self.java_path + '/' + java_src
            fill_java_src(self, java_src)
        else:
            # 关闭输入框
            clear_src_input(self)
        set_generate_button_available(self)

    def choose_model_dir(self):
        """选择java实体类包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.model_path = directory
        model_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.model_lineEdit.setText(model_package)
        self.output_config_dict['model_package'] = model_package
        set_generate_button_available(self)

    def input_model_path(self):
        """实体类包名输入框"""
        model_package = self.model_lineEdit.text()
        if model_package:
            self.model_path = self.package_to_path(model_package)
            self.output_config_dict['model_package'] = model_package
        else:
            # 清空数据
            clear_model_package_input(self)
        set_generate_button_available(self)

    def package_to_path(self, package):
        """将包名转换为全路径"""
        path = package.replace('.', '/')
        return self.abs_java_src + '/' + path

    def choose_mapper_dir(self):
        """选择mapper接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.mapper_path = directory
        mapper_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.mapper_lineEdit.setText(mapper_package)
        self.output_config_dict['mapper_package'] = mapper_package
        set_generate_button_available(self)

    def input_mapper_path(self):
        """mapper接口包名输入框"""
        mapper_package = self.mapper_lineEdit.text()
        if mapper_package:
            self.mapper_path = self.package_to_path(mapper_package)
            self.output_config_dict['mapper_package'] = mapper_package
        else:
            # 清空数据
            clear_mapper_package_input(self)
        set_generate_button_available(self)

    def choose_xml_dir(self):
        """选择xml地址"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.java_path)
        self.xml_path = directory
        self.xml_lineEdit.setText(directory)
        self.output_config_dict['xml_path'] = directory
        set_generate_button_available(self)

    def input_xml_path(self):
        """输入xml地址框"""
        xml_path = self.xml_lineEdit.text()
        if xml_path:
            self.xml_path = xml_path
            self.output_config_dict['xml_path'] = xml_path
        else:
            # 清空数据库
            clear_xml_input(self)
        set_generate_button_available(self)

    def choose_service_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.service_path = directory
        service_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.service_lineEdit.setText(service_package)
        self.output_config_dict['service_package'] = service_package
        set_generate_button_available(self)

    def input_service_path(self):
        """service包名输入框"""
        service_package = self.service_lineEdit.text()
        if service_package:
            self.service_path = self.package_to_path(service_package)
            self.output_config_dict['service_package'] = service_package
        else:
            # 清空数据
            clear_service_package_input(self)
        set_generate_button_available(self)

    def choose_service_impl_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.service_impl_path = directory
        service_impl_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.service_impl_lineEdit.setText(service_impl_package)
        self.output_config_dict['service_impl_package'] = service_impl_package
        set_generate_button_available(self)

    def input_service_impl_path(self):
        """service_impl输入框"""
        service_impl_package = self.service_impl_lineEdit.text()
        if service_impl_package:
            self.service_impl_path = self.package_to_path(service_impl_package)
            self.output_config_dict['service_impl_package'] = service_impl_package
        else:
            # 清空数据
            clear_service_impl_package_input(self)
        set_generate_button_available(self)

    def choose_controller_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.controller_path = directory
        controller_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.controller_lineEdit.setText(controller_package)
        self.output_config_dict['controller_package'] = controller_package
        set_generate_button_available(self)

    def input_controller_path(self):
        """controller包名输入框"""
        controller_package = self.controller_lineEdit.text()
        if controller_package:
            self.controller_path = self.package_to_path(controller_package)
            self.output_config_dict['controller_package'] = controller_package
        else:
            # 清空数据
            clear_controller_package_input(self)
        set_generate_button_available(self)

