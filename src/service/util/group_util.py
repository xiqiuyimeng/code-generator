# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/5/25 17:10'


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
