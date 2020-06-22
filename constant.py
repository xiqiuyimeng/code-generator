# -*- coding: utf-8 -*-
_author_ = 'luwt'
_date_ = '2020/4/20 10:40'

# 默认配置文件地址
DEFAULT_CONFIG_PATH = 'config.xml'

# 数据库默认端口
DEFAULT_DB_PORT = 3306
# 数据库默认字符集
DEFAULT_DB_CHARSET = 'utf8'

# 测试数据库连接，查询数据库版本信息
TEST_CONN_SQL = 'select version();'

# 查询数据库列表
QUERY_DB_SQL = 'show databases;'

# 查询数据库中的表名sql
QUERY_TABLES_SQL = 'show tables;'

# 创建临时表sql
CREATE_TEMP_TB = 'create temporary table tmp_table'
# 查询临时表sql
QUERY_TEMP_TB = 'show full fields from tmp_table'
# 查询系统表sql
QUERY_SYS_TB = 'select column_name, data_type, column_key, column_comment from information_schema.columns'

# 生成路径前缀语
OUTPUT_PREFIX = '生成的文件为：'

# 默认的mapper命名空间
DEFAULT_MAPPER_NS = "待填写"
# 默认的model命名空间
DEFAULT_MODEL_NS = "实体类"

# 默认输出目录
DEFAULT_PATH = "./输出目录"

# 默认java模板文件路径
DEFAULT_JAVA_TP = 'java.txt'
# 默认mapper模板文件路径
DEFAULT_MAPPER_TP = 'mapper.txt'
# 默认xml模板文件路径
DEFAULT_XML_TP = 'xml.txt'
# 默认service模板文件路径
DEFAULT_SERVICE_TP = 'service.txt'
# 默认service_impl模板文件路径
DEFAULT_SERVICE_IMPL_TP = 'service_impl.txt'
# 默认controller模板文件路径
DEFAULT_CONTROLLER_TP = 'controller.txt'
# 默认java项目源码包的相对路径结构
DEFAULT_JAVA_SRC_RELATIVE_PATH = 'src/main/java'

# 选择生成器类型
CHOOSE_GENERATOR_TYPE = "请选择生成下面哪一种代码：\r\n1.mybatis(mapper, xml, model)\r\n" \
                           "2.spring(controller, service, serviceImpl, mapper, xml, model)"
# 路径
PATH_ERROR = "请检查config.xml中else标签参数，因为已选java_output和xml_output，所以else标签参数必不可少"
# 参数有误
PARAM_ERROR = "请检查config.xml中参数，按任意键退出"
# spring生成器错误提示
SPRING_ERROR = "spring代码不支持指定列和自定义sql，请检查config.xml中参数，按任意键退出"
# 输入不合法错误
INPUT_ILLEGAL = "输入不合法，按任意键退出"
# 路径参数有误
PARAM_PATH_ERROR = "路径参数有误"

# 执行成功提示语
SUCCESS = "执行成功！五秒后退出"

"""关于连接的右键菜单"""
# 打开连接
OPEN_CONN_MENU = '打开连接'
# 关闭连接
CLOSE_CONN_MENU = '关闭连接'
# 测试连接
TEST_CONN_MENU = '测试连接'
# 添加连接
ADD_CONN_MENU = '添加连接'
# 编辑连接
EDIT_CONN_MENU = '编辑连接'
# 删除连接
DEL_CONN_MENU = '删除连接'

"""关于数据库的右键菜单"""
# 打开数据库
OPEN_DB_MENU = '打开数据库'
# 关闭数据库
CLOSE_DB_MENU = '关闭数据库'
# 全选所有表
SELECT_ALL_TB_MENU = '全选所有表'
# 取消选择表
UNSELECT_TB_MENU = '取消选择表'

"""关于表的右键菜单"""
# 打开表
OPEN_TABLE_MENU = '打开表'
# 关闭表
CLOSE_TABLE_MENU = '关闭表'
# 全选表中所有字段
SELECT_ALL_FIELD_MENU = '全选表中所有字段'
# 取消选择字段
UNSELECT_FIELD_MENU = '取消选择字段'
# 生成
GENERATE_MENU = '生成'

"""消息框按钮文字"""
OK_BUTTON = '确定'
ACCEPT_BUTTON = '是'
REJECT_BUTTON = '否'

"""操作连接时提示语"""
# 编辑连接时的提示语
EDIT_CONN_PROMPT = '编辑连接需要先关闭连接，是否继续？'
# 删除连接时的提示语
DEL_CONN_PROMPT = '是否要删除连接？'
# 保存连接成功提示语
SAVE_CONN_SUCCESS_PROMPT = '保存成功！'
# 测试连接成功提示语
TEST_CONN_SUCCESS_PROMPT = '连接成功！'
# 测试连接失败提示语
TEST_CONN_FAIL_PROMPT = '连接失败！'

"""表格列头"""
TABLE_HEADER_LABELS = ["全选", "字段名", "数据类型", "备注"]

"""树部件头标题"""
TREE_HEADER_LABELS = 'mysql连接列表'
