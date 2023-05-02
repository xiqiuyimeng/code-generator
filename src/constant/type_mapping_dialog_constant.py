# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/2/24 16:42'


# 数据源列类型
DS_COL_TYPE_LIST_TITLE = '数据源列类型列表'
ADD_DS_COL_TYPE_BUTTON_TEXT = '添加数据源列类型'
ADD_DS_COL_TYPE_TITLE = '添加数据源列类型'

DS_COL_TYPE_LIST_BOX_TITLE = '读取数据源列类型列表'
ADD_COL_TYPE_LIST_TITLE = '保存数据源列类型列表'

SAVE_DATA_TIPS = '温馨提示：在页面操作后，请点击 [保存] 按钮保存修改内容后退出。'

# 类型映射表格页
TYPE_MAPPING_LIST_TITLE = '类型映射列表'
DS_COL_TYPE_BUTTON_TEXT = '数据源列类型'
ADD_TYPE_MAPPING_BUTTON_TEXT = '添加类型映射'
TYPE_MAPPING_BOX_TITLE = '读取类型映射列表'
ADD_TYPE_MAPPING_BOX_TITLE = '添加类型映射'
EDIT_TYPE_MAPPING_BOX_TITLE = '编辑类型映射'
DEL_TYPE_MAPPING_BUTTON_TEXT = '删除类型映射'
DEL_TYPE_MAPPING_BOX_TITLE = '删除类型映射'
DEL_TYPE_MAPPING_PROMPT = '类型映射：{}\n确认删除类型映射吗？'
BATCH_DEL_TYPE_MAPPING_PROMPT = '已选择{}个类型映射\n确认删除选中的类型映射吗？'
IMPORT_TYPE_MAPPING_BTN_TEXT = '导入类型映射'
EXPORT_TYPE_MAPPING_BTN_TEXT = '导出类型映射'

# 类型映射详情页
TYPE_MAPPING_TITLE = '类型映射信息'
READ_TYPE_MAPPING_BOX_TITLE = '读取类型映射信息'
TYPE_MAPPING_INFO_TEXT = '基本信息'
TYPE_MAPPING_COL_TABLE_TEXT = '列类型映射'
TYPE_MAPPING_NAME = '类型映射名称：'
DS_TYPE_TEXT = '数据源类型：'
TYPE_MAPPING_COMMENT_TEXT = '备\t\b\b注：'

# 同步数据源列类型按钮
SYNC_DS_COL_TYPE_BTN_TEXT = '同步当前数据源列类型'
# 添加列类型映射按钮
ADD_COL_TYPE_MAPPING_BTN_TEXT = '添加列类型映射'
# 删除列类型映射按钮
DEL_COL_TYPE_MAPPING_BTN_TEXT = '删除列类型映射'

# 添加列类型映射组按钮
ADD_MAPPING_GROUP_BTN_TEXT = '添加列类型映射组'
# 删除列类型映射组按钮
DEL_MAPPING_GROUP_BTN_TEXT = '删除列类型映射组'

# 获取数据源类型
GET_DS_TYPE_TITLE = '获取数据源类型'
# 没有选择数据源类型提示语
NO_DS_TYPE_PROMPT = f'数据源类型为空！\n\t请到 [{TYPE_MAPPING_INFO_TEXT}] -> [{DS_TYPE_TEXT.split("：")[0]}] ' \
                    f'中选择一种数据源类型'
# 获取数据源列类型
GET_COL_TYPES_TITLE = '获取数据源列类型'
# 根据数据源类型获取不到列类型，提示维护数据，或手动添加列类型
NO_COL_TYPES_PROMPT = f'根据数据源类型 [{0}]，获取列类型为空！\n\t请退出对话框，到 [{DS_COL_TYPE_BUTTON_TEXT}] ' \
                      f' -> [{ADD_DS_COL_TYPE_BUTTON_TEXT}] 中维护列类型数据；\t\n或者在当前表格中，' \
                      f'[{ADD_COL_TYPE_MAPPING_BTN_TEXT}] 手动添加列类型数据'

# 检查列类型映射表中未完成数据的提示
CHECK_COL_TYPE_MAPPING_FRAGMENTARY_TITLE = '列类型映射表数据检查'
CHECK_COL_TYPE_MAPPING_FRAGMENTARY_PROMPT = '输入不完整，以下列中存在空值，请完成输入！\n\n{}'
