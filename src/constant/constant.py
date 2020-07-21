# -*- coding: utf-8 -*-
"""
所有用到的常量
"""
import os

_author_ = 'luwt'
_date_ = '2020/4/20 10:40'

# 默认配置文件地址
DEFAULT_CONFIG_PATH = 'config.xml'

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
# 查询系统表和列sql
QUERY_SYS_TB_COL = 'select column_name, table_name from information_schema.columns'

# 生成路径前缀语
OUTPUT_PREFIX = '生成的文件为：'

# 默认的mapper命名空间
DEFAULT_MAPPER_NS = "待填写"
# 默认的model命名空间
DEFAULT_MODEL_NS = "实体类"

# 默认输出目录
DEFAULT_PATH = "./输出目录"
# icon 目录
ICON_DIR = os.path.dirname(__file__) + '/../../static/icon/'
# bg 目录
BG_dir = os.path.dirname(__file__) + '/../../static/bg_jpg/'

# 项目目录
TEMPLATE_PATH = (os.path.split(os.path.dirname(__file__))[0]).replace("\\", "/") + "/../static/template"
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

# 路径参数有误
PARAM_PATH_ERROR = "路径参数有误"

"""菜单栏"""
FILE_MENU = '文件'
HELP_MENU = '帮助'

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
""""消息弹窗"""
WARNING_TITLE = '警告信息'
PARAM_WARNING_MSG = '系统检测到以下路径:\n{}\n可能存在问题，请确认，以免影响生成结果'
WARNING_NONE = '有参数未填！请检查参数'
WARNING_OK = '确认无误'
WARNING_RESELECT = '重新选择'
WRONG_TITLE = '错误'
WRONG_UNSELECT_DATA = '当前未选中数据，请选择后再执行！'

"""消息框按钮文字"""
OK_BUTTON = '确定'
ACCEPT_BUTTON = '是'
REJECT_BUTTON = '否'

"""按钮文字"""
NEXT_STEP_BUTTON = '下一步'
PRE_STEP_BUTTON = '上一步'
CANCEL_BUTTON = '取消'
EXPAND_BUTTON = '一键展开所有项'
COLLAPSE_BUTTON = '一键折叠所有项'
CLEAR_CONFIG_BUTTON = '清空本页配置'
GENERATE_BUTTON = '开始生成'
CHOOSE_DIRECTORY = '请选择文件夹'

"""操作连接时提示语"""
# 编辑连接时的提示语
EDIT_CONN_PROMPT = '编辑连接需要先关闭连接，是否继续？'
# 编辑连接关闭时如有选择字段
EDIT_CONN_WITH_FIELD_PROMPT = '编辑连接需要先关闭连接，此连接下有已选的字段，' \
                              '如果继续将清空此连接下已选字段并关闭连接，是否继续？'
# 删除连接时的提示语
DEL_CONN_PROMPT = '是否要删除连接？'
# 删除连接时如有选择字段
DEL_CONN_WITH_FIELD_PROMPT = '此连接下有已选字段，如果继续将清空此连接下已选字段并删除连接，是否继续？'
# 保存连接成功提示语
SAVE_CONN_SUCCESS_PROMPT = '保存成功！'
# 测试连接成功提示语
TEST_CONN_SUCCESS_PROMPT = '连接成功！'
# 测试连接失败提示语
TEST_CONN_FAIL_PROMPT = '连接失败！'
# 检查系统库中连接名字存在提示语
CONN_NAME_EXISTS = '连接名称已存在！'
# 关闭连接时的提示语
CLOSE_CONN_PROMPT = '该连接下有已选的字段，强行关闭将清空连接下所选字段，是否继续'

"""操作数据库时提示语"""
# 关闭数据库时提示语
CLOSE_DB_PROMPT = '该数据库下有已选的字段，强行关闭将清空库下所选字段，是否继续？'

"""表格列头"""
TABLE_HEADER_LABELS = ["全选", "字段名", "数据类型", "备注"]

"""主页面树部件头标题"""
TREE_HEADER_LABELS = 'mysql连接列表'

"""生成弹窗确认页树部件头标题"""
CONFIRM_TREE_HEADER_LABELS = '已选择的表字段列表'

