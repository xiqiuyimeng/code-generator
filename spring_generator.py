# -*- coding: utf-8 -*-
import time
import os
from xml.etree import cElementTree

from mysql_generator.mybatis_generator import MybatisGenerator
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

    def __init__(self,
                 host,
                 user,
                 pwd,
                 db,
                 table_schema,
                 table_name,
                 port=3306,
                 charset='utf8',
                 column_name=None,
                 java_tp='java.txt',
                 mapper_tp='mapper.txt',
                 xml_tp='xml.txt',
                 service_tp='service.txt',
                 service_impl_tp='service_impl.txt',
                 controller_tp='controller.txt',
                 path='./输出目录',
                 lombok=True,
                 exec_sql=None,
                 model_package=None,
                 mapper_package=None,
                 service_package=None,
                 service_impl_package=None,
                 controller_package=None):
        super().__init__(host,
                         user,
                         pwd,
                         db,
                         table_schema,
                         table_name,
                         port,
                         charset,
                         column_name,
                         java_tp,
                         mapper_tp,
                         xml_tp,
                         path,
                         lombok,
                         exec_sql,
                         model_package,
                         mapper_package)
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
        self.service_path = os.path.join(self.path, f'{self.class_name}Service.java')
        # serviceImpl文件命名空间
        self.service_impl_namespace = f'{self.service_impl_package}.{self.class_name}ServiceImpl'
        # serviceImpl文件保存路径
        self.service_impl_path = os.path.join(self.path, f'{self.class_name}ServiceImpl.java')
        # controller文件命名空间
        self.controller_namespace = f'{self.controller_package}.{self.class_name}Controller'
        # controller文件保存路径
        self.controller_path = os.path.join(self.path, f'{self.class_name}Controller.java')

    def generate_service(self):
        content = self.env.get_template(self.service_tp).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            service_package=self.service_package, param=self.param, key=self.key
        )
        self.save(self.service_path, content)

    def generate_service_impl(self):
        content = self.env.get_template(self.service_impl_tp).render(
            cls_name=self.class_name, model_namespace=self.model_namespace,
            mapper_namespace=self.mapper_namespace, param=self.param, key=self.key,
            service_impl_package=self.service_impl_package, hump_cls_name=self.hump_cls_name
        )
        self.save(self.service_impl_path, content)

    def generate_controller(self):
        content = self.env.get_template(self.controller_tp).render(
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


if __name__ == '__main__':
    try:
        tree = cElementTree.parse(os.path.join(os.path.abspath('.'), 'config.xml'))
        root = tree.getroot()
        host = root.find('database').find('host').text
        port = root.find('database').find('port').text
        user = root.find('database').find('user').text
        pwd = root.find('database').find('pwd').text
        db = root.find('database').find('db').text
        charset = root.find('database').find('charset').text
        table_schema = root.find('generator').find('table_schema').text
        table_name = root.find('generator').find('table_name').text
        column = root.find('generator').find('column').text
        path = root.find('generator').find('path').text
        lombok = root.find('generator').find('lombok').text
        lombok = True if lombok.lower() == 'true' else False
        exec_sql = root.find('generator').find('exec_sql').text
        table_names = table_name.split(',')
        model_package = root.find('else').find('model_package').text
        mapper_package = root.find('else').find('mapper_package').text
        service_package = root.find('else').find('service_package').text
        service_impl_package = root.find('else').find('service_impl_package').text
        controller_package = root.find('else').find('controller_package').text
        choose = int(input("请选择生成下面哪一种代码：\r\n1.mybatis(mapper, xml, model)\r\n"
                           "2.spring(controller, service, serviceImpl, mapper, xml, model)"))
        if choose == 1:
            # 如果可执行语句存在或者指定列名存在就不应该循环执行
            if (exec_sql or column) and len(table_names) == 1:
                generator = MybatisGenerator(host, user, pwd, db, table_schema, table_name.strip(),
                                             port, charset, column, path=path, lombok=lombok,
                                             exec_sql=exec_sql, model_package=model_package,
                                             mapper_package=mapper_package)
                generator.main()
                print("执行成功！五秒后退出")
                time.sleep(5)
            elif len(table_names) >= 1:
                for t_name in table_names:
                    generator = MybatisGenerator(host, user, pwd, db, table_schema, t_name.strip(),
                                                 port, charset, column, path=path, lombok=lombok,
                                                 exec_sql=exec_sql, model_package=model_package,
                                                 mapper_package=mapper_package)
                    generator.main()
                print("执行成功！五秒后退出")
                time.sleep(5)
            else:
                input("请检查config.xml中参数，按任意键退出")
        elif choose == 2:
            if len(table_names) >= 1 and not exec_sql and not column:
                for t_name in table_names:
                    generator = SpringGenerator(host, user, pwd, db, table_schema, table_name,
                                                port, charset, path=path, lombok=lombok,
                                                model_package=model_package, mapper_package=mapper_package,
                                                service_package=service_package,
                                                service_impl_package=service_impl_package,
                                                controller_package=controller_package)
                    generator.main()
                print("执行成功！五秒后退出")
                time.sleep(5)
            else:
                input("spring代码不支持指定列和自定义sql，请检查config.xml中参数，按任意键退出")
        else:
            input("输入不合法，按任意键退出")
    except Exception as e:
        print("执行出错：=>\n\n{}\n\n按任意键退出".format(e))
        input()
