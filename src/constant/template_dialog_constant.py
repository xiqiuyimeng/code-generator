# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/3/9 9:38'


# 模板列表对话框标题
TEMPLATE_LIST_TITLE = '模板列表'
TEMPLATE_LIST_BOX_TITLE = '模板列表'

# 打开方法区对话框按钮
FUNC_DIALOG_BTN_TEXT = '模板常用方法'
ADD_TEMPLATE_BTN_TEXT = '添加模板'
DEL_TEMPLATE_BTN_TEXT = '删除模板'

# 模板常用方法对话框
TEMPLATE_FUNC_TITLE = '模板常用方法'

# 删除模板消息对话框标题
DEL_TEMPLATE_BOX_TITLE = '删除模板'
DEL_TEMPLATE_PROMPT = '模板：{}\n确认删除模板吗？'
BATCH_TEMPLATE_PROMPT = '已选择{}个模板\n确认删除选中的模板吗？'

# 模板详细信息
TEMPLATE_TITLE = '模板详细信息'
READ_TEMPLATE_BOX_TITLE = '读取模板详细信息'
ADD_TEMPLATE_BOX_TITLE = '添加模板'
EDIT_TEMPLATE_BOX_TITLE = '编辑模板'

# 模板详情页左侧列表项
TEMPLATE_INFO_TEXT = '基本信息'
TEMPLATE_FILE_TEXT = '模板文件'
TEMPLATE_CONFIG_TEXT = '模板配置'

# 模板详情页
TEMPLATE_NAME = '模板名称：'
TEMPLATE_DESC = '模板说明：'

# 模板文件页
CREATE_FILE_TITLE = '新建模板文件'
ADD_FILE_BTN_TEXT = '新建模板文件'
LOCATE_FILE_BTN_TEXT = '定位'

# 模板配置页
# 按钮
ADD_CONFIG_BTN_TEXT = '添加配置项'
REMOVE_CONFIG_BTN_TEXT = '移除配置项'
PREVIEW_CONFIG_BTN_TEXT = '预览模板配置页'
TEMPLATE_CONFIG_HEADER_LABELS = ['配置项名称', '输出变量名', '控件类型', '是否必填', '说明']

# 模板配置详情页
TEMPLATE_CONFIG_TITLE_TEXT = '模板配置详情'

# 控件类型
CONFIG_INPUT_WIDGET_TYPE_DICT = {
    '文本输入框': ('QLineEdit', 'from PyQt5.QtWidgets import QLineEdit'),
    '文本输入框 + 文件夹对话框': ('QLineEdit,QFileDialog', 'from PyQt5.QtWidgets import QLineEdit, QFileDialog'),
    '文本编辑区': ('TextEditor', 'from src.view.custom_widget.text_editor import TextEditor'),
    '下拉框列表': ('QComboBox', 'from PyQt5.QtWidgets import QComboBox'),
    '文件夹对话框': ('QFileDialog', 'from PyQt5.QtWidgets import QFileDialog'),
}
DEL_CONFIG_BOX_TITLE = '删除配置项'
DEL_CONFIG_PROMPT = '配置项：{}\n确认删除配置项吗？'
BATCH_DEL_CONFIG_PROMPT = '已选择{}个配置项\n确认删除选中的配置项吗？'

CONFIG_NAME_TEXT = ' 配置项名称：'
VAR_NAME_TEXT = ' 输出变量名称：'

VAR_NAME_PLACEHOLDER_TEXT = '变量名称最多可输入50字符，须符合变量命名规则，以下划线或大小写字母开头'
VAR_NAME_REG_RULE = r'[_a-zA-Z]\w*'

WIDGET_LABEL_TEXT = ' 配置项控件：'
CONFIG_DESC_TEXT = ' 配置项说明：'
DEFAULT_VALUE_TEXT = '默认值：'
PLACEHOLDER_TEXT = '占位文本：'
VALUE_RANGE_TEXT = '值列表：'
IS_REQUIRED_TEXT = '是否必填：'
ADD_VALUE_BTN_TEXT = '添加值'

ADD_RANGE_VALUE_BOX_TITLE = '添加下拉列表值'