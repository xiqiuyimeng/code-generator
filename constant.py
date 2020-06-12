# -*- coding: utf-8 -*-
_author_ = 'luwt'
_date_ = '2020/4/20 10:40'

# 默认配置文件地址
DEFAULT_CONFIG_PATH = 'config.xml'

# 数据库默认端口
DEFAULT_DB_PORT = 3306
# 数据库默认字符集
DEFAULT_DB_CHARSET = 'utf8'

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
