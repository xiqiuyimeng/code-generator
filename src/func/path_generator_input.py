# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QFileDialog
from src.constant_.constant import CHOOSE_DIRECTORY
import os

_author_ = 'luwt'
_date_ = '2020/7/24 17:30'


def check_path_mybatis_lineEdit(ui):
    """检查mybatis配置页所有输入是否都有值"""
    output_path = ui.output_lineEdit.text()
    model_package = ui.model_lineEdit.text()
    mapper_package = ui.mapper_lineEdit.text()
    return all((output_path, model_package, mapper_package)) \
           and os.path.isdir(output_path)


def check_path_spring_lineEdit(ui):
    """检查spring配置页所有输入是否都有值或都为空"""
    service_package = ui.service_lineEdit.text()
    service_impl_package = ui.service_impl_lineEdit.text()
    controller_package = ui.controller_lineEdit.text()
    return all((service_package, service_impl_package, controller_package)) \
           or all((not service_package, not service_impl_package, not controller_package))


def set_generate_button_available(ui):
    """检查输入，如果mybatis页都有值，并且spring页都有值或为空，那么生成按钮可用"""
    if check_path_mybatis_lineEdit(ui) and check_path_spring_lineEdit(ui):
        ui.generate_button.setDisabled(False)
    else:
        ui.generate_button.setDisabled(True)


def clear_spring_input(ui):
    ServicePathInputHandler.clear_service_package_input(ui)
    ServiceImplPathInputHandler.clear_service_impl_package_input(ui)
    ControllerPathInputHandler.clear_controller_package_input(ui)


def clear_current_param(ui):
    # spring tab页，清空spring页
    if ui.tabWidget.currentIndex() == 1:
        clear_spring_input(ui)
    else:
        # lombok置为默认的True
        ui.lombok_comboBox.setCurrentIndex(0)
        OutputPathInputHandler().clear_output_path_input(ui)
        set_generate_button_available(ui)


class PathInputHandlerAbstract(ABC):

    @abstractmethod
    def input(self, ui): ...


class OutputPathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        """
        指定地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        if ui.output_lineEdit.text():
            if os.path.isdir(ui.output_lineEdit.text()):
                ui.path_output_dict['output_path'] = ui.output_lineEdit.text()
                # 解锁剩余可输入框
                self.disable_package_button(ui, False)
                set_generate_button_available(ui)
            else:
                # 屏蔽所有输入框
                self.disable_package_button(ui, True)
        else:
            # 如果清空了输入框，那么就将其余输入都关闭
            self.clear_output_path_input(ui)

    def choose_dir(self, ui):
        """
        选择指定地址
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        directory = QFileDialog.getExistingDirectory(ui.widget, CHOOSE_DIRECTORY, '/')
        if directory:
            ui.output_lineEdit.setText(directory)
            ui.path_output_dict['output_path'] = directory
            # 解锁剩余可输入框
            self.disable_package_button(ui, False)
            set_generate_button_available(ui)

    @staticmethod
    def disable_package_button(ui, status):
        """
        禁用需要输入包名的按钮输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        :param status: 状态，是否禁用
        """
        ui.model_lineEdit.setDisabled(status)
        ui.mapper_lineEdit.setDisabled(status)
        ui.service_lineEdit.setDisabled(status)
        ui.service_impl_lineEdit.setDisabled(status)
        ui.controller_lineEdit.setDisabled(status)

    @staticmethod
    def clear_output_path_input(ui):
        """
        清空指定地址输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        ui.output_lineEdit.clear()
        if ui.path_output_dict.get('output_path'):
            del ui.path_output_dict['output_path']
        OutputPathInputHandler.disable_package_button(ui, True)
        ModelPathInputHandler.clear_model_package_input(ui)
        MapperPathInputHandler.clear_mapper_package_input(ui)
        clear_spring_input(ui)


class ModelPathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        model_package = ui.model_lineEdit.text()
        if model_package:
            ui.path_output_dict['model_package'] = model_package
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
        if ui.path_output_dict.get('model_package'):
            del ui.path_output_dict['model_package']


class MapperPathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        """
        mapper接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        mapper_package = ui.mapper_lineEdit.text()
        if mapper_package:
            ui.path_output_dict['mapper_package'] = mapper_package
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
        if ui.path_output_dict.get('mapper_package'):
            del ui.path_output_dict['mapper_package']


class ServicePathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        """
        service接口包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        service_package = ui.service_lineEdit.text()
        if service_package:
            ui.path_output_dict['service_package'] = service_package
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
        if ui.path_output_dict.get('service_package'):
            del ui.path_output_dict['service_package']


class ServiceImplPathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        """
        service实现类输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        service_impl_package = ui.service_impl_lineEdit.text()
        if service_impl_package:
            ui.path_output_dict['service_impl_package'] = service_impl_package
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
        if ui.path_output_dict.get('service_impl_package'):
            del ui.path_output_dict['service_impl_package']


class ControllerPathInputHandler(PathInputHandlerAbstract):

    def input(self, ui):
        """
        controller类包名输入框
        :param ui: ui对象，维护的父级对象为生成器对话框对象DisplaySelectedDialog
            属性widget为包含了所有页面元素的小部件对象，用于在布局中互相替换，实现换页
        """
        controller_package = ui.controller_lineEdit.text()
        if controller_package:
            ui.path_output_dict['controller_package'] = controller_package
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
        if ui.path_output_dict.get('controller_package'):
            del ui.path_output_dict['controller_package']
