# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/2/24 12:31'

# 定位按钮
LOCATION_TXT = '定位'

# 不允许操作提示语
CLOSE_REFRESHING_NODE_PROMPT = '当前节点 [{}] 正在刷新，请等待操作完成'
CLOSE_REFRESHING_CHILD_NODE_PROMPT = '当前节点 [{}] 包含正在刷新的子节点，请等待操作完成'
CLOSE_OPENING_CHILD_NODE_PROMPT = '当前节点 [{}] 包含正在打开的子节点，请等待操作完成'

# -------------------- sql数据源 start --------------------
# 打开连接对话框，标题文本
ADD_CONN_DIALOG_TITLE = "添加{}连接"
EDIT_CONN_DIALOG_TITLE = "编辑{}连接"

"""关于连接的右键菜单"""
# 打开连接
OPEN_CONN_ACTION = '打开连接 [{}]'
# 取消打开连接
CANCEL_OPEN_CONN_ACTION = '取消打开连接 [{}]'
# 关闭连接
CLOSE_CONN_ACTION = '关闭连接 [{}]'
# 测试连接
TEST_CONN_ACTION = '测试连接 [{}]'
# 取消测试连接
CANCEL_TEST_CONN_ACTION = '取消测试连接 [{}]'
# 添加连接
ADD_CONN_ACTION = '添加连接'
# 编辑连接
EDIT_CONN_ACTION = '编辑连接 [{}]'
# 删除连接
DEL_CONN_ACTION = '删除连接 [{}]'
# 刷新连接
REFRESH_CONN_ACTION = '刷新连接 [{}]'
# 取消刷新连接
CANCEL_REFRESH_CONN_ACTION = '取消刷新连接 [{}]'

"""关于数据库的右键菜单"""
# 打开数据库
OPEN_DB_ACTION = '打开数据库 [{}]'
# 取消打开数据库
CANCEL_OPEN_DB_ACTION = '打开数据库 [{}]'
# 关闭数据库
CLOSE_DB_ACTION = '关闭数据库 [{}]'
# 全选所有表
SELECT_ALL_TB_ACTION = '全选所有表'
# 取消选择表
UNSELECT_TB_ACTION = '取消选择表'
# 刷新数据库
REFRESH_DB_ACTION = '刷新数据库 [{}]'
# 取消刷新数据库
CANCEL_REFRESH_DB_ACTION = '取消刷新数据库 [{}]'

"""关于表的右键菜单"""
# 打开表
OPEN_TABLE_ACTION = '打开表 [{}]'
# 取消打开表
CANCEL_OPEN_TABLE_ACTION = '取消打开表 [{}]'
# 关闭表
CLOSE_TABLE_ACTION = '关闭表 [{}]'
# 全选表中所有字段
SELECT_ALL_FIELD_ACTION = '全选 [{}] 表中所有字段'
# 取消选择字段
UNSELECT_FIELD_ACTION = '取消选择字段'
# 刷新数据表
REFRESH_TB_ACTION = '刷新数据表 [{}]'
# 取消刷新数据表
CANCEL_REFRESH_TB_ACTION = '取消刷新数据表 [{}]'

"""操作连接时提示语"""
# 打开连接结果消息盒子标题
OPEN_CONN_BOX_TITLE = "打开连接"
OPEN_CONN_SUCCESS_PROMPT = "打开连接成功"
OPEN_CONN_FAIL_PROMPT = "打开连接失败"

# 关闭连接结果消息盒子标题
CLOSE_CONN_BOX_TITLE = '关闭连接'
CLOSE_CONN_PROMPT = '该连接下有已选的字段，强行关闭将清空连接下所选字段，是否继续'

# 编辑连接提示
EDIT_CONN_PROMPT = '编辑连接需要先关闭连接，是否继续？'

# 删除连接结果消息盒子标题
DEL_CONN_BOX_TITLE = "删除连接"
DEL_CONN_SUCCESS_PROMPT = "删除连接成功"
DEL_CONN_PROMPT = '是否要删除连接？'
DEL_CONN_FAIL_PROMPT = "删除连接失败"

