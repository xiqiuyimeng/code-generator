# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/2/24 15:00'


# ---------- 对话框占位符文本 start ---------- #
PORT_INPUT_PLACEHOLDER_TEXT = '端口号只允许输入数字符'
HOST_MAX_LENGTH_PLACEHOLDER_TEXT = '主机地址最多可输入100字符'
USER_MAX_LENGTH_PLACEHOLDER_TEXT = '用户名最多可输入30字符'
PWD_MAX_LENGTH_PLACEHOLDER_TEXT = '密码最多可输入50字符'
SERVICE_NAME_MAX_LENGTH_PLACEHOLDER_TEXT = '服务最多可输入50字符'
# ---------- 对话框占位符文本 end ---------- #


# ---------- 连接对话框中的展示文本 start ---------- #
# 输入框部分
CONN_NAME_TEXT = "连接名："
HOST_TEXT = "主机："
SERVICE_NAME_TEXT = '服务：'
PORT_TEXT = "端口号："
USERNAME_TEXT = "用户名："
PWD_TEXT = "密码："
SQLITE_FILE_URL_TXT = "文件："
CHOOSE_SQLITE_FILE = "选择文件"
# mysql 默认host、端口、用户名
MYSQL_DEFAULT_HOST = "localhost"
MYSQL_DEFAULT_PORT = "3306"
MYSQL_DEFAULT_USER = "root"
# oracle
ORACLE_DEFAULT_HOST = 'localhost'
ORACLE_DEFAULT_PORT = '1521'
ORACLE_DEFAULT_SERVICE_NAME = 'XE'
# ---------- 连接对话框中的展示文本 end ---------- #


# ---------- 结构体对话框中的展示文本 start ---------- #
DEL_STRUCT_TITLE = '删除数据源'
STRUCTURE_NAME_TEXT = "{}数据源名称："
STRUCTURE_FILE_URL_TEXT = "{}文件地址： "
STRUCTURE_CONTENT_TEXT = "{}数据源内容："
PRETTY_STRUCT_TEXT = '美化{}'
CHOOSE_STRUCT_FILE_TEXT = "选择文件"
SAVE_STRUCT_TITLE = '保存{}数据源'
SAVE_STRUCT_TO = '保存到'
ADD_FOLDER_BOX_TITLE = '新建文件夹'
EDIT_FOLDER_BOX_TITLE = '编辑文件夹'
DEL_FOLDER_TITLE = '删除文件夹'
# ---------- 结构体对话框中的展示文本 start ---------- #


# 按钮部分
TEST_CONN_BTN_TEXT = "测试连接"

"""操作连接时提示语"""
# 查询连接信息结果消息盒子标题
QUERY_CONN_BOX_TITLE = '查询连接信息'

# 测试连接结果消息盒子标题
TEST_CONN_BOX_TITLE = "测试连接"
TEST_CONN_SUCCESS_PROMPT = "测试连接成功"
TEST_CONN_FAIL_PROMPT = "测试连接失败"

# 保存连接结果消息盒子标题
SAVE_CONN_BOX_TITLE = "保存连接"
SAVE_CONN_SUCCESS_PROMPT = "保存连接成功"
SAVE_CONN_FAIL_PROMPT = "保存连接失败"

"""操作结构体时提示语"""
# 查询结构体结果消息盒子标题
QUERY_STRUCT_BOX_TITLE = '查询结构体'
READ_STRUCT_FILE_BOX_TITLE = '读取{}文件'
PRETTY_STRUCT_BOX_TITLE = '美化{}'
EDIT_STRUCT_BOX_TITLE = '修改{}'
ADD_STRUCT_BOX_TITLE = '添加{}'
