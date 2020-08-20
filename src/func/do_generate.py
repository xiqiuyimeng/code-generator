# -*- coding: utf-8 -*-
from src.func.connection_function import open_connection
from src.constant.constant import SPRING_TAB_TITLE, MYBATIS_TAB_TITLE
from src.generator.mybatis_generator import MybatisGenerator
from src.generator.spring_generator import SpringGenerator
from src.sys.sys_info_storage.sqlite import get_id_by_name

_author_ = 'luwt'
_date_ = '2020/7/15 14:25'


def get_params(gui, selected_data):
    """
    拼接生成器需要的参数。数据库游标，数据库名称，表名称，列名列表（如果是部分选择字段的话）
    :param gui:
    :param selected_data:
    """
    selected_parted_table = 0
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
                    selected_parted_table += 1
                params.append(current_param_dict)
    return params, selected_parted_table


def get_file_counts(params, generator_type):
    # 总表数
    all_file = 0
    all_tbs = len(params[0])
    # 部分选择字段的表数
    parted_tbs = params[1]
    # 整表数
    full_tbs = all_tbs - parted_tbs
    # 部分字段表将只生成xml和model
    parted_tbs_files = parted_tbs * 2
    # 整表：如果是spring生成器，将生成controller service serviceImpl mapper model xml
    if SPRING_TAB_TITLE == generator_type:
        all_file = parted_tbs_files + full_tbs * 6
    # 如果是mybatis生成器，将生成mapper model xml
    elif MYBATIS_TAB_TITLE == generator_type:
        all_file = parted_tbs_files + full_tbs * 3
    return all_file


def mybatis_generate(param_dict, params, file_count, consumer):
    count = 0
    for param in params:
        param.update(param_dict)
        generator = MybatisGenerator(**param)
        count = generator.main(count, file_count, consumer)


def spring_generate(spring_param_dict, params, file_count, consumer):
    count = 0
    for param in params:
        param.update(spring_param_dict)
        generator = SpringGenerator(**param)
        count = generator.main(count, file_count, consumer)


def dispatch_generate(gui, param_dict, selected_data, consumer):
    params = get_params(gui, selected_data)
    # spring生成器
    if 'service_package' in param_dict \
            and 'service_impl_package' in param_dict \
            and 'controller_package' in param_dict:
        file_count = get_file_counts(params, SPRING_TAB_TITLE)
        spring_generate(param_dict, params[0], file_count, consumer)
    else:
        file_count = get_file_counts(params, MYBATIS_TAB_TITLE)
        mybatis_generate(param_dict, params[0], file_count, consumer)
