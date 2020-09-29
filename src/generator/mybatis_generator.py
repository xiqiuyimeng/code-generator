# -*- coding: utf-8 -*-
import os

from jinja2 import Template

from src.constant import mysql_type as mt
from src.constant.constant import DEFAULT_PATH, DEFAULT_JAVA_SRC_RELATIVE_PATH, DEFAULT_MODEL_NS, DEFAULT_MAPPER_NS, \
    PARAM_PATH_ERROR, QUERY_SYS_TB, QUERY_TEMP_TB, CREATE_TEMP_TB, OUTPUT_PREFIX
from src.sys.sys_info_storage.template_sqlite import TemplateSqlite

_author_ = 'luwt'
_date_ = '2019/3/5 15:17'


class Data:

    def __init__(self, name, column_name, java_type, jdbc_type, comment=None):
        # java字段名，驼峰
        self.name = name
        # 数据库字段名，下划线
        self.column_name = column_name
        self.java_type = java_type
        self.jdbc_type = jdbc_type
        self.comment = comment if comment is None \
            else comment.replace("\r\n", " ")


class MybatisGenerator:
    """
    默认生成lombok的@Data注释，可配置生成getter和setter方法，如果生成getter和setter则不会生成@Data，
    可以配置生成多表字段联合的java类和resultMap，也可以指定某表的某些字段
        参数：

        `cursor`
            数据库连接游标，可操作数据库
        `table_schema`
            数据库名称，需要传
        `table_name`
            数据库表名，暂时只支持单表，将生成java、mapper、xml
        `column_name`
            单表情况下可指定字段，默认为None，如果不为None，只会生成java和xml，
            其中xml不会生成select和delete，另外所有的where语句也会缺省
            传参形式为字符串，多个字段名用逗号分隔
        `java_tp`
            java类文件的模板，存在于系统模板库中
        `mapper_tp`
            mapper.java接口文件的模板，存在于系统模板库中
        `xml_tp`
            mapper.xml配置文件的模板，存在于系统模板库中
        `output_path`
            输出路径，默认为'./输出目录'，可修改
        `lombok`
            在生成java类时是否生成lombok的@Data注释，默认true，若配置为false则生成getter和setter方法
        `exec_sql`
            可执行的sql查询语句，用于多表联合查询情况，默认None，开启后将会生成相应的java类和xml，不会生成mapper.java，
            xml中只会生成resultMap
        优先级：exec_sql 最高，有可执行语句即按exec_sql执行，其次，必须指定表名，列名可不指定，列名指定后，按列名来执行
        `model_package`
            实体类文件所在的包命名空间，例如 com.demo.model，它将被作为实体类文件的文件头部的引包声明，若无则不声明包命名空间。
            由包命名空间，生成器可生成实体类文件的命名空间，它将被用于xml文件及mapper文件中。
                xml：在resultMap、插入、更新块语句中需要声明实体类命名空间，若无，则默认填写“实体类”。
                mapper: 在插入、更新接口中需要使用实体类，若无实体类命名空间，则默认不引入。
        `mapper_package`
            mapper文件所在包命名空间，例如com.demo.dao，该命名空间将被作为mapper文件头部的引包声明，若无则不声明包命名空间。
            由包命名空间，生成器可生成mapper文件的命名空间，此命名空间将用于xml中作为namespace存在，若无，则默认填写“待填写”
        `java_path`
            java项目路径，如果此参数有效，将忽视path参数。如果存在，将生成到指定项目，否则生成到output_path输出目录。
                绝对路径 D:\java_workspaces\demo
        `xml_path`
            xml文件输出路径，如果此参数有效，将忽视path参数
        `consumer`
            作为消费者生成器，负责发送每次生成文件的信息，发送需要生成的文件总数，当前已生成的百分比，文件输出路径
        `file_count`
            文件总数，生成器总共需要生成的文件总数，不是只当前对象需要生成的，为了配合页面进度条
        `count`
            当前已经生成的文件数，与上面文件总数可计算当前进度，也就是返回的百分比
        `java_src_relative`
            java项目默认的源码包相对路径结构，默认为 src/main/java，由此参数，可结合java_path生成项目源码包绝对路径，
            再与命名空间拼接，可推出文件的绝对路径
    """
    def __init__(
            self,
            cursor,
            table_schema,
            table_name,
            column_name=None,
            output_path=DEFAULT_PATH,
            lombok=True,
            exec_sql=None,
            model_package=None,
            mapper_package=None,
            java_path=None,
            xml_path=None,
            consumer=None,
            file_count=None,
            count=None,
            java_src_relative=DEFAULT_JAVA_SRC_RELATIVE_PATH,
            **kwargs
    ):
        self.cursor = cursor
        # 库名
        self.table_schema = table_schema
        # 表名
        self.table_name = table_name
        # 可选：字段名，列表形式
        self.column_name = column_name
        # 可执行的sql语句
        self.exec_sql = exec_sql
        # 查询结果为字段名，类型，约束（判断是否为主键PRI即可，应用在按主键查询更新删除等操作），自定义sql提供完整查询字段即可
        self.sql = self.get_sql()
        # 获取查询的数据
        self.data = self.get_data()
        # 主键信息
        self.primary = list(filter(lambda k: k[2] == 'PRI', self.data))
        # 是否开启lombok注解
        self.lombok = lombok
        # 是否需要更新语句，如果表中都是主键，就不需要更新语句了
        self.need_update = False if len(self.primary) == len(self.data) else True
        # 确认在查询语句时，传参的类型
        self.param = ''
        # 确认在查询语句时，传参的值，一般为主键
        self.key = ''
        self.get_param_key()
        self.class_name = self.deal_class_name()
        # 驼峰形式的类名
        self.hump_cls_name = self.class_name.replace(
            self.class_name[:1],
            self.class_name[:1].lower(),
            1
        )
        self.mapper = True if not self.exec_sql and not self.column_name else False
        # 从库中读取正在使用的模板信息
        self.template = TemplateSqlite().get_using_template()
        # java实体类的模板
        self.java_tp = self.template.java_tp
        # mapper的模板
        self.mapper_tp = self.template.mapper_tp
        # xml的模板
        self.xml_tp = self.template.xml_tp
        self.separator = '/'
        # 默认输出目录"./输出目录"
        self.path = output_path
        # java项目地址，绝对路径 D:\java_workspaces\demo
        self.java_path = java_path
        # xml 路径
        self.xml_path = xml_path
        # java项目源码包相对路径 src/main/java
        self.java_src_relative = java_src_relative.replace("\\", '/')
        self.model_package = model_package
        self.mapper_package = mapper_package
        # model实体类文件的存放目录
        model_absolute_path = self.get_path(self.model_package)
        # model文件输出路径
        self.java_output_path = model_absolute_path + '/' + f'{self.class_name}.java'
        # xml文件输出路径，根据实体类文件的存放目录是否是默认的目录来判断xml目录地址，
        # 如果是默认目录，那么说明xml也应该输出到默认目录，否则应该输出到xml_path
        xml_absolute_path = self.path if self.path == model_absolute_path else self.xml_path
        self.xml_output_path = xml_absolute_path + '/' + f'{self.class_name}Mapper.xml'
        # mapper文件输出路径，如果是任意字段组合（主要用于多表字段联合情况），不需要生成Mapper.java
        self.mapper_output_path = self.get_path(self.mapper_package) + '/' + \
                                  f'{self.class_name}Mapper.java' if self.mapper else None
        self.model_namespace = f'{self.model_package}.{self.class_name}' \
            if self.model_package else DEFAULT_MODEL_NS
        self.mapper_namespace = f'{self.mapper_package}.{self.class_name}Mapper' \
            if self.mapper_package else DEFAULT_MAPPER_NS
        self.consumer = consumer
        self.file_count = file_count
        self.count = count

    def get_path(self, package=None):
        """
        获取生成文件的父级目录，注意，如果是开启了java_path，xml_path和java_src_relative，
        那么xml路径即为xml路径 + xml文件名，
        java类路径需要拼接：java_path + java_src_relative + package.replace(".", separator)
        :param package 文件的包路径，如果为空，参数不全，所以返回默认输出目录
        """
        if all(
                (
                        self.java_path,
                        self.xml_path,
                        self.java_src_relative,
                        package
                )
        ):
            return self.java_path + '/' + self.java_src_relative + '/' + package.replace(".", self.separator)
        elif self.path:
            return self.path
        else:
            raise EnvironmentError(PARAM_PATH_ERROR)

    def get_sql(self):
        """
        生成sql查询语句。
        如果是可执行sql语句，只能查询临时表；
        否则应查询系统表，如果指定了列名，那么在系统表中拼接过滤条件即可
        """
        sql = f'{QUERY_SYS_TB} where table_schema = "{self.table_schema}" ' \
              f'and table_name = "{self.table_name}"'
        if self.exec_sql:
            sql = QUERY_TEMP_TB
        elif self.column_name:
            # 如果只有一个值，就不需要循环了
            if len(self.column_name) == 1:
                sql += f' and column_name in ("{self.column_name[0]}")'
            else:
                for i, col_name in enumerate(self.column_name):
                    if i == 0:
                        sql += f' and column_name in ("{col_name}", '
                    elif col_name == self.column_name[-1]:
                        sql += f'"{col_name}")'
                    else:
                        sql += f'"{col_name}", '
        return sql

    def get_data(self):
        """连接数据库获取数据"""
        # 如果存在自定义sql，那么先生成临时表
        if self.exec_sql:
            self.cursor.execute(f'use {self.table_schema};')
            self.cursor.execute(f'{CREATE_TEMP_TB} {self.exec_sql};')
        self.cursor.execute(self.sql)
        data = list(self.cursor.fetchall())
        if self.exec_sql:
            for ix, line in enumerate(data):
                line = list(line)
                # 类型标准化，临时表中查得的类型是类型加字段长度，去除长度信息
                if line[1].find('(') > 0:
                    type_ = line[1][0: line[1].find('(')]
                    line[1] = type_
                data[ix] = line
        return data

    def deal_class_name(self):
        class_name = ''
        for name in self.table_name.split('_'):
            class_name += name.capitalize()
        return class_name

    @staticmethod
    def deal_column_name(db_column_name):
        """
        eg:
        user_name -> userName
        """
        column_list, column_name_str = db_column_name.split('_'), ''
        # 处理字段名称，采用驼峰式
        for column_name in column_list:
            if column_name != column_list[0]:
                column_name = column_name.capitalize()
            column_name_str += column_name
        return column_name_str

    @staticmethod
    def deal_type(data):
        """返回jdbcType和java_type，若在枚举类型里没有，一律视为字符串"""
        jdbc_type, java_type = mt.MysqlType.text.value[0],\
                               mt.MysqlType.text.value[1]
        try:
            jdbc_type, java_type = eval('mt.MysqlType.{}.value[0]'.format(data)), \
                                   eval('mt.MysqlType.{}.value[1]'.format(data))
        finally:
            return jdbc_type, java_type

    def get_param_key(self):
        # 多个主键的情况，mapper里的delete和select都应传入类，否则传主键
        if len(self.primary) > 1:
            self.param, self.key = self.class_name, self.class_name.lower()
        elif len(self.primary) == 1:
            self.param, self.key = self.deal_type(self.primary[0][1])[1], \
                                   self.deal_column_name(self.primary[0][0])

    def generate_java(self):
        java_list = []
        import_list = set()
        for line in self.data:
            # types -> tuple(jdbcType, javaType)
            name, types = self.deal_column_name(line[0]), \
                          self.deal_type(line[1])
            # 处理需要import的语句
            if types[1] in mt.import_type:
                import_list.add(mt.import_type.get(types[1]))
            data = Data(name, line[0], types[1], types[0], line[-1])
            java_list.append(data)
        content = Template(self.java_tp).render(
            cls_name=self.class_name, java_list=java_list,
            lombok=self.lombok, import_list=import_list,
            model_package=self.model_package
        )
        self.save(self.java_output_path, content)

    def generate_mapper(self):
        if self.mapper:
            content = Template(self.mapper_tp).render(
                cls_name=self.class_name, param=self.param, key=self.key,
                need_update=self.need_update, model_namespace=self.model_namespace,
                mapper_package=self.mapper_package, hump_cls_name=self.hump_cls_name
            )
            self.save(self.mapper_output_path, content)

    def generate_xml(self):
        # resultMap, base_column_list, 主键params, java类型（用于在）
        result_map, columns, params, java_type = [], [], [], ''
        # 生成base_column_list
        self.generate_base_col(columns)
        # 生成resultMap
        self.generate_result_map(result_map)
        # 处理主键对于java_type的影响
        if len(self.primary) > 1:
            java_type = self.deal_class_name()
        elif len(self.primary) == 1:
            java_type = self.deal_type(self.primary[0][1])[1]
        # 主键信息放入params中
        for primary in self.primary:
            params.append(Data(
                self.deal_column_name(primary[0]), primary[0],
                None, self.deal_type(primary[1])[0]
            ))
        update_columns = result_map[:]
        # 拷贝一份result_map，用以存放xml中的更新块字段数据，将其中的主键信息剔除
        self.rm_pri(update_columns, params)
        content = Template(self.xml_tp).render(
            cls_name=self.class_name, result_map=result_map, columns=columns,
            table_name=self.table_name, params=params, java_type=java_type,
            need_update=self.need_update, update_columns=update_columns,
            mapper=self.mapper, any_column=self.exec_sql,
            model_namespace=self.model_namespace, mapper_namespace=self.mapper_namespace
        )
        self.save(self.xml_output_path, content)

    @staticmethod
    def rm_pri(update_columns, params):
        """
        在update的时候，set语句中不需要主键的信息，
        主键是作为唯一标识，所以需要从update的语句中删除主键的信息
        """
        [update_columns.remove(result) for result in update_columns
         for param in params if param.column_name == result.column_name]

    def generate_base_col(self, columns):
        col, i = 0, 1
        for line in self.data:
            column_name, base_column = line[0], line[0] + ', '
            if line == self.data[-1]:
                base_column = column_name
            else:
                # 对baseColumnList进行换行处理，控制每行字符数
                col += len(base_column)
                if col > i * 80:
                    i += 1
                    base_column = column_name + ', \n\t'
            columns.append(base_column)

    def generate_result_map(self, result_map):
        for line in self.data:
            column_name = line[0]
            name = self.deal_column_name(line[0])
            jdbc_type = self.deal_type(line[1])[0]
            data = Data(name, column_name, java_type=None, jdbc_type=jdbc_type)
            result_map.append(data)

    def save(self, path, content):
        parent_dir = os.path.split(path)[0]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(path, 'w+', encoding='utf-8')as f:
            f.write(content)
            print(f'{OUTPUT_PREFIX}{path}')
            self.count += 1
            self.consumer.send([self.file_count, round(self.count * 100 / self.file_count), f'{OUTPUT_PREFIX}{path}'])

    def main(self):
        self.generate_java()
        self.generate_mapper()
        self.generate_xml()

