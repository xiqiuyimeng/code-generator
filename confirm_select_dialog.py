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
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QFileDialog

from constant import CONFIRM_TREE_HEADER_LABELS, NEXT_STEP_BUTTON, CANCEL_BUTTON, COLLAPSE_BUTTON, EXPAND_BUTTON, \
    CHOOSE_DIRECTORY, DEFAULT_JAVA_SRC_RELATIVE_PATH, WARNING_TITLE, JAVA_SRC_PATH, MODEL_PACKAGE, \
    MAPPER_PACKAGE, XML_PATH, SERVICE_PACKAGE, SERVICE_IMPL_PACKAGE, CONTROLLER_PACKAGE, PARAM_WARNING_MSG, \
    WARNING_NONE, WRONG_TITLE
from do_generate import dispatch_generate
from font import set_font
from message_box import pop_warning, pop_fail
from select_generator_ui import setup_tab_ui


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
        self.widget.setObjectName("widget")
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
        self.make_tree()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate("Dialog", "Dialog"))
        self.treeWidget.headerItem().setText(0, self._translate("Dialog", CONFIRM_TREE_HEADER_LABELS))
        self.expand_collapse_button = self.first_buttonBox_2.button(QtWidgets.QDialogButtonBox.Ok)
        self.expand_collapse_button.setText(COLLAPSE_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText(NEXT_STEP_BUTTON)
        self.first_buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).setText(CANCEL_BUTTON)

    def make_tree(self):
        """根据选中数据构建树"""
        for conn_name, db_dict in self.selected_data.items():
            conn_item = self.make_item(self.treeWidget, conn_name)
            for db_name, tb_dict in db_dict.items():
                db_item = self.make_item(conn_item, db_name)
                for tb_name, cols in tb_dict.items():
                    tb_item = self.make_item(db_item, tb_name)
                    for col in cols:
                        self.make_item(tb_item, col)
        self.treeWidget.expandAll()

    def make_item(self, parent, name):
        item = QTreeWidgetItem(parent)
        item.setText(0, self._translate("Dialog", name))
        return item

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

    def generate(self):
        # lombok选值
        self.output_config_dict['lombok'] = eval(self.lombok_comboBox.currentText())
        # 检验是否mybatis页面都已选择
        if not self.check_no_none():
            pop_fail(WRONG_TITLE, WARNING_NONE)
        # 检验输入是否正确，只做警告提示
        wrong_params = self.check_params()
        if wrong_params:
            reply = pop_warning(WARNING_TITLE, PARAM_WARNING_MSG.format(wrong_params))
            if not reply:
                return
        dispatch_generate(self.gui, self.output_config_dict, self.selected_data)

    def check_no_none(self):
        """检查是否都有值"""
        mybatis_output_param = self.java_lineEdit.text(), self.java_src_lineEdit.text(), \
                               self.model_lineEdit.text(), self.mapper_lineEdit.text(), \
                               self.xml_lineEdit.text()
        return all(mybatis_output_param)

    def check_params(self):
        # 参数校验
        wrong_params = list()
        # java源码路径，应该在java项目路径下
        if not self.abs_java_src.startswith(self.java_path):
            wrong_params.append(JAVA_SRC_PATH)
        # 实体类的包名，也就是路径，应该在java源码路径下
        elif not self.model_path.startswith(self.abs_java_src):
            wrong_params.append(MODEL_PACKAGE)
        # mapper的包名，也就是路径，应该在java源码路径下
        elif not self.mapper_path.startswith(self.abs_java_src):
            wrong_params.append(MAPPER_PACKAGE)
        # xml的路径，应该在java项目路径下
        elif not self.xml_path.startswith(self.java_path):
            wrong_params.append(XML_PATH)
        # service的包名，也就是路径，应该在java源码路径下
        elif hasattr(self, 'service_path') and not self.service_path.startswith(self.abs_java_src):
            wrong_params.append(SERVICE_PACKAGE)
        # service_impl的包名，也就是路径，应该在java源码路径下
        elif hasattr(self, 'service_impl_path') and not self.service_impl_path.startswith(self.abs_java_src):
            wrong_params.append(SERVICE_IMPL_PACKAGE)
        # controller的包名，也就是路径，应该在java源码路径下
        elif hasattr(self, 'controller_path') and not self.controller_path.startswith(self.abs_java_src):
            wrong_params.append(CONTROLLER_PACKAGE)
        return wrong_params

    def choose_java_dir(self):
        """选择java项目地址"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, '/')
        self.java_lineEdit.setText(directory)
        self.set_java_path(directory)

    def input_java_path(self):
        """java项目地址输入框"""
        if self.java_lineEdit.text():
            self.set_java_path(self.java_lineEdit.text())

    def set_java_path(self, directory):
        # java源码包地址
        self.output_config_dict['java_path'] = directory
        self.java_path = directory
        # 自动检索并填充java源码包路径
        if os.path.isdir(directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH):
            java_src = DEFAULT_JAVA_SRC_RELATIVE_PATH
            # 绝对路径
            self.abs_java_src = directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH
            self.fill_java_src(java_src)
        # 解锁源码包，xml选择文件夹按钮
        if os.path.isdir(directory):
            self.java_src_button.setDisabled(False)
            self.xml_button.setDisabled(False)

    def choose_java_src_dir(self):
        """选择java源码包相对路径"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.java_path)
        self.abs_java_src = directory
        java_src = directory[len(self.java_path) + 1:]
        self.fill_java_src(java_src)

    def input_java_src_path(self):
        """java源码相对路径输入框"""
        java_src = self.java_src_lineEdit.text()
        if java_src:
            self.abs_java_src = self.java_path + '/' + java_src
            self.fill_java_src(java_src)

    def fill_java_src(self, java_src):
        """填充java_src路径，并解锁相关按钮"""
        self.java_src_lineEdit.setText(java_src)
        self.output_config_dict['java_src_relative'] = java_src
        # 解锁剩余的五个包名选择文件夹按钮
        self.model_button.setDisabled(False)
        self.mapper_button.setDisabled(False)
        self.service_button.setDisabled(False)
        self.service_impl_button.setDisabled(False)
        self.controller_button.setDisabled(False)

    def choose_model_dir(self):
        """选择java实体类包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.model_path = directory
        model_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.model_lineEdit.setText(model_package)
        self.output_config_dict['model_package'] = model_package

    def input_model_path(self):
        """实体类包名输入框"""
        model_package = self.model_lineEdit.text()
        if model_package:
            self.model_path = self.package_to_path(model_package)
            self.output_config_dict['model_package'] = model_package

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

    def input_mapper_path(self):
        """mapper接口包名输入框"""
        mapper_package = self.mapper_lineEdit.text()
        if mapper_package:
            self.mapper_path = self.package_to_path(mapper_package)
            self.output_config_dict['mapper_package'] = mapper_package

    def choose_xml_dir(self):
        """选择xml地址"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.java_path)
        self.xml_path = directory
        self.xml_lineEdit.setText(directory)
        self.output_config_dict['xml_path'] = directory

    def input_xml_path(self):
        """输入xml地址框"""
        xml_path = self.xml_lineEdit.text()
        if xml_path:
            self.xml_path = xml_path
            self.output_config_dict['xml_path'] = xml_path

    def choose_service_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.service_path = directory
        service_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.service_lineEdit.setText(service_package)
        self.output_config_dict['service_package'] = service_package

    def input_service_path(self):
        """service包名输入框"""
        service_package = self.service_lineEdit.text()
        if service_package:
            self.service_path = self.package_to_path(service_package)
            self.output_config_dict['service_package'] = service_package

    def choose_service_impl_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.service_impl_path = directory
        service_impl_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.service_impl_lineEdit.setText(service_impl_package)
        self.output_config_dict['service_impl_package'] = service_impl_package

    def input_service_impl_path(self):
        """service_impl输入框"""
        service_impl_package = self.service_impl_lineEdit.text()
        if service_impl_package:
            self.service_impl_path = self.package_to_path(service_impl_package)
            self.output_config_dict['service_impl_package'] = service_impl_package

    def choose_controller_dir(self):
        """选择service接口包名"""
        directory = QFileDialog.getExistingDirectory(self.widget_generator, CHOOSE_DIRECTORY, self.abs_java_src)
        self.controller_path = directory
        controller_package = (directory[len(self.abs_java_src) + 1:]).replace("/", ".")
        self.controller_lineEdit.setText(controller_package)
        self.output_config_dict['controller_package'] = controller_package

    def input_controller_path(self):
        """controller包名输入框"""
        controller_package = self.controller_lineEdit.text()
        if controller_package:
            self.controller_path = self.package_to_path(controller_package)
            self.output_config_dict['controller_package'] = controller_package
