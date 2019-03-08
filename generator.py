# -*- coding: utf-8 -*-
from mysql_generator import mysql_type as mt
from db_opt import getcursor
import os
_author_ = 'luwt'
_date_ = '2019/1/23 11:33'


class MysqlGenerator:

    def __init__(self, table_name, path, mapper=True, column_name=None, select_delete=True):
        self.table_name = table_name
        self.java_path = os.path.join(path, self.deal_class_name() + '.java')
        self.xml_path = os.path.join(path, self.deal_class_name() + 'Mapper.xml')
        self.mapper_path = os.path.join(path, self.deal_class_name() + 'Mapper.java')
        self.column_name = column_name
        # 主键信息
        self.primary = []
        self.data = None
        self.result_xml = '<?xml version="1.0" encoding="UTF-8" ?>\n'\
                          '<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" ' \
                          '"http://mybatis.org/dtd/mybatis-3-mapper.dtd" >' \
                          '\n<mapper namespace="待填写" >\n'
        self.result_map = '\t<resultMap id="BaseResultMap" type="实体类路径" >\n'
        self.base_column_list = '\t<sql id="Base_Column_List">\n\t\t'
        self.select_delete = select_delete
        self.insert = ['\n\t<insert id="insert" parameterType="实体类路径" >\n',
                       '\t\tinsert into \n\t\t{}('.format(self.table_name),
                       '\t\tvalues (']
        self.insert_selective = ['\t<insert id="insertSelective" parameterType="实体类路径" >',
                                 '\n\t\tinsert into \n\t\t{}\n\t\t'
                                 '<trim prefix="(" suffix=")" suffixOverrides="," >\n'.format(self.table_name),
                                 '\t\t<trim prefix="values (" suffix=")" suffixOverrides="," >\n']
        self.update = '\t<update id="updateByPrimaryKey" parameterType="实体类路径">\n' \
                      '\t\tupdate {} set\n'.format(self.table_name)
        self.update_selective = '\t<update id="updateByPrimaryKeySelective" parameterType="实体类路径">\n' \
                                '\t\tupdate {}\n' \
                                '\t\t<set>\n'.format(self.table_name)
        self.result = '%spublic class %s{\n\n' % ('\n\n@Data\n', self.deal_class_name())
        self.mapper = mapper

    def get_data(self):
        """连接数据库获取数据"""
        get_cursor = getcursor.GetCursor()
        conn = get_cursor.get_native_conn()
        cursor = conn.cursor()
        # 查询结果为字段名，类型，约束（判断是否为主键PRI即可，应用在按主键查询更新删除等操作）
        sql = 'select column_name, data_type, column_key from information_schema.columns ' \
              'where table_schema = "xy_db" and table_name = "{}"'.format(self.table_name)
        if self.column_name:
            sql += 'and column_name in ({})'.format(self.column_name)
        cursor.execute(sql)
        self.data = cursor.fetchall()

    def deal_class_name(self):
        class_name = ''
        for name in self.table_name.split('_'):
            class_name += name.capitalize()
        return class_name

    def generate_java(self, data, end=False):
        column_type = eval('mt.MysqlType.{}.value[1]'.format(data[1]))
        self.result += '\tprivate {} {};\n\n'.format(column_type, self.deal_column_name(data[0]))
        if end:
            self.result += '}'

    def generate_mapper(self):
        mapper = 'public interface %sMapper {\n\n' \
                 '\t%s selectByPrimaryKey(%s %s);\n\n' \
                 '\tint deleteByPrimaryKey(%s %s);\n\n' \
                 '\tint insert(%s record);\n\n' \
                 '\tint insertSelective(%s record);\n\n' \
                 '\tint updateByPrimaryKey(%s record);\n\n' \
                 '\tint updateByPrimaryKeySelective(%s record);\n\n}' \
                 % (self.deal_class_name(), self.deal_class_name(),
                    self.get_key_type()[1], self.get_key_type()[0],
                    self.get_key_type()[1], self.get_key_type()[0],
                    self.deal_class_name(), self.deal_class_name(),
                    self.deal_class_name(), self.deal_class_name())
        return mapper

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
        return eval('mt.MysqlType.{}.value[0]'.format(data[1])), eval('mt.MysqlType.{}.value[1]'.format(data[1]))

    def generate_result_map(self, data, end=False):
        self.result_map += '\t\t<result column="{}" property="{}" jdbcType="{}"/>\n'\
            .format(data[0], self.deal_column_name(data[0]), self.deal_type(data)[0])
        if end:
            self.result_map += '\t</resultMap>\n'

    def generate_base_column_list(self, data, end=False):
        if end:
            self.base_column_list += data[0]
            self.base_column_list += '\n\t</sql>'
        else:
            self.base_column_list += '{}, '.format(data[0])

    def get_key_type(self):
        """返回key和对应的java类型"""
        key = '未找到主键'
        key_type = '未找到主键'
        if len(self.primary) == 1:
            key = self.primary[0][0]
            key_type = self.deal_type(self.primary[0])[1]
        elif len(self.primary) > 1:
            key = 'record'
            key_type = self.deal_class_name()
        return key, key_type

    def generate_select_delete(self):
        result = '\n\t<select id="selectByPrimaryKey" resultMap="BaseResultMap" parameterType="{}">\n' \
                 '\t\tselect\n' \
                 '\t\t<include refid="Base_Column_List" />\n' \
                 '\t\tfrom {}{}</select>'.format(self.get_key_type()[1], self.table_name, self.deal_where_clause())
        result += '\n\t<delete id="deleteByPrimaryKey" parameterType="{}">\n' \
                  '\t\tdelete from {}{}</delete>'.format(self.get_key_type()[1], self.table_name, self.deal_where_clause())
        return result

    def generate_insert(self, data, end=False):
        key_tail = ', '
        value_tail = ', '
        # 根据是否是末尾，处理尾部拼接字符
        if end:
            key_tail = ')\n'
            value_tail = ')\n\t</insert>\n'
        self.insert[1] += '{}{}'.format(data[0], key_tail)
        self.insert[2] += '#{%s,jdbcType=%s}%s' % (self.deal_column_name(data[0]),
                                                   self.deal_type(data)[0], value_tail)

    def generate_insert_selective(self, data, end=False):
        self.insert_selective[1] += '\t\t\t<if test="{} != null" >\n\t\t\t\t{},\n\t\t\t</if>\n'\
            .format(self.deal_column_name(data[0]), data[0])
        self.insert_selective[2] += '\t\t\t<if test="%s != null" >\n\t\t\t\t#{%s,jdbcType=%s},\n\t\t\t</if>\n' \
                                    % (self.deal_column_name(data[0]), self.deal_column_name(data[0]),
                                       self.deal_type(data)[0])
        if end:
            self.insert_selective[1] += '\t\t</trim>\n'
            self.insert_selective[2] += '\t\t</trim>\n\t</insert>\n'

    def deal_where_clause(self):
        # 此处需要考虑有多个主键的情况，应该用and连接，作为where条件，生成更新时应该只生成非主键的key
        where_clause = []
        str_where = '未找到主键，请检查表结构并再次运行程序或手动添加where条件\n\t'
        if len(self.primary) >= 1:
            for key in self.primary:
                where_clause.append('%s = #{%s,jdbcType=%s}\n\t' %
                                    (key[0], self.deal_column_name(key[0]), self.deal_type(key)[0]))
            str_where = '\tand\t'.join(where_clause)
        tail = '\n\t\twhere %s' % str_where
        return tail

    def generate_update(self, data, end=False):
        tail = ',\n'
        if end:
            tail = self.deal_where_clause() + '</update>\n'
        if data[2] != 'PRI':
            self.update += '\t\t\t%s = #{%s,jdbcType=%s}%s' % \
                           (data[0], self.deal_column_name(data[0]), self.deal_type(data)[0], tail)

    def generate_update_selective(self, data, end=False):
        tail = '\n'
        if end:
            tail = '\n\t\t</set>' + self.deal_where_clause() + '</update>\n'
        if data[2] != 'PRI':
            self.update_selective += '\t\t\t<if test="%s != null">\n' \
                                     '\t\t\t\t%s = #{%s,jdbcType=%s},\n' \
                                     '\t\t\t</if>%s' \
                                     % (self.deal_column_name(data[0]), data[0],
                                        self.deal_column_name(data[0]), self.deal_type(data)[0], tail)

    def main(self):
        self.get_data()
        # 将主键放在primary里备用
        self.primary = list(filter(lambda k: k[2] == 'PRI', self.data))
        end = False
        for data in self.data:
            if self.data[-1] == data:
                end = True
            self.generate_java(data, end)
            self.generate_result_map(data, end)
            self.generate_base_column_list(data, end)
            self.generate_insert(data, end)
            self.generate_insert_selective(data, end)
            if len(self.data) != len(self.primary):
                self.generate_update(data, end)
                self.generate_update_selective(data, end)
        select_and_delete = ''
        update = ''
        if len(self.data) != len(self.primary):
            update = self.update + self.update_selective
        if self.select_delete:
            select_and_delete = self.generate_select_delete()
        self.result_xml += \
            self.result_map + self.base_column_list + select_and_delete + \
            " ".join(self.insert) + " ".join(self.insert_selective) + \
            update + '</mapper>'
        self.save(self.java_path, self.result)
        self.save(self.xml_path, self.result_xml)
        if self.mapper:
            mapper = self.generate_mapper()
            self.save(self.mapper_path, mapper)

    @staticmethod
    def save(path, content):
        with open(path, 'w', encoding='utf-8')as f:
            for line in content:
                f.writelines(line)


if __name__ == '__main__':
    column_ = '"sf_account", "sf_pwd", "sf_is_active"'
    table = 'uw_company'
    table_double = 'activity_category_ref'
    table_en = 'user_role'
    generator = MysqlGenerator(table_name=table, path="D:\\", mapper=False)
    generator.main()
