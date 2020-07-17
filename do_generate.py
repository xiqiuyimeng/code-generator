# -*- coding: utf-8 -*-
from connection_function import open_connection
from mybatis_generator import MybatisGenerator
from spring_generator import SpringGenerator
from sys_info_storage.sqlite import get_id_by_name

_author_ = 'luwt'
_date_ = '2020/7/15 14:25'


param_dict = {
    'lombok': False,
    'java_path': r'D:\java_workspaces\demo',
    'java_src_relative': 'src/main/java',
    'model_package': 'com.demo.model',
    'mapper_package': 'com.demo.dao',
    'xml_path': r'D:\java_workspaces\demo\src\main\resources\test',
}
spring_param_dict = {
    'service_package': 'com.demo.service',
    'service_impl_package': 'com.demo.service.impl',
    'controller_package': 'com.demo.controller'
}

spring_param_dict.update(param_dict)


def get_params(gui, selected_data):
    """
    拼接生成器需要的参数。数据库游标，数据库名称，表名称，列名列表（如果是部分选择字段的话）
    :param gui:
    :param selected_data:
    """
    params = list()
    for conn_name, db_dict in selected_data.items():
        conn_id = get_id_by_name(conn_name)
        cursor = open_connection(gui, conn_id, conn_name).cursor
        for db_name, tb_dict in db_dict.items():
            for tb_name, cols in tb_dict.items():
                current_param_dict = {
                    'cursor': cursor,
                    'table_schema': db_name,
                    'table_name': tb_name
                }
                if isinstance(cols, list):
                    current_param_dict['column_name'] = cols
                params.append(current_param_dict)
    return params


def mybatis_generate(gui, selected_data):
    params = get_params(gui, selected_data)
    for param in params:
        param.update(param_dict)
        generator = MybatisGenerator(**param)
        generator.main()


def spring_generate(gui, selected_data):
    params = get_params(gui, selected_data)
    for param in params:
        param.update(spring_param_dict)
        generator = SpringGenerator(**param)
        generator.main()
