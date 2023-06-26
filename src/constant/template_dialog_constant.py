# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/3/9 9:38'


# 模板列表对话框标题
TEMPLATE_LIST_TITLE = '模板列表'
TEMPLATE_LIST_BOX_TITLE = '模板列表'

ADD_TEMPLATE_BTN_TEXT = '添加模板'
DEL_TEMPLATE_BTN_TEXT = '删除模板'
COPY_TEMPLATE_BTN_TEXT = '复制模板'
IMPORT_TEMPLATE_BTN_TEXT = '导入模板'
EXPORT_TEMPLATE_BTN_TEXT = '导出模板'

# 复制模板消息对话框标题
COPY_TEMPLATE_BOX_TITLE = '复制模板'

# 删除模板消息对话框标题
DEL_TEMPLATE_BOX_TITLE = '删除模板'
DEL_TEMPLATE_PROMPT = '模板：{}\n确认删除模板吗？'
BATCH_TEMPLATE_PROMPT = '已选择{}个模板\n确认删除选中的模板吗？'

# 模板详细信息
CREATE_TEMPLATE_TITLE = '添加模板'
EDIT_TEMPLATE_TITLE = '编辑模板'
READ_TEMPLATE_BOX_TITLE = '读取模板详细信息'
ADD_TEMPLATE_BOX_TITLE = '添加模板'
EDIT_TEMPLATE_BOX_TITLE = '编辑模板'

# 模板详情页左侧列表项
TEMPLATE_INFO_TEXT = '基本信息'
TEMPLATE_CONFIG_TEXT = '模板配置'
TEMPLATE_FILE_TEXT = '模板文件'
TEMPLATE_FUNC_TEXT = '模板方法'

# 模板详情页
TEMPLATE_NAME = '模板名称：'
TEMPLATE_DESC = '模板说明：'

# 模板配置页
TEMPLATE_OUTPUT_DIR_TAB_TEXT = '模板输出路径配置详情'
TEMPLATE_VAR_CONFIG_TAB_TEXT = '模板变量配置详情'
# 按钮
ADD_CONFIG_BTN_TEXT = '添加配置项'
REMOVE_CONFIG_BTN_TEXT = '移除配置项'
PREVIEW_CONFIG_BTN_TEXT = '预览模板配置页'
AUTO_GENERATE_OUTPUT_CONFIG_BTN_TEXT = '生成文件输出路径配置'
MAINTAIN_FILE_CONFIG_BTN_TEXT = '维护文件输出路径'

PREVIEW_VAR_CONFIG_TITLE = '模板变量配置页预览'
PREVIEW_OUTPUT_CONFIG_TITLE = '模板输出路径配置页预览'
NO_TEMPLATE_CONFIG_ITEMS_TEXT = '暂未维护模板配置项'
TEMPLATE_VAR_CONFIG_HEADER_LABELS = ['配置项名称', '输出变量名', '控件类型', '是否必填', '说明']
TEMPLATE_OUTPUT_CONFIG_HEADER_LABELS = ['配置项名称', '输出变量名', '控件类型', '是否必填', '关联模板文件', '说明']
TEMPLATE_CONFIG_LIST_BOX_TITLE = '模板配置列表'

# 模板配置详情页
CREATE_OUTPUT_CONFIG_TITLE = '添加模板输出路径配置'
EDIT_OUTPUT_CONFIG_TITLE = '编辑模板输出路径配置'
CREATE_VAR_CONFIG_TITLE = '添加模板变量配置'
EDIT_VAR_CONFIG_TITLE = '编辑模板变量配置'

# 控件类型
CONFIG_INPUT_WIDGET_TYPE_DICT = {
    '文本输入框 + 文件夹对话框': 'LineEditFileDialogConfigValueWidget',
    '文本输入框': 'LineEditConfigValueWidget',
    '文本编辑区': 'TextEditorConfigValueWidget',
    '下拉框列表': 'ComboBoxConfigValueWidget',
    '文件夹对话框': 'FileDialogConfigValueWidget',
}
DEFAULT_INPUT_WIDGET_TYPE = tuple(CONFIG_INPUT_WIDGET_TYPE_DICT)[0]
DEL_CONFIG_BOX_TITLE = '删除配置项'
DEL_CONFIG_PROMPT = '配置项：{}\n确认删除配置项吗？'
BATCH_DEL_CONFIG_PROMPT = '已选择{}个配置项\n确认删除选中的配置项吗？'
DEL_OUTPUT_CONFIG_PROMPT = '配置项：{}\n关联的模板文件已删除，是否同步删除配置项？'
BATCH_DEL_OUTPUT_CONFIG_PROMPT = '配置项关联的模板文件已删除\n是否同步删除配置项？'

CONFIG_NAME_TEXT = '配置项名称：'
VAR_NAME_TEXT = '输出变量名称：'

VAR_NAME_PLACEHOLDER_TEXT = '变量名称最多可输入50字符，须符合变量命名规则，以下划线或大小写字母开头'
VAR_NAME_REG_RULE = r'[_a-zA-Z]\w*'

WIDGET_LABEL_TEXT = '配置项控件：'
CONFIG_DESC_TEXT = '配置项说明：'
DEFAULT_VALUE_TEXT = '默认值：'
PLACEHOLDER_TEXT = '占位文本：'
VALUE_RANGE_TEXT = '值列表：'
IS_REQUIRED_TEXT = '是否必填：'
ADD_VALUE_BTN_TEXT = '添加值'

ADD_RANGE_VALUE_BOX_TITLE = '添加下拉列表值'

