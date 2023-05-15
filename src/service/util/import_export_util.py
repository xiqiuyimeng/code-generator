# -*- coding: utf-8 -*-
import dataclasses

_author_ = 'luwt'
_date_ = '2023/5/15 14:11'


def convert_import_to_model(import_model_class, model_class, data):
    # 之所以要经历两次转化，是为了规范数据，第一次先转化为导入导出使用的实体类，可保证与导出时数据结构相同，第二次转化为数据库实体类
    return model_class(**dataclasses.asdict(import_model_class().convert_import(**data)))


def convert_import_to_model_list(import_model_class, model_class, data_list):
    return [convert_import_to_model(import_model_class, model_class, data) for data in data_list]


def add_group_list(group_dict, get_group_key, data):
    key = get_group_key(data)
    data_group_list = group_dict.get(key)
    # 如果之前没存储过，那么创建list
    if data_group_list is None:
        data_group_list = list()
        group_dict[key] = data_group_list
    data_group_list.append(data)


def group_model_list(data_list, get_group_key):
    model_list_dict = dict()
    for data in data_list:
        add_group_list(model_list_dict, get_group_key, data)
    return model_list_dict


def check_repair_type_mapping_group_num(mapping_col_group_dict):
    for group_idx, group_num in enumerate(sorted(mapping_col_group_dict)):
        # 如果组号不对，更新组号
        if group_idx != group_num:
            error_group_list = mapping_col_group_dict.get(group_num)
            for group_col in error_group_list:
                group_col.group_num = group_idx
            # 将元素移动到 group_idx 组内
            if mapping_col_group_dict.get(group_idx) is None:
                mapping_col_group_dict[group_idx] = error_group_list
            else:
                mapping_col_group_dict[group_idx].extend(error_group_list)
            # 删除原有组
            del mapping_col_group_dict[group_num]