"""生成弹窗tab页，mybatis"""
# mybatis的tab页名称
MYBATIS_TAB_TITLE = 'mybatis生成器'
# mybatis页面标题
MYBATIS_TITLE = 'mybatis生成器输出配置'
MYBATIS_GENERATOR_DESC = 'mybatis生成器：根据官方生成器生成的代码样例制作。可以生成Java实体类文件，' \
                         'mapper接口文件，xml文件。\n1. 默认增加了列表查询语句。' \
                         '\n2. 可根据配置决定是否生成set和get方法，默认不生成，生成@Data注解。'\
                         '\n3. 当前支持整表生成，也支持选择部分表字段生成，需要注意的是，' \
                         '部分选择字段时，仅生成当前的Java实体类中\n\b\b需要新增的类属性代码' \
                         '及xml文件中需要新增的代码，例如resultMap与插入更新代码块。' \
                         '\n4. 以下参数皆为必填项，填写Java项目地址后，才可开启其他项。'
IS_LOMBOK = '是否启用lombok注解'
LOMBOK_DESC = 'lombok注解：如果选择开启，那么在生成的Java实体类中，将不复生成get与set方法，' \
              '以@Data注解代替之，\n\t否则，将生成完整的get与set方法。'
JAVA_PATH = 'Java项目地址'
JAVA_PATH_DESC = 'java项目地址：即为java项目的根目录所在的绝对路径，例如：D:/workspace/demo'
JAVA_SRC_PATH = 'Java项目源码包相对路径'
JAVA_SRC_PATH_DESC = 'Java项目源码包相对路径：在Java项目根目录下，到Java源码包的路径，一般为src/main/java' \
                     '\n\t填写Java项目地址后开启'
MODEL_PACKAGE = 'Java实体类包名'
MODEL_PACKAGE_DESC = 'Java实体类包名：您希望输出的Java实体类的包名，例如：com.demo.model' \
                     '\n\t填写Java项目源码包相对路径后开启'
MAPPER_PACKAGE = 'mapper接口包名'
MAPPER_PACKAGE_DESC = 'mapper接口包名：您希望输出的mapper接口文件的包名，例如：com.demo.dao' \
                      '\n\t填写Java项目源码包相对路径后开启'
XML_PATH = 'xml文件输出路径'
XML_PATH_DESC = 'xml输出路径：您希望输出的mybatis xml文件存放路径，' \
                '例如：D:/workspace/demo/src/main/resources/mybatis\n\t填写Java项目地址后开启'

"""生成弹窗tab页，spring"""
# spring的tab页名称
SPRING_TAB_TITLE = 'spring生成器'
# spring页面标题
SPRING_TITLE = 'spring 生成器输出配置'
SPRING_GENERATOR_DESC = 'spring生成器：对于mybatis生成器进行扩展，可以生成相应的service、serviceImpl、controller类。' \
                        '\n1. 当前仅支持整表选择生成，字段部分选择情况暂不支持。' \
                        '因为部分选择字段意味着您的项目中已经存在了这些代码，' \
                        '\n\b\b再次生成将会覆盖，带来不必要的麻烦。' \
                        '\n2. 这里仅需要配置三类文件的输出包名即可，系统会根据mybatis生成器中的配置自动获取相关信息。' \
                        '\n3. 以下参数为是否使用spring生成器的标识，如果填写了，则会使用spring生成器。' \
                        '\n4. 在本页清空配置将只影响本页的参数，在mybatis参数配置页清空，将一并清空本页配置。'
SERVICE_PACKAGE = 'service接口包名'
SERVICE_PACKAGE_DESC = 'service接口包名：您希望输出的service接口文件的包名，例如：com.demo.service' \
                       '\n\t填写Java项目源码包相对路径后开启'
SERVICE_IMPL_PACKAGE = 'service实现类包名'
SERVICE_IMPL_PACKAGE_DESC = 'service实现类包名：您希望输出的service实现类的包名，例如：com.demo.service.impl' \
                            '\n\t填写Java项目源码包相对路径后开启'
CONTROLLER_PACKAGE = 'controller类包名'
CONTROLLER_PACKAGE_DESC = 'controller类包名：您希望输出的controller文件的包名，例如：com.demo.controller' \
                          '\n\t填写Java项目源码包相对路径后开启'

