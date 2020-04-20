# -*- coding: utf-8 -*-
from mysql_generator import mysql_type as mt
from mysql_generator.get_cursor import Cursor
from mysql_generator.constant import *
from jinja2 import Environment, FileSystemLoader
import os
import sys
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
        self.comment = comment if comment is None else comment.replace("\r\n", " ")


class MybatisGenerator:
    """
    默认生成lombok的@Data注释，可配置生成getter和setter方法，如果生成getter和setter则不会生成@Data，
    可以配置生成多表字段联合的java类和resultMap，也可以指定某表的某些字段
        参数：

        `host`
            数据库地址
        `user`
            数据库用户名
        `pwd`
            数据库密码
        `db`
            数据库名
        `port`
            数据库端口
        `charset`
            数据库字符集信息
        `table_schema`
            数据库名称，需要传
        `table_name`
            数据库表名，暂时只支持单表，将生成java、mapper、xml
        `column_name`
            单表情况下可指定字段，默认为None，如果不为None，只会生成java和xml，
            其中xml不会生成select和delete，另外所有的where语句也会缺省
            传参形式为字符串，多个字段名用逗号分隔
        `java_tp`
            java类文件的模板，默认为当前目录下的java.txt文件，目录可选为当前目录下的子目录
        `mapper_tp`
            mapper.java接口文件的模板，默认为当前目录下的mapper.txt文件，目录可选为当前目录下的子目录
        `xml_tp`
            mapper.xml配置文件的模板，默认为当前目录下的xml.txt文件，目录可选为当前目录下的子目录
        `path`
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
            java文件输出路径，如果此参数有效，将忽视path参数。
                需要判断
        `xml_path`
            xml文件输出路径，如果此参数有效，将忽视path参数
        `java_src_relative`
            java项目默认的源码包相对路径结构，默认为 src/main/java，由此参数，可结合java_path生成项目源码包绝对路径，
            再与命名空间拼接，可推出文件的绝对路径
    """
    def __init__(
            self,
            host,
            user,
            pwd,
            db,
            table_schema,
            table_name,
            port=DEFAULT_DB_PORT,
            charset=DEFAULT_DB_CHARSET,
            column_name=None,
            java_tp=DEFAULT_JAVA_TP,
            mapper_tp=DEFAULT_MAPPER_TP,
            xml_tp=DEFAULT_XML_TP,
            path=DEFAULT_PATH,
            lombok=True,
            exec_sql=None,
            model_package=None,
            mapper_package=None,
            java_path=None,
            xml_path=None,
            java_src_relative=DEFAULT_JAVA_SRC_RELATIVE_PATH
    ):
        # 数据库信息
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db
        self.port = int(port) if port else DEFAULT_DB_PORT
        self.charset = charset if charset else DEFAULT_DB_CHARSET
        # 库名
        self.table_schema = table_schema
        # 表名
        self.table_name = table_name
        # 可选：字段名，字符串形式，逗号分隔
        self.column_name = column_name
        # 可执行的sql语句
        self.exec_sql = exec_sql
        # 查询结果为字段名，类型，约束（判断是否为主键PRI即可，应用在按主键查询更新删除等操作），自定义sql提供完整查询字段即可
        self.sql = self.get_sql()
        # 获取查询的数据
        self.data = self.get_data()
        # 主键信息
        self.primary = list(filter(lambda k: k[2] == 'PRI', self.data))
        # java实体类的模板文件
        self.java_tp = java_tp
        # mapper的模板文件
        self.mapper_tp = mapper_tp
        # xml的模板文件
        self.xml_tp = xml_tp
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
        self.hump_cls_name = self.class_name.replace(self.class_name[:1], self.class_name[:1].lower())
        self.appointed_columns = True if self.column_name else False
        self.mapper = True if not self.exec_sql and not self.appointed_columns else False
        # 获取模板文件
        self.env = Environment(loader=FileSystemLoader('./'), lstrip_blocks=True, trim_blocks=True)
        self.separator = '\\' if sys.platform.startswith("win") else '/'
        # 默认输出目录"./输出目录"
        self.path = path
        # java项目地址，绝对路径 D:\\java_workspaces\\demo
        self.java_path = java_path
        # xml 路径
        self.xml_path = xml_path
        # java项目源码包相对路径 src/main/java
        self.java_src_relative = java_src_relative.replace('/', '\\')
        self.model_package = model_package
        self.mapper_package = mapper_package
        # model文件输出路径
        self.java_output_path = os.path.join(self.get_path(self.model_package),
                                             f'{self.class_name}.java')
        # xml文件输出路径
        self.xml_output_path = os.path.join(self.get_path(), f'{self.class_name}Mapper.xml')
        # mapper文件输出路径，如果是任意字段组合（主要用于多表字段联合情况），不需要生成Mapper.java
        self.mapper_output_path = os.path.join(self.get_path(self.mapper_package),
                                               f'{self.class_name}Mapper.java') \
            if self.mapper else None
        self.model_namespace = f'{self.model_package}.{self.class_name}' \
            if self.model_package else DEFAULT_MODEL_NS
        self.mapper_namespace = f'{self.mapper_package}.{self.class_name}Mapper' \
            if self.mapper_package else DEFAULT_MAPPER_NS

    def get_path(self, package=None):
        """
        获取生成文件的父级目录，注意，如果是开启了java_path，xml_path和java_src_relative，
        那么xml路径即为xml路径 + xml文件名，
        java类路径需要拼接：java_path + java_src_relative + package.replace(".", separator)
        :param package 文件的包路径，如果为空，则是xml文件，return xml_path
        """
        if self.java_path and self.xml_path and self.java_src_relative:
            if package:
                # java类
                return os.path.join(
                    self.java_path,
                    self.java_src_relative,
                    package.replace(".", self.separator)
                )
            else:
                return self.xml_path
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
        sql = f'{QUERY_SYS_TB} where table_schema = "{self.table_schema}" and table_name = "{self.table_name}"'
        if self.exec_sql:
            sql = QUERY_TEMP_TB
        elif self.column_name:
            columns = list(map(lambda x: x.strip(), self.column_name.split(',')))
            for i, col_name in enumerate(columns):
                if i == 0:
                    sql += f' and column_name in ("{col_name}", '
                elif col_name == columns[-1]:
                    sql += f'"{col_name}")'
                else:
                    sql += f'"{col_name}", '
        return sql

    def get_data(self):
        """连接数据库获取数据"""
        with Cursor(self.host, self.user, self.pwd, self.db, self.port, self.charset) as cursor:
            # 如果存在自定义sql，那么先生成临时表
            if self.exec_sql:
                cursor.execute(f'use {self.table_schema};')
                cursor.execute(f'{CREATE_TEMP_TB} {self.exec_sql};')
            cursor.execute(self.sql)
            data = list(cursor.fetchall())
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
        column_list = db_column_name.split('_')
        column_name_str = ''
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
            self.param = self.class_name
            self.key = self.class_name.lower()
        elif len(self.primary) == 1:
            self.param = self.deal_type(self.primary[0][1])[1]
            self.key = self.deal_column_name(self.primary[0][0])

    def generate_java(self):
        java_list = []
        import_list = set()
        for line in self.data:
            name = self.deal_column_name(line[0])
            # types -> tuple(jdbcType, javaType)
            types = self.deal_type(line[1])
            # 处理需要import的语句
            if types[1] in mt.import_type:
                import_list.add(mt.import_type.get(types[1]))
            data = Data(name, line[0], types[1], types[0], line[-1])
            java_list.append(data)
        content = self.env.get_template(self.java_tp).render(
            cls_name=self.class_name, java_list=java_list,
            lombok=self.lombok, import_list=import_list,
            model_package=self.model_package
        )
        self.save(self.java_output_path, content)

    def generate_mapper(self):
        if self.mapper:
            content = self.env.get_template(self.mapper_tp).render(
                cls_name=self.class_name, param=self.param, key=self.key,
                need_update=self.need_update, model_namespace=self.model_namespace,
                mapper_package=self.mapper_package, hump_cls_name=self.hump_cls_name
            )
            self.save(self.mapper_output_path, content)

    def generate_xml(self):
        # resultMap
        result_map = []
        # base_column_list
        columns = []
        params = []
        java_type = ''
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
        content = self.env.get_template(self.xml_tp).render(
            cls_name=self.class_name, result_map=result_map, columns=columns,
            table_name=self.table_name, params=params, java_type=java_type,
            need_update=self.need_update, update_columns=update_columns,
            mapper=self.mapper, any_column=self.exec_sql,
            model_namespace=self.model_namespace, mapper_namespace=self.mapper_namespace
        )
        self.save(self.xml_output_path, content)

    @staticmethod
    def rm_pri(update_columns, params):
        for param in params:
            for result in update_columns:
                if param.column_name == result.column_name:
                    update_columns.remove(result)
                    continue

    def generate_base_col(self, columns):
        col = 0
        i = 1
        for line in self.data:
            column_name = line[0]
            base_column = column_name + ', '
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

    @staticmethod
    def save(path, content):
        parent_dir = os.path.split(path)[0]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        with open(path, 'w+', encoding='utf-8')as f:
            f.write(content)
            print(f'{OUTPUT_PREFIX}{path}')

    def main(self):
        self.generate_java()
        self.generate_mapper()
        self.generate_xml()

