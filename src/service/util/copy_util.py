# -*- coding: utf-8 -*-
import re
from dataclasses import fields

from src.service.system_storage.col_type_mapping_sqlite import ColTypeMapping
from src.service.system_storage.template_config_sqlite import TemplateConfig
from src.service.system_storage.template_file_sqlite import TemplateFile
from src.service.system_storage.template_sqlite import Template
from src.service.system_storage.type_mapping_sqlite import TypeMapping

_author_ = 'luwt'
_date_ = '2023/5/24 16:21'

COPY_NAME_SUFFIX = '-copy'
COPY_NAME_PATTERN = f'(.+{COPY_NAME_SUFFIX})(\\d*)$'


def generate_copy_name(exists_name_list, name_str, num_suffix=0):
    if num_suffix:
        copy_name = f'{name_str}{num_suffix}'
    else:
        copy_name = name_str
    # 判断是否存在，如果存在，继续递归处理
    if copy_name in exists_name_list:
        return generate_copy_name(exists_name_list, name_str, num_suffix + 1)
    return copy_name


def generate_unique_name(origin_name, exists_name_list):
    find_result = re.findall(COPY_NAME_PATTERN, origin_name)
    # 如果能匹配到，说明原有名称也是复制生成的，那么根据规则，取出数字编号，加1即可生成新的名称
    if find_result:
        copy_num = int(find_result[0][1]) if find_result[0][1] else 0
        unique_name = generate_copy_name(exists_name_list, find_result[0][0], copy_num + 1)
        # 判断名称是否已经存在，如果存在，继续递归处理
    else:
        # 如果原有名称不是复制生成的，那么添加后缀
        unique_name = generate_copy_name(exists_name_list, f'{origin_name}{COPY_NAME_SUFFIX}')
    # 生成成功后，放入已存在名称列表
    exists_name_list.append(unique_name)
    return unique_name


# ------------------------------ 复制类型映射 start ------------------------------ #


def copy_type_mapping_col(export_type_mapping_col):
    col_type_mapping = ColTypeMapping()
    for field in fields(export_type_mapping_col):
        setattr(col_type_mapping, field.name, getattr(export_type_mapping_col, field.name))
    return col_type_mapping


def copy_type_mapping(export_type_mapping, exists_name_list):
    type_mapping = TypeMapping()
    # 复制类型映射主体数据
    for field in fields(export_type_mapping):
        setattr(type_mapping, field.name, getattr(export_type_mapping, field.name))
    # 生成新的名称
    type_mapping.mapping_name = generate_unique_name(export_type_mapping.mapping_name, exists_name_list)
    # 复制类型映射列信息
    if export_type_mapping.type_mapping_cols:
        type_mapping.type_mapping_cols = [copy_type_mapping_col(type_mapping_col)
                                          for type_mapping_col in export_type_mapping.type_mapping_cols]
    return type_mapping


# ------------------------------ 复制类型映射 end ------------------------------ #


# ------------------------------ 复制模板 start ------------------------------ #


def copy_template_file(export_template_file):
    template_file = TemplateFile()
    for field in fields(export_template_file):
        setattr(template_file, field.name, getattr(export_template_file, field.name))
    return template_file


def copy_template_config(export_template_config: TemplateConfig):
    template_config = TemplateConfig()
    for field in fields(export_template_config):
        setattr(template_config, field.name, getattr(export_template_config, field.name))
    return template_config


def copy_template_output_config(export_output_config: TemplateConfig, template_file_dict):
    copy_config = copy_template_config(export_output_config)
    if export_output_config.bind_file_list:
        copy_config.bind_file_list = [template_file_dict.get(bind_file.file_name)
                                      for bind_file in export_output_config.bind_file_list]
    return copy_config


def copy_template(export_template, exists_name_list):
    template = Template()
    # 生成新的名称
    template.template_name = generate_unique_name(export_template.template_name, exists_name_list)
    template.template_desc = export_template.template_desc
    template_file_dict = dict()
    # 复制模板文件
    if export_template.template_files:
        template_file_list = list()
        for file in export_template.template_files:
            copy_file = copy_template_file(file)
            template_file_list.append(copy_file)
            # 将文件放入字典，名称为key，方便输出配置取值
            template_file_dict[file.file_name] = copy_file
        template.template_files = template_file_list
    # 复制模板配置
    if export_template.output_config_list:
        template.output_config_list = [copy_template_output_config(output_config, template_file_dict)
                                       for output_config in export_template.output_config_list]
    else:
        template.output_config_list = tuple()
    if export_template.var_config_list:
        template.var_config_list = [copy_template_config(var_config)
                                    for var_config in export_template.var_config_list]
    else:
        template.var_config_list = tuple()
    return template

# ------------------------------ 复制模板 end ------------------------------ #
