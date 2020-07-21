# -*- coding: utf-8 -*-
import os

from PyQt5.QtWidgets import QTreeWidgetItem

from src.constant.constant import DEFAULT_JAVA_SRC_RELATIVE_PATH, JAVA_SRC_PATH, MODEL_PACKAGE, MAPPER_PACKAGE, \
    XML_PATH, SERVICE_PACKAGE, SERVICE_IMPL_PACKAGE, CONTROLLER_PACKAGE

_author_ = 'luwt'
_date_ = '2020/7/21 16:04'


def make_tree(self):
    """根据选中数据构建树"""
    for conn_name, db_dict in self.selected_data.items():
        conn_item = make_item(self, self.treeWidget, conn_name)
        for db_name, tb_dict in db_dict.items():
            db_item = make_item(self, conn_item, db_name)
            for tb_name, cols in tb_dict.items():
                tb_item = make_item(self, db_item, tb_name)
                for col in cols:
                    make_item(self, tb_item, col)
    self.treeWidget.expandAll()


def make_item(self, parent, name):
    item = QTreeWidgetItem(parent)
    item.setText(0, self._translate("Dialog", name))
    return item


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


def disable_package_button(self, status):
    """禁用需要输入包名的按钮输入框"""
    self.model_button.setDisabled(status)
    self.model_lineEdit.setDisabled(status)
    self.mapper_button.setDisabled(status)
    self.mapper_lineEdit.setDisabled(status)
    self.service_button.setDisabled(status)
    self.service_lineEdit.setDisabled(status)
    self.service_impl_button.setDisabled(status)
    self.service_impl_lineEdit.setDisabled(status)
    self.controller_button.setDisabled(status)
    self.controller_lineEdit.setDisabled(status)


def clear_java_path_input(self):
    """清空java项目地址输入框"""
    self.java_lineEdit.setText("")
    if hasattr(self, 'java_path'):
        del self.java_path
    if self.output_config_dict.get('java_path'):
        del self.output_config_dict['java_path']
    # 禁用src和xml的按钮输入框并清空内容
    disable_src_xml_button(self, True)
    clear_src_input(self)
    clear_xml_input(self)


def clear_src_input(self):
    """清除src的内容，禁用所有包名输入按钮并清空内容"""
    self.java_src_lineEdit.setText("")
    if hasattr(self, 'abs_java_src'):
        del self.abs_java_src
    if self.output_config_dict.get('java_src_relative'):
        del self.output_config_dict['java_src_relative']
    # 禁用所有包名输入框按钮并清空内容
    disable_package_button(self, True)
    clear_mybatis_package_input(self)
    clear_spring_input(self)


def clear_xml_input(self):
    """清空xml地址输入框"""
    self.xml_lineEdit.setText("")
    if hasattr(self, 'xml_path'):
        del self.xml_path
    if self.output_config_dict.get('xml_path'):
        del self.output_config_dict['xml_path']


def clear_model_package_input(self):
    """清空model包名输入框"""
    self.model_lineEdit.setText("")
    if hasattr(self, 'model_path'):
        del self.model_path
    if self.output_config_dict.get('model_package'):
        del self.output_config_dict['model_package']


def clear_mapper_package_input(self):
    """清空mapper包名输入框"""
    self.mapper_lineEdit.setText("")
    if hasattr(self, 'mapper_path'):
        del self.mapper_path
    if self.output_config_dict.get('mapper_package'):
        del self.output_config_dict['mapper_package']


def clear_mybatis_package_input(self):
    """清空mybatis页面的包名输入框"""
    clear_model_package_input(self)
    clear_mapper_package_input(self)


def clear_service_package_input(self):
    """清空service包名输入框"""
    self.service_lineEdit.setText("")
    if hasattr(self, 'service_path'):
        del self.service_path
    if self.output_config_dict.get('service_package'):
        del self.output_config_dict['service_package']


def clear_service_impl_package_input(self):
    """清空service impl包名输入框"""
    self.service_impl_lineEdit.setText("")
    if hasattr(self, 'service_impl_path'):
        del self.service_impl_path
    if self.output_config_dict.get('service_impl_package'):
        del self.output_config_dict['service_impl_package']


def clear_controller_package_input(self):
    """清空service impl包名输入框"""
    self.controller_lineEdit.setText("")
    if hasattr(self, 'controller_path'):
        del self.controller_path
    if self.output_config_dict.get('controller_package'):
        del self.output_config_dict['controller_package']


def clear_spring_input(self):
    """清空spring页输入的参数"""
    clear_service_package_input(self)
    clear_service_impl_package_input(self)
    clear_controller_package_input(self)


def clear_mybatis_input(self):
    """清空mybatis页输入的参数"""
    self.clear_java_path_input()
    self.clear_src_xml_input()
    self.clear_mybatis_package_input()


def disable_src_xml_button(self, status):
    """禁用源码包和xml输入框按钮"""
    self.java_src_button.setDisabled(status)
    self.java_src_lineEdit.setDisabled(status)
    self.xml_button.setDisabled(status)
    self.xml_lineEdit.setDisabled(status)


def set_java_path(self, directory):
    # java源码包地址
    self.output_config_dict['java_path'] = directory
    self.java_path = directory
    # 自动检索并填充java源码包路径
    if os.path.isdir(directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH):
        java_src = DEFAULT_JAVA_SRC_RELATIVE_PATH
        # 绝对路径
        self.abs_java_src = directory + '/' + DEFAULT_JAVA_SRC_RELATIVE_PATH
        self.java_src_lineEdit.setText(java_src)
        fill_java_src(self, java_src)
    # 解锁源码包，xml选择文件夹按钮输入框
    if os.path.isdir(directory):
        disable_src_xml_button(self, False)


def fill_java_src(self, java_src):
    """填充java_src路径，并解锁相关按钮"""
    self.output_config_dict['java_src_relative'] = java_src
    # 解锁剩余的五个包名选择文件夹按钮
    disable_package_button(self, False)


def check_mybatis_lineEdit(self):
    """检查mybatis配置页所有输入是否都有值"""
    java_path = self.java_lineEdit.text()
    java_src = self.java_src_lineEdit.text()
    model_package = self.model_lineEdit.text()
    mapper_package = self.mapper_lineEdit.text()
    xml_path = self.xml_lineEdit.text()
    return all((java_path, java_src, model_package, mapper_package, xml_path))


def check_spring_lineEdit(self):
    """检查spring配置页所有输入是否都有值或都为空"""
    service_package = self.service_lineEdit.text()
    service_impl_package = self.service_impl_lineEdit.text()
    controller_package = self.controller_lineEdit.text()
    return all((service_package, service_impl_package, controller_package)) \
           or all((not service_package, not service_impl_package, not controller_package))


def set_generate_button_available(self):
    """检查输入，如果mybatis页都有值，并且spring页都有值或为空，那么生成按钮可用"""
    if check_mybatis_lineEdit(self) and check_spring_lineEdit(self):
        self.generate_button.setDisabled(False)
    else:
        self.generate_button.setDisabled(True)
