# -*- coding: utf-8 -*-
from mysql_generator import mysql_type as mt
from jinja2 import Environment, FileSystemLoader
from xml.etree import cElementTree
import os
import pymysql
import time
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
        self.comment = comment


def get_native_define_conn(host, port, user, pwd, db):
    """打开本地数据库连接（ip/数据库用户名/登录密码/数据库名/编码）"""
    try:
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=pwd,
            db=db,
            charset='utf8'
        )
        print("获取数据库连接成功")
        return conn
    except Exception as e:
        print(e)
        raise e


class MybatisGenerator:
    """
    默认生成lombok的@Data注释，可配置生成getter和setter方法，如果生成getter和setter则不会生成@Data，
    可以配置生成多表字段联合的java类和resultMap，也可以指定某表的某些字段
        参数：

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
            输出路径，默认为'./'当前目录下，可修改
        `lombok`
            在生成java类时是否生成lombok的@Data注释，默认true，若配置为false则生成getter和setter方法
        `exec_sql`
            可执行的sql查询语句，用于多表联合查询情况，默认None，开启后将会生成相应的java类和xml，不会生成mapper.java，
            xml中只会生成resultMap
    """
    def __init__(self, table_schema, table_name, column_name=None, java_tp='java.txt',
                 mapper_tp='mapper.txt', xml_tp='xml.txt', path='./', lombok=True,
                 exec_sql=None):
        # 库名
        self.table_schema = table_schema
        # 表名
        self.table_name = table_name
        # 可选：字段名，字符串形式，逗号分隔
        self.column_name = column_name
        # 查询结果为字段名，类型，约束（判断是否为主键PRI即可，应用在按主键查询更新删除等操作），自定义sql提供完整查询字段即可
        self.sql = 'select column_name, data_type, column_key, column_comment from information_schema.columns ' \
                   'where table_schema = "{}" and table_name = "{}"'.format(self.table_schema, self.table_name)\
            if exec_sql is None else 'show full fields from tmp_table'
        self.exec_sql = exec_sql
        self.data = self.get_data()
        self.primary = list(filter(lambda k: k[2] == 'PRI', self.data))
        self.java_tp = java_tp
        self.mapper_tp = mapper_tp
        self.xml_tp = xml_tp
        self.lombok = lombok
        self.appointed_columns = True if self.column_name else False
        self.mapper = True if not self.exec_sql and not self.appointed_columns else False
        # 获取模板文件
        self.env = Environment(loader=FileSystemLoader('./'), lstrip_blocks=True, trim_blocks=True)
        self.java_path = os.path.join(path, self.deal_class_name() + '.java')
        self.xml_path = os.path.join(path, self.deal_class_name() + 'Mapper.xml')
        # 如果是任意字段组合（主要用于多表字段联合情况），不需要生成Mapper.java
        self.mapper_path = os.path.join(path, self.deal_class_name() + 'Mapper.java') \
            if self.mapper else None

    def get_data(self):
        """连接数据库获取数据"""
        conn = get_native_define_conn(host, int(port), user, pwd, db)
        cursor = conn.cursor()
        if self.column_name and not self.exec_sql:
            columns = self.column_name.split(',')
            for i, c in enumerate(columns):
                if i == 0:
                    self.sql += ' and column_name in ("' + c + '"'
                else:
                    self.sql += ',"' + c + '"'
            self.sql += ')'
        if self.exec_sql:
            cursor.execute('use {};'.format(self.table_schema))
            cursor.execute('create temporary table tmp_table {};'.format(self.exec_sql))
        cursor.execute(self.sql)
        data = list(cursor.fetchall())
        if self.exec_sql:
            for line in data:
                ix = data.index(line)
                line = list(line)
                if line[1].find('(') > 0:
                    type_ = line[1][0: line[1].find('(')]
                    line[1] = type_
                data[ix] = line
        cursor.close()
        conn.close()
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
        """返回jdbcType和java_type"""
        return eval('mt.MysqlType.{}.value[0]'.format(data)), eval('mt.MysqlType.{}.value[1]'.format(data))

    def generate_java(self):
        java_list = []
        for line in self.data:
            name = self.deal_column_name(line[0])
            types = self.deal_type(line[1])
            data = Data(name, line[0], types[1], types[0], line[-1])
            java_list.append(data)
        content = self.env.get_template(self.java_tp).render(
            cls_name=self.deal_class_name(), java_list=java_list, lombok=self.lombok)
        self.save(self.java_path, content)

    def generate_mapper(self):
        if self.mapper:
            cls_name = self.deal_class_name()
            # 多个主键的情况，mapper里的delete和select都应传入类，否则传主键
            param = ''
            key = ''
            have_update = True
            if len(self.primary) == len(self.data):
                have_update = False
            if len(self.primary) > 1:
                param = cls_name
                key = cls_name.lower()
            elif len(self.primary) == 1:
                param = self.deal_type(self.primary[0][1])[1]
                key = self.deal_column_name(self.primary[0][0])
            content = self.env.get_template(self.mapper_tp).render(
                cls_name=cls_name, param=param, key=key, haveUpdate=have_update)
            self.save(self.mapper_path, content)

    def generate_xml(self):
        # resultMap
        result_map = []
        # base_column_list
        columns = []
        params = []
        java_type = ''
        need_update = True
        # 生成base_column_list
        self.generate_base_col(columns)
        for line in self.data:
            column_name = line[0]
            name = self.deal_column_name(line[0])
            jdbc_type = self.deal_type(line[1])[0]
            java_type = self.deal_type(line[1])[0]
            data = Data(name, column_name, jdbc_type=jdbc_type, java_type=java_type)
            result_map.append(data)
        if len(self.primary) > 1:
            java_type = self.deal_class_name()
        elif len(self.primary) == 1:
            java_type = self.deal_type(self.primary[0][1])[1]
        if len(self.data) == len(self.primary):
            need_update = False
        for primary in self.primary:
            params.append(Data(self.deal_column_name(primary[0]), primary[0],
                               self.deal_type(primary[1])[1], self.deal_type(primary[1])[0]))
        update_columns = result_map[:]
        for param in params:
            for result in update_columns:
                if param.column_name == result.column_name:
                    update_columns.remove(result)
                    continue
        content = self.env.get_template(self.xml_tp).render(
            result_map=result_map, columns=columns, table_name=self.table_name,
            params=params, java_type=java_type, need_update=need_update,
            update_columns=update_columns, mapper=self.mapper, any_column=self.exec_sql
        )
        self.save(self.xml_path, content)

    @staticmethod
    def save(path, content):
        with open(path, 'w+', encoding='utf-8')as f:
            f.write(content)
            print('生成的文件为' + path)

    def main(self):
        self.generate_java()
        self.generate_mapper()
        self.generate_xml()

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


if __name__ == '__main__':
    try:
        tree = cElementTree.parse(os.path.join(os.path.abspath('.'), 'config.xml'))
        root = tree.getroot()
        host = root.find('database').find('host').text
        port = root.find('database').find('port').text
        user = root.find('database').find('user').text
        pwd = root.find('database').find('pwd').text
        db = root.find('database').find('db').text
        table_schema = root.find('generator').find('table_schema').text
        table_name = root.find('generator').find('table_name').text
        column = root.find('generator').find('column').text
        path = root.find('generator').find('path').text
        lombok = root.find('generator').find('lombok').text
        exec_sql = root.find('generator').find('exec_sql').text

        generator = MybatisGenerator(table_schema, table_name, column, path=path, lombok=lombok, exec_sql=exec_sql)
        generator.main()
        print("执行成功！五秒后退出")
        time.sleep(5)
    except Exception as e:
        print("执行出错：=>\n\n{}\n\n按任意键退出".format(e))
        input()
