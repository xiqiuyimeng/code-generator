# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/5/10 9:04'


EXPORT_SELECTED_DATA_LABEL_TEXT = '导出数据：'
EXPORT_SELECTED_DATA_DESC_TEXT = '已选中 {} 条数据'
EXPORT_OUTPUT_PATH_LABEL_TEXT = '导出路径：'
START_EXPORT_BTN_TEXT = '开始导出'

CHOOSE_IMPORT_FILE_TEXT = '请选择导入文件'
CHOOSE_EXPORT_DIR_TEXT = '请选择导出路径'
IMPORT_EXPORT_SELECT_FILE_ICON = '导入导出选择文件icon'

IMPORT_FILE_PROMPT = '拖入文件'
IMPORT_FILE_LABEL_TEXT = '导入文件：'
START_IMPORT_BTN_TEXT = '开始导入'

# 导入导出文件内的第一层key
TYPE_KEY = 'data_type'
DATA_KEY = 'data_list'

# 类型映射
IMPORT_TYPE_MAPPING_TITLE = '导入类型映射'
EXPORT_TYPE_MAPPING_TITLE = '导出类型映射'
TYPE_MAPPING_DATA_KEY = 'type_mapping'
EXPORT_TYPE_MAPPING_FILE_NAME = 'type_mapping.json'
PROCESS_DUPLICATE_TYPE_MAPPING_TITLE = '处理重复的类型映射数据'
PROCESS_ILLEGAL_TYPE_MAPPING_TITLE = '处理异常的类型映射数据'
OVERRIDE_TYPE_MAPPING_TITLE = '覆盖类型映射数据'

# 模板
IMPORT_TEMPLATE_TITLE = '导入模板'
EXPORT_TEMPLATE_TITLE = '导出模板'
TEMPLATE_DATA_KEY = 'template'
EXPORT_TEMPLATE_FILE_NAME = 'template.json'

# 模板方法
IMPORT_TEMPLATE_FUNC_TITLE = '导入模板方法'
EXPORT_TEMPLATE_FUNC_TITLE = '导出模板方法'
TEMPLATE_FUNC_DATA_KEY = 'template_function'
EXPORT_TEMPLATE_FUNC_FILE_NAME = 'template_func.json'

# 处理导入数据异常对话框
SELECT_ALL_BTN_TEXT = '全选'
UNSELECT_ALL_BTN_TEXT = '取消选择'
SKIP_DUPLICATE_BTN_TEXT = '跳过选中的重复数据'
PROCESS_DUPLICATE_BTN_TEXT = '覆盖数据库数据'

SKIP_ILLEGAL_BTN_TEXT = '跳过选中的异常数据'
PROCESS_ILLEGAL_BTN_TEXT = '手动处理数据'

MULTI_ILLEGAL_SELECTED_TITLE = '手动处理异常数据'
MULTI_ILLEGAL_SELECTED_PROMPT = '系统目前只支持一次处理一条异常数据，您选中的多条数据中，此次处理仅处理第一条，' \
                                '若需要处理其他数据，请在当前处理完成后，继续处理'
