# -*- coding: utf-8 -*-
from src.constant.constant import DEFAULT_JAVA_TP, DEFAULT_MAPPER_TP, DEFAULT_XML_TP, DEFAULT_SERVICE_TP, \
    DEFAULT_SERVICE_IMPL_TP, DEFAULT_CONTROLLER_TP, DEFAULT_PATH, DEFAULT_JAVA_SRC_RELATIVE_PATH
from src.generator.mybatis_generator import MybatisGenerator

_author_ = 'luwt'
_date_ = '2020/4/19 23:37'


class SpringGenerator(MybatisGenerator):
    """
    对mybatis生成器做扩展，生成相应的service、serviceImpl、controller，仅作为参考框架
        参数（此处未说明之参数，参见 MybatisGenerator 类文档）

        `service_tp`
            service文件的模板路径，默认为当前目录下的service.txt文件，目录可选为当前目录下的子目录
        `service_impl_tp`
            serviceImpl文件的模板路径，默认为当前目录下的service_impl.txt文件，目录可选为当前目录下的子目录
        `controller_tp`
            controller文件的模板路径，默认为当前目录下的controller.txt文件，目录可选为当前目录下的子目录
        `service_package`
            service文件所在包命名空间，例如com.demo.service，该命名空间将被作为service文件头部的引包声明，若无则不声明包命名空间。
            由包命名空间，生成器可生成service文件的命名空间，此命名空间将用于controller中作为引包声明，若无，则不声明
        `service_impl_package`
            service文件所在包命名空间，例如com.demo.serviceImpl，该命名空间将被作为serviceImpl文件头部的引包声明，若无则不声明。
        `controller_package`
            service文件所在包命名空间，例如com.demo.controller，该命名空间将被作为controller文件头部的引包声明，若无则不声明。
    """

    def __init__(
            self,
            cursor,
            table_schema,
            table_name,
            column_name=None,
            java_tp=DEFAULT_JAVA_TP,
            mapper_tp=DEFAULT_MAPPER_TP,
            xml_tp=DEFAULT_XML_TP,
            service_tp=DEFAULT_SERVICE_TP,
            service_impl_tp=DEFAULT_SERVICE_IMPL_TP,
            controller_tp=DEFAULT_CONTROLLER_TP,
            default_path=DEFAULT_PATH,
            lombok=True,
            exec_sql=None,
            model_package=None,
            mapper_package=None,
            service_package=None,
            service_impl_package=None,
            controller_package=None,
            java_path=None,
            xml_path=None,
            java_src_relative=DEFAULT_JAVA_SRC_RELATIVE_PATH,
            **kwargs
    ):
        super().__init__(
            cursor,
            table_schema,
            table_name,
            column_name,
            java_tp,
            mapper_tp,
            xml_tp,
            default_path,
            lombok,
            exec_sql,
            model_package,
            mapper_package,
            java_path,
            xml_path,
            java_src_relative,
            **kwargs
        )
        self.service_tp = service_tp
        self.service_impl_tp = service_impl_tp
        self.controller_tp = controller_tp
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

    def generate_service(self, count, file_count, consumer):
        content = self.env.get_template(self.service_tp).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            service_package=self.service_package, param=self.param, key=self.key
        )
        return self.save(self.service_path, content, count, file_count, consumer)

    def generate_service_impl(self, count, file_count, consumer):
        content = self.env.get_template(self.service_impl_tp).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            mapper_namespace=self.mapper_namespace, param=self.param, key=self.key,
            service_impl_package=self.service_impl_package, hump_cls_name=self.hump_cls_name,
            service_namespace=self.service_namespace
        )
        return self.save(self.service_impl_path, content, count, file_count, consumer)

    def generate_controller(self, count, file_count, consumer):
        content = self.env.get_template(self.controller_tp).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            service_namespace=self.service_namespace, param=self.param, key=self.key,
            controller_package=self.controller_package, hump_cls_name=self.hump_cls_name
        )
        return self.save(self.controller_path, content, count, file_count, consumer)

    def main(self, count, file_count, consumer):
        count = super().main(count, file_count, consumer)
        count = self.generate_service(count, file_count, consumer)
        count = self.generate_service_impl(count, file_count, consumer)
        count = self.generate_controller(count, file_count, consumer)
        return count