OPEN_FILE_DIALOG_BUTTON_TXT = '请选择文件夹'
SELECT_DIRECTORY_TITLE = '选择文件夹'

NOT_FILL_ALL_REQUIRED_INPUT_TXT = '还有未完成的必填项，请完成所有必填项'
REQUIRED_CHECK_BOX_TITLE = '必填项检查'

# 模板配置类型枚举值
OUTPUT_DIR_TXT = '输出路径'
TEMPLATE_VAR_TXT = '模板变量'

# 输出路径，关联文件，气泡提示
UNBIND_FILE_TOOL_TIP = '暂未关联模板文件！'

# 没有未关联配置的文件提示
NO_UNBIND_FILE_PROMPT = '未发现需要生成输出路径配置的模板文件！'
GENERATE_FILE_CONFIG_TITLE = '生成文件的输出路径配置'
GENERATE_CONFIG_FAIL_PROMPT = '以下文件未能自动生成输出路径配置，请手动处理！\n\n{}'

MANAGE_FILE_CONFIG_TITLE = '管理文件的输出路径配置'

# 维护配置和文件关系对话框
MAINTAIN_FILE_CONFIG_BOX_TITLE = '维护输出路径配置和文件关系'
NO_OUTPUT_CONFIG_PROMPT = '暂无输出配置！\n请添加输出配置后再操作'

MAINTAIN_FILE_CONFIG_TITLE = '维护输出路径配置和文件关系'
OUTPUT_CONFIG_LIST_HEADER_TEXT = '输出路径配置列表'
FILE_LIST_HEADER_TEXT = '模板文件列表'

NO_TEMPLATE_PROMPT = '暂无模板，请先维护模板再进行生成'
NO_TEMPLATE_TITLE = '获取模板'

FILE_NAME_TEMPLATE_LABEL_TEXT = '文件名模板：'

CHECK_TEMPLATE_FILE_TITLE = '检查模板文件'
CHECK_TEMPLATE_FILE_PROMPT = '您还未添加模板文件，当前模板将无法在生成代码时使用，确认保存吗？'
CHECK_TP_FILE_CONFIG_TITLE = '检查模板文件关联输出路径配置'
CHECK_TP_FILE_CONFIG_PROMPT = '当前模板存在模板文件还未绑定输出路径配置，当前模板将无法在生成代码时使用，确认保存吗？'
CHECK_FILE_NAME_TP_TITLE = '检查模板文件名称模板'
CHECK_FILE_NAME_TP_PROMPT = '当前模板存在模板文件还未设置文件名称模板，在生成代码时，无法根据数据表名生成文件名，确认保存吗？'

CHECK_OUTPUT_CONFIG_NAME_TITLE = '检查模板输出配置名称'
CHECK_OUTPUT_CONFIG_NAME_PROMPT = '模板输出配置，配置项名称存在空值或重复项，请打开输出配置详情页，进行数据修正'
CHECK_OUTPUT_CONFIG_VAR_NAME_TITLE = '检查模板输出配置变量名称'
CHECK_OUTPUT_CONFIG_VAR_NAME_PROMPT = '模板输出配置，输出变量名称存在空值或重复项，请打开输出配置详情页，进行数据修正'
CHECK_VAR_CONFIG_NAME_TITLE = '检查模板变量配置名称'
CHECK_VAR_CONFIG_NAME_PROMPT = '模板变量配置，配置项名称存在空值或重复项，请打开变量配置详情页，进行数据修正'
CHECK_VAR_CONFIG_VAR_NAME_TITLE = '检查模板变量配置变量名称'
CHECK_VAR_CONFIG_VAR_NAME_PROMPT = '模板变量配置，输出变量名称存在空值或重复项，请打开变量配置详情页，进行数据修正'

# 模板文件页
CREATE_FILE_TITLE = '新建模板文件'
ADD_FILE_BTN_TEXT = '新建模板文件'
LOCATE_FILE_BTN_TEXT = '定位'

# 模板方法页
SELECT_ALL_BTN_TEXT = '全选'
UNSELECT_BTN_TEXT = '取消全选'
COPY_OTHER_TP_FUNC_BTN_TEXT = '从其他模板复制方法'
CREATE_NEW_FUNC_BTN_TEXT = '创建方法'
CREATE_NEW_FUNC_TITLE = '创建方法'
DEL_FUNC_BTN_TEXT = '删除方法'
# 模板方法对话框
TEMPLATE_FUNC_NAME_PLACEHOLDER_TEXT = '方法名将自动根据方法体解析，不可重复'

# 模板方法复制对话框
HAS_FUNC_TEMPLATE_LIST_TITLE = '拥有模板方法的模板列表'
HAS_FUNC_TEMPLATE_LIST_BOX_TITLE = '读取拥有模板方法的模板列表'
TEMPLATE_FUNC_TITLE = '{} 模板方法列表'
TEMPLATE_FUNC_BOX_TITLE = '读取 {}'
# 按钮
SELECT_ALL_FUNC_BTN_TEXT = '全选'
UNSELECT_ALL_FUNC_BTN_TEXT = '取消选择'
COPY_FUNC_BTN_TEXT = '复制方法'
BACK_TO_TEMPLATE_BTN_TEXT = '返回模板列表'
# 消息框
COPY_FUNC_BOX_TITLE = '复制模板方法'
COPY_FUNC_DUPLICATE_PROMPT = '以下模板方法已经存在，是否覆盖？\n    {}'
COPY_FUNC_SUCCESS_BOX_TITLE = '复制模板方法成功'
COPY_FUNC_SUCCESS_PROMPT = '复制模板方法成功，此次共复制 {} 个模板方法！'