# 读取所有连接结果消息盒子标题
LIST_ALL_CONN_BOX_TITLE = "获取连接列表"
LIST_ALL_CONN_SUCCESS_PROMPT = "获取存储的所有连接成功"
LIST_ALL_CONN_FAIL_PROMPT = "获取存储的所有连接失败"

# 刷新连接结果消息盒子标题
REFRESH_CONN_BOX_TITLE = '刷新连接'
REFRESH_CONN_SUCCESS_PROMPT = "刷新连接成功"
REFRESH_CONN_FAIL_PROMPT = "刷新连接失败"

"""操作数据库时提示语"""
OPEN_DB_BOX_TITLE = "打开数据库"
OPEN_DB_SUCCESS_PROMPT = "打开数据库成功"
OPEN_DB_FAIL_PROMPT = "打开数据库失败"
NO_TBS_PROMPT = "连接[{}]数据库[{}]下没有表！"

CLOSE_DB_BOX_TITLE = '关闭数据库'
CLOSE_DB_PROMPT = '该数据库下有已选的字段，强行关闭将清空库下所选字段，是否继续？'

REFRESH_DB_BOX_TITLE = '刷新数据库'
REFRESH_DB_SUCCESS_PROMPT = "刷新数据库成功"
REFRESH_DB_FAIL_PROMPT = "刷新数据库失败"

"""操作数据表时提示语"""
OPEN_TB_BOX_TITLE = "打开数据表"
OPEN_TB_SUCCESS_PROMPT = "打开数据表成功"
OPEN_TB_FAIL_PROMPT = "打开数据表失败"

REFRESH_TB_BOX_TITLE = '刷新数据表'
REFRESH_TB_SUCCESS_PROMPT = "刷新数据表成功"
REFRESH_TB_FAIL_PROMPT = "刷新数据表失败"

# -------------------- sql数据源 end --------------------

# -------------------- 结构体数据源 start --------------------
CREATE_NEW_FOLDER = '新建文件夹'

# 打开结构体对话框，标题文本
ADD_STRUCT_DIALOG_TITLE = "添加{}数据源"
EDIT_STRUCT_DIALOG_TITLE = "编辑{}数据源"

EDIT_FOLDER_NAME = '编辑文件夹名称'

"""关于结构体的右键菜单"""
OPEN_STRUCT_ACTION = '打开 [{}]'
CLOSE_STRUCT_ACTION = '关闭 [{}]'
CANCEL_OPEN_STRUCT_ACTION = '取消打开 [{}]'
EDIT_STRUCT_ACTION = '编辑 [{}]'
DEL_STRUCT_ACTION = '删除 [{}]'
REFRESH_STRUCT_ACTION = '刷新结构体 [{}]'
CANCEL_REFRESH_STRUCT_ACTION = '取消刷新结构体 [{}]'

"""关于文件夹的右键菜单"""
ADD_STRUCT_ACTION = '添加结构体'
CREATE_NEW_FOLDER_ACTION = '新建文件夹'
SELECT_ALL_ACTION = '全选所有节点'
UNSELECT_ACTION = '取消选择节点'
RENAME_FOLDER_ACTION = '重命名 [{}]'
DEL_FOLDER_ACTION = '删除 [{}]'
REFRESH_FOLDER_ACTION = '刷新文件夹 [{}]'
CANCEL_REFRESH_FOLDER_ACTION = '取消刷新文件 [{}]'

"""操作文件夹提示语"""
DEL_FOLDER_BOX_TITLE = '删除文件夹'
REFRESH_FOLDER_BOX_TITLE = '刷新文件夹'
DEL_FOLDER_PROMPT = '是否要删除文件夹？'

"""操作结构体提示语"""
LIST_ALL_STRUCT_BOX_TITLE = '获取所有结构体列表'
OPEN_STRUCT_BOX_TITLE = '打开结构体'
EDIT_STRUCT_PROMPT = '编辑结构体需要先关闭结构体，是否继续？'
DEL_STRUCT_BOX_TITLE = '删除结构体'
DEL_STRUCT_PROMPT = '是否要删除结构体？'
REFRESH_STRUCT_BOX_TITLE = '刷新结构体'

# -------------------- 结构体数据源 end --------------------

CLOSE_TABLE_BOX_TITLE = '关闭表'
