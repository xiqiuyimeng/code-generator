# -*- coding: utf-8 -*-
from service.system_storage.data_type import get_data_type
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfo, ColTypeEnum

_author_ = 'luwt'
_date_ = '2023/1/13 12:33'


def assemble_col_info(name, value):
    col_info = DsTableColInfo(init=True)
    col_info.col_name = name
    # 获取变量值的数据类型映射值
    data_type = get_data_type(value)
    col_info.data_type = data_type
    col_info.full_data_type = data_type
    return col_info


# ---------------------------------------- 解析json结构体 start ---------------------------------------- #

def parse_json(obj_dict: dict):
    col_list = list()
    for name, value in obj_dict.items():
        col_info = assemble_col_info(name, value)
        col_list.append(col_info)
        # 如果是字典，那么继续解析，当前列类型为对象
        if isinstance(value, dict):
            col_info.col_type = ColTypeEnum.obj.value
            col_info.children = parse_json(value)
            # 在子元素中维护一个父元素的指针
            for child in col_info.children:
                child.parent_col = col_info
        elif isinstance(value, list):
            parse_json_array(value, col_info)
        else:
            # 基本数据类型，结束
            col_info.col_type = ColTypeEnum.col.value
    return col_list


def parse_json_array(value_list, col_info):
    # 对于list，只需要取第一个元素即可获取类型
    value_obj = value_list[0]
    # 将当前列类型，置为数组
    col_info.col_type = ColTypeEnum.array.value
    # 根据第一个元素的类型，决定整个数组的数据类型
    col_info.data_type = col_info.data_type.format(get_data_type(value_obj))
    col_info.full_data_type = col_info.full_data_type.format(get_data_type(value_obj))
    # 如果数组下元素为字典，那么继续解析
    if isinstance(value_obj, dict):
        # 只有在字典类型的时候，才指定子元素列表
        col_info.children = parse_json(value_obj)
        # 在子元素中维护一个父元素的指针
        for child in col_info.children:
            child.parent_col = col_info
    elif isinstance(value_obj, list):
        # 如果是list类型，继续解析，对于列表类型，那么无需指定子元素列表，
        # 因为对于json来说，只有k v结构，才应被当做一条列信息对待，
        # 而列表本身，应被作为一条数组类型的列来看待
        parse_json_array(value_obj, col_info)
    else:
        # 如果数组元素为基本数据类型，那么结束，最终的数据类型应类似于：string []
        pass

# ---------------------------------------- 解析json结构体 end ---------------------------------------- #
