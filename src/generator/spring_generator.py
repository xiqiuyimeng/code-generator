# -*- coding: utf-8 -*-
from jinja2 import Template

from src.constant.constant import DEFAULT_PATH, DEFAULT_JAVA_SRC_RELATIVE_PATH
from src.generator.mybatis_generator import MybatisGenerator

_author_ = 'luwt'
_date_ = '2020/4/19 23:37'


class SpringGenerator(MybatisGenerator):
    """
    对mybatis生成器做扩展，生成相应的service、serviceImpl、controller，仅作为参考框架
        参数（此处未说明之参数，参见 MybatisGenerator 类文档）

        `service_tp`
            service文件的模板，存在于系统模板库中
        `service_impl_tp`
            serviceImpl文件的模板，存在于系统模板库中
        `controller_tp`
            controller文件的模板，存在于系统模板库中
        `service_package`
            service文件所在包命名空间，例如com.demo.service，该命名空间将被作为service文件头部的引包声明，若无则不声明包命名空间。
            由包命名空间，生成器可生成service文件的命名空间，此命名空间将用于controller中作为引包声明，若无，则不声明
        `service_impl_package`
            service文件所在包命名空间，例如com.demo.service.impl，该命名空间将被作为serviceImpl文件头部的引包声明，若无则不声明。
        `controller_package`
            service文件所在包命名空间，例如com.demo.controller，该命名空间将被作为controller文件头部的引包声明，若无则不声明。
    """

    def __init__(
            self,
            db_executor,
            table_schema,
            table_name,
            column_name=None,
            output_path=DEFAULT_PATH,
            lombok=True,
            model_package=None,
            mapper_package=None,
            service_package=None,
            service_impl_package=None,
            controller_package=None,
            java_path=None,
            xml_path=None,
            consumer=None,
            java_src_relative=DEFAULT_JAVA_SRC_RELATIVE_PATH,
            **kwargs
    ):
        super().__init__(
            db_executor,
            table_schema,
            table_name,
            column_name,
            output_path,
            lombok,
            model_package,
            mapper_package,
            java_path,
            xml_path,
            consumer,
            java_src_relative,
            **kwargs
        )
        self.service_tp = self.template.service_tp
        self.service_impl_tp = self.template.service_impl_tp
        self.controller_tp = self.template.controller_tp
        # service包命名空间
        self.service_package = service_package
        # serviceImpl包命名空间
        self.service_impl_package = service_impl_package
        # controller包命名空间
        self.controller_package = controller_package
        # service文件命名空间
        self.service_namespace = f'{self.service_package}.{self.class_name}Service'
        # service文件保存路径
        self.service_path = self.get_path(self.service_package) + '/' + f'{self.class_name}Service.java'
        # serviceImpl文件命名空间
        self.service_impl_namespace = f'{self.service_impl_package}.{self.class_name}ServiceImpl'
        # serviceImpl文件保存路径
        self.service_impl_path = self.get_path(self.service_impl_package) + '/' + f'{self.class_name}ServiceImpl.java'
        # controller文件命名空间
        self.controller_namespace = f'{self.controller_package}.{self.class_name}Controller'
        # controller文件保存路径
        self.controller_path = self.get_path(self.controller_package) + '/' + f'{self.class_name}Controller.java'

    def generate_service(self):
        content = Template(self.service_tp, trim_blocks=True, lstrip_blocks=True).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            service_package=self.service_package, param=self.param, key=self.key
        )
        self.save(self.service_path, content)

    def generate_service_impl(self):
        content = Template(self.service_impl_tp, trim_blocks=True, lstrip_blocks=True).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            mapper_namespace=self.mapper_namespace, param=self.param, key=self.key,
            service_impl_package=self.service_impl_package, hump_cls_name=self.hump_cls_name,
            service_namespace=self.service_namespace
        )
        self.save(self.service_impl_path, content)

    def generate_controller(self):
        content = Template(self.controller_tp, trim_blocks=True, lstrip_blocks=True).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            service_namespace=self.service_namespace, param=self.param, key=self.key,
            controller_package=self.controller_package, hump_cls_name=self.hump_cls_name
        )
        self.save(self.controller_path, content)

    def main(self):
        super().main()
        self.generate_service()
        self.generate_service_impl()
        self.generate_controller()

