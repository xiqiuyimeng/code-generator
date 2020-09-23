# -*- coding: utf-8 -*-
import os
from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QFileDialog

from src.constant.constant import CHOOSE_DIRECTORY, DEFAULT_JAVA_SRC_RELATIVE_PATH, \
    JAVA_SRC_PATH, MODEL_PACKAGE, MAPPER_PACKAGE, XML_PATH, SERVICE_PACKAGE,\
    SERVICE_IMPL_PACKAGE, CONTROLLER_PACKAGE

_author_ = 'luwt'
_date_ = '2020/7/23 19:04'


def check_params(ui):
    # 参数校验
    wrong_params = list()
    # java源码路径，应该在java项目路径下
    if not ui.abs_java_src.startswith(ui.java_path):
        wrong_params.append(JAVA_SRC_PATH)
    # 实体类的包名，也就是路径，应该在java源码路径下
    elif not ui.model_path.startswith(ui.abs_java_src):
        wrong_params.append(MODEL_PACKAGE)
    # mapper的包名，也就是路径，应该在java源码路径下
    elif not ui.mapper_path.startswith(ui.abs_java_src):
        wrong_params.append(MAPPER_PACKAGE)
    # xml的路径，应该在java项目路径下
    elif not ui.xml_path.startswith(ui.java_path):
        wrong_params.append(XML_PATH)
    # service的包名，也就是路径，应该在java源码路径下
    elif hasattr(ui, 'service_path') and not ui.service_path.startswith(ui.abs_java_src):
        wrong_params.append(SERVICE_PACKAGE)
    # service_impl的包名，也就是路径，应该在java源码路径下
    elif hasattr(ui, 'service_impl_path') and not ui.service_impl_path.startswith(ui.abs_java_src):
        wrong_params.append(SERVICE_IMPL_PACKAGE)
    # controller的包名，也就是路径，应该在java源码路径下
    elif hasattr(ui, 'controller_path') and not ui.controller_path.startswith(ui.abs_java_src):
        wrong_params.append(CONTROLLER_PACKAGE)
    return wrong_params


def package_to_path(ui, package):
    """将包名转换为全路径"""
    path = package.replace('.', '/')
    return ui.abs_java_src + '/' + path


def check_mybatis_lineEdit(ui):
    """检查mybatis配置页所有输入是否都有值"""
    java_path = ui.java_lineEdit.text()
    java_src = ui.java_src_lineEdit.text()
    model_package = ui.model_lineEdit.text()
    mapper_package = ui.mapper_lineEdit.text()
    xml_path = ui.xml_lineEdit.text()
    return all((java_path, java_src, model_package, mapper_package, xml_path))


def check_spring_lineEdit(ui):
    """检查spring配置页所有输入是否都有值或都为空"""
    service_package = ui.service_lineEdit.text()
    service_impl_package = ui.service_impl_lineEdit.text()
    controller_package = ui.controller_lineEdit.text()
    return all((service_package, service_impl_package, controller_package)) \
           or all((not service_package, not service_impl_package, not controller_package))


def set_generate_button_available(ui):
    """检查输入，如果mybatis页都有值，并且spring页都有值或为空，那么生成按钮可用"""
    if check_mybatis_lineEdit(ui) and check_spring_lineEdit(ui):
        ui.generate_button.setDisabled(False)
    else:
        ui.generate_button.setDisabled(True)


def clear_spring_input(ui):
    ServiceInputHandler.clear_service_package_input(ui)
    ServiceImplInputHandler.clear_service_impl_package_input(ui)
    ControllerInputHandler.clear_controller_package_input(ui)


def clear_current_param(ui):
    # spring tab页，清空spring页
    if ui.template_tab_widget.currentIndex() == 1:
        clear_spring_input(ui)
    else:
        # lombok置为默认的True
        ui.lombok_comboBox.setCurrentIndex(0)
        JavaInputHandler().clear_java_path_input(ui)
        set_generate_button_available(ui)


class ProjectInputHandlerAbstract(ABC):

    @abstractmethod
    def choose_dir(self, ui): ...

    @abstractmethod
    def input(self, ui): ...


class JavaInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择java项目地址
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, '/')
        if directory:
            ui.java_lineEdit.setText(directory)
            self.set_java_path(ui, directory)
            set_generate_button_available(ui)

    def input(self, ui):
        """
        java项目地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        if ui.java_lineEdit.text():
            if os.path.isdir(ui.java_lineEdit.text()):
                self.set_java_path(ui, ui.java_lineEdit.text())
            else:
                # 屏蔽其他输入框
                self.disable_src_xml_button(ui, True)
        else:
            # 如果清空了输入框，那么就将其余输入都关闭
            self.clear_java_path_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def set_java_path(ui, directory):
        """
        向生成器对话框的output_config_dict中存放值，
        向ui对象设置属性，用以最后校验数据
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        :param directory: 文件夹
        """
        # java源码包地址
        ui.project_output_dict['java_path'] = directory
        ui.java_path = directory
        # 自动检索并填充java源码包路径
        if os.path.isdir(directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH):
            java_src = DEFAULT_JAVA_SRC_RELATIVE_PATH
            # 绝对路径
            ui.abs_java_src = directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH
            ui.java_src_lineEdit.setText(java_src)
            JavaSrcInputHandler.fill_java_src(ui, java_src)
        # 解锁源码包，xml选择文件夹按钮输入框
        if os.path.isdir(directory):
            JavaInputHandler.disable_src_xml_button(ui, False)

    @staticmethod
    def clear_java_path_input(ui):
        """
        清空java项目地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.java_lineEdit.clear()
        if hasattr(ui, 'java_path'):
            del ui.java_path
        if ui.project_output_dict.get('java_path'):
            del ui.project_output_dict['java_path']
        # 禁用src和xml的按钮输入框并清空内容
        JavaInputHandler.disable_src_xml_button(ui, True)
        JavaSrcInputHandler.clear_src_input(ui)
        XmlInputHandler.clear_xml_input(ui)

    @staticmethod
    def disable_src_xml_button(ui, status):
        """
        禁用源码包和xml输入框按钮
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        :param status: 状态，是否禁用
        """
        ui.java_src_button.setDisabled(status)
        ui.java_src_lineEdit.setDisabled(status)
        ui.xml_button.setDisabled(status)
        ui.xml_lineEdit.setDisabled(status)


class JavaSrcInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择java源码包相对路径，通常为src/main/java
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.java_path)
        if directory:
            ui.abs_java_src = directory
            java_src = directory[len(ui.java_path) + 1:]
            ui.java_src_lineEdit.setText(java_src)
            self.fill_java_src(ui, java_src)
            set_generate_button_available(ui)

    def input(self, ui):
        """
        java源码包地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        java_src = ui.java_src_lineEdit.text()
        if java_src:
            ui.abs_java_src = ui.java_path + '/' + java_src
            self.fill_java_src(ui, java_src)
        else:
            # 关闭输入框
            self.clear_src_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def fill_java_src(ui, java_src):
        """
        填充java_src路径，并解锁相关按钮
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        :param java_src: java源码包相对路径
        """
        ui.project_output_dict['java_src_relative'] = java_src
        # 解锁剩余的五个包名选择文件夹按钮
        JavaSrcInputHandler.disable_package_button(ui, False)

    @staticmethod
    def clear_src_input(ui):
        """
        清除java源码包输入框的内容，禁用所有包名输入按钮并清空内容
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.java_src_lineEdit.clear()
        if hasattr(ui, 'abs_java_src'):
            del ui.abs_java_src
        if ui.project_output_dict.get('java_src_relative'):
            del ui.project_output_dict['java_src_relative']
        # 禁用所有包名输入框按钮并清空内容
        JavaSrcInputHandler.disable_package_button(ui, True)
        ModelInputHandler.clear_model_package_input(ui)
        MapperInputHandler.clear_mapper_package_input(ui)
        clear_spring_input(ui)

    @staticmethod
    def disable_package_button(ui, status):
        """
        禁用需要输入包名的按钮输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        :param status: 状态，是否禁用
        """
        ui.model_button.setDisabled(status)
        ui.model_lineEdit.setDisabled(status)
        ui.mapper_button.setDisabled(status)
        ui.mapper_lineEdit.setDisabled(status)
        ui.service_button.setDisabled(status)
        ui.service_lineEdit.setDisabled(status)
        ui.service_impl_button.setDisabled(status)
        ui.service_impl_lineEdit.setDisabled(status)
        ui.controller_button.setDisabled(status)
        ui.controller_lineEdit.setDisabled(status)


class ModelInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择java实体类包名路径，转化为包名的形式
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.abs_java_src)
        if directory:
            ui.model_path = directory
            model_package = (directory[len(ui.abs_java_src) + 1:]).replace("/", ".")
            ui.model_lineEdit.setText(model_package)
            ui.project_output_dict['model_package'] = model_package
            set_generate_button_available(ui)

    def input(self, ui):
        """
        java实体类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        model_package = ui.model_lineEdit.text()
        if model_package:
            ui.model_path = package_to_path(ui, model_package)
            ui.project_output_dict['model_package'] = model_package
        else:
            # 清空数据
            self.clear_model_package_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_model_package_input(ui):
        """
        清空java实体类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.model_lineEdit.clear()
        if hasattr(ui, 'model_path'):
            del ui.model_path
        if ui.project_output_dict.get('model_package'):
            del ui.project_output_dict['model_package']


class MapperInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择mapper接口包名
         :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.abs_java_src)
        if directory:
            ui.mapper_path = directory
            mapper_package = (directory[len(ui.abs_java_src) + 1:]).replace("/", ".")
            ui.mapper_lineEdit.setText(mapper_package)
            ui.project_output_dict['mapper_package'] = mapper_package
            set_generate_button_available(ui)

    def input(self, ui):
        """
        mapper接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        mapper_package = ui.mapper_lineEdit.text()
        if mapper_package:
            ui.mapper_path = package_to_path(ui, mapper_package)
            ui.project_output_dict['mapper_package'] = mapper_package
        else:
            # 清空数据
            self.clear_mapper_package_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_mapper_package_input(ui):
        """
        清空mapper接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.mapper_lineEdit.clear()
        if hasattr(ui, 'mapper_path'):
            del ui.mapper_path
        if ui.project_output_dict.get('mapper_package'):
            del ui.project_output_dict['mapper_package']


class XmlInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择xml地址
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.java_path)
        if directory:
            ui.xml_path = directory
            ui.xml_lineEdit.setText(directory)
            ui.project_output_dict['xml_path'] = directory
            set_generate_button_available(ui)

    def input(self, ui):
        """
        xml地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        xml_path = ui.xml_lineEdit.text()
        if xml_path:
            ui.xml_path = xml_path
            ui.project_output_dict['xml_path'] = xml_path
        else:
            # 清空数据
            self.clear_xml_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_xml_input(ui):
        """
        清空xml地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.xml_lineEdit.clear()
        if hasattr(ui, 'xml_path'):
            del ui.xml_path
        if ui.project_output_dict.get('xml_path'):
            del ui.project_output_dict['xml_path']


class ServiceInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择service接口包名
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.abs_java_src)
        if directory:
            ui.service_path = directory
            service_package = (directory[len(ui.abs_java_src) + 1:]).replace("/", ".")
            ui.service_lineEdit.setText(service_package)
            ui.project_output_dict['service_package'] = service_package
            set_generate_button_available(ui)

    def input(self, ui):
        """
        service接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        service_package = ui.service_lineEdit.text()
        if service_package:
            ui.service_path = package_to_path(ui, service_package)
            ui.project_output_dict['service_package'] = service_package
        else:
            # 清空数据
            self.clear_service_package_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_service_package_input(ui):
        """
        清空service接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.service_lineEdit.clear()
        if hasattr(ui, 'service_path'):
            del ui.service_path
        if ui.project_output_dict.get('service_package'):
            del ui.project_output_dict['service_package']


class ServiceImplInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择service实现类包名
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.abs_java_src)
        if directory:
            ui.service_impl_path = directory
            service_impl_package = (directory[len(ui.abs_java_src) + 1:]).replace("/", ".")
            ui.service_impl_lineEdit.setText(service_impl_package)
            ui.project_output_dict['service_impl_package'] = service_impl_package
            set_generate_button_available(ui)

    def input(self, ui):
        """
        service实现类输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        service_impl_package = ui.service_impl_lineEdit.text()
        if service_impl_package:
            ui.service_impl_path = package_to_path(ui, service_impl_package)
            ui.project_output_dict['service_impl_package'] = service_impl_package
        else:
            # 清空数据
            self.clear_service_impl_package_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_service_impl_package_input(ui):
        """
        清空service实现类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.service_impl_lineEdit.clear()
        if hasattr(ui, 'service_impl_path'):
            del ui.service_impl_path
        if ui.project_output_dict.get('service_impl_package'):
            del ui.project_output_dict['service_impl_package']


class ControllerInputHandler(ProjectInputHandlerAbstract):

    def choose_dir(self, ui):
        """
        选择controller类包名
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, ui.abs_java_src)
        if directory:
            ui.controller_path = directory
            controller_package = (directory[len(ui.abs_java_src) + 1:]).replace("/", ".")
            ui.controller_lineEdit.setText(controller_package)
            ui.project_output_dict['controller_package'] = controller_package
            set_generate_button_available(ui)

    def input(self, ui):
        """
        controller类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        controller_package = ui.controller_lineEdit.text()
        if controller_package:
            ui.controller_path = package_to_path(ui, controller_package)
            ui.project_output_dict['controller_package'] = controller_package
        else:
            # 清空数据
            self.clear_controller_package_input(ui)
        set_generate_button_available(ui)

    @staticmethod
    def clear_controller_package_input(ui):
        """
        清空controller类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.controller_lineEdit.clear()
        if hasattr(ui, 'controller_path'):
            del ui.controller_path
        if ui.project_output_dict.get('controller_package'):
            del ui.project_output_dict['controller_package']



