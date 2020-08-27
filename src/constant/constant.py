# -*- coding: utf-8 -*-
"""
所有用到的常量
"""
import os

_author_ = 'luwt'
_date_ = '2020/4/20 10:40'

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
EXIT_MENU = '退出'
ABOUT_MENU = '关于'

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
PROJECT_GENERATOR_BUTTON = '生成到指定项目'
PATH_GENERATOR_BUTTON = '生成到指定路径'
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
TEST_CONN_FAIL_PROMPT = '无法连接到数据库'
# 选择数据库表数据时，无法连接到数据库
SELECT_TABLE_FAIL_PROMPT = '选择数据库表失败'
# 检查系统库中连接名字存在提示语
CONN_NAME_EXISTS = '当前名称不可用，{}已存在！'
CONN_NAME_AVAILABLE = '连接名称{}可用'
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
MYBATIS_GENERATOR_DESC = '\n根据官方生成器生成的代码样例制作。可以生成Java实体类文件，' \
                         'mapper接口文件，xml文件。\n1. 默认增加了列表查询语句。' \
                         '\n2. 可根据配置决定是否生成set和get方法，默认不生成，生成@Data注解。'\
                         '\n3. 当前支持整表生成，也支持选择部分表字段生成，需要注意的是，' \
                         '部分选择字段时，仅生成当前的Java实体类中需要新增的类属性代码' \
                         '及xml文件中需要新增的代码，例如resultMap与插入更新代码块。' \
                         '\n4. 以下参数皆为必填项，填写Java项目地址后，将开启其他项，生成器会直接将文件生成到您指定的项目目录中。'
MYBATIS_PATH_GENERATOR_DESC = '\n根据官方生成器生成的代码样例制作。可以生成Java实体类文件，' \
                         'mapper接口文件，xml文件。\n1. 默认增加了列表查询语句。' \
                         '\n2. 可根据配置决定是否生成set和get方法，默认不生成，生成@Data注解。'\
                         '\n3. 当前支持整表生成，也支持选择部分表字段生成，需要注意的是，' \
                         '部分选择字段时，仅生成当前的Java实体类中需要新增的类属性代码' \
                         '及xml文件中需要新增的代码，例如resultMap与插入更新代码块。' \
                         '\n4. 参数解释：支持指定路径生成，指定路径后，将开启其他输入项，生成的所有文件都会存放在您指定的目录中。'
IS_LOMBOK = '是否启用lombok注解'
LOMBOK_DESC = 'lombok注解：如果选择开启，那么在生成的Java实体类中，将不复生成get与set方法，' \
              '以@Data注解代替之，否则，将生成完整的get与set方法。'
OUTPUT_PATH = '输出的指定路径'
OUTPUT_PATH_DESC = '输出的指定路径：生成器会把所有生成的文件都存放到您指定的目录中，方便您查看和使用。'
JAVA_PATH = 'Java项目地址'
JAVA_PATH_DESC = 'java项目地址：即为java项目的根目录所在的绝对路径，例如：D:/workspace/demo，输入后将开始源码包和xml地址的输入'
JAVA_SRC_PATH = 'Java项目源码包相对路径'
JAVA_SRC_PATH_DESC = 'Java项目源码包相对路径：在Java项目根目录下，到Java源码包的路径，一般为src/main/java，输入后将开启所有的包名输入'
MODEL_PACKAGE = 'Java实体类包名'
MODEL_PACKAGE_DESC = 'Java实体类包名：您希望输出的Java实体类的包名，例如：com.demo.model'
MAPPER_PACKAGE = 'mapper接口包名'
MAPPER_PACKAGE_DESC = 'mapper接口包名：您希望输出的mapper接口文件的包名，例如：com.demo.dao'
XML_PATH = 'xml文件输出路径'
XML_PATH_DESC = 'xml输出路径：您希望输出的mybatis xml文件存放路径，' \
                '例如：D:/workspace/demo/src/main/resources/mybatis'

"""生成弹窗tab页，spring"""
# spring的tab页名称
SPRING_TAB_TITLE = 'spring生成器'
# spring页面标题
SPRING_TITLE = 'spring 生成器输出配置'
SPRING_GENERATOR_DESC = '对于mybatis生成器进行扩展，可以生成相应的service、serviceImpl、controller类。' \
                        '\n1. 当前仅支持整表选择生成，字段部分选择情况暂不支持。' \
                        '因为部分选择字段意味着您的项目中已经存在了这些代码，再次生成将会覆盖，带来不必要的麻烦。' \
                        '\n2. 这里仅需要配置三类文件的输出包名即可，系统会根据mybatis生成器中的配置自动获取相关信息。' \
                        '\n3. 以下参数为是否使用spring生成器的标识，如果填写了，则会使用spring生成器。' \
                        '\n4. 在本页清空配置将只影响本页的参数，在mybatis参数配置页清空，将一并清空本页配置。'
SERVICE_PACKAGE = 'service接口包名'
SERVICE_PACKAGE_DESC = 'service接口包名：您希望输出的service接口文件的包名，例如：com.demo.service'
SERVICE_IMPL_PACKAGE = 'service实现类包名'
SERVICE_IMPL_PACKAGE_DESC = 'service实现类包名：您希望输出的service实现类的包名，例如：com.demo.service.impl'
CONTROLLER_PACKAGE = 'controller类包名'
CONTROLLER_PACKAGE_DESC = 'controller类包名：您希望输出的controller文件的包名，例如：com.demo.controller'
"""生成配置spring页弹窗"""
ASK_TITLE = '生成配置'
ASK_PROMPT = 'mybatis配置页输入信息尚未填写，spring页输入项无法开放。是否返回mybatis页继续填写？'
"""帮助信息页面"""
HELP_TITLE = '生成器帮助信息'
HELP_MYSQL_CONN_TITLE = 'mysql连接管理'
HELP_MYSQL_CONN_INFO = '生成器提供对mysql连接的基本管理功能，添加连接、删除连接、测试连接、编辑连接。当您打开一个连接后，' \
                  '生成器将会读取mysql连接中所包含的所有库表信息，树形结构界面最多可展示到表名，如需查看表的结构，' \
                  '可以双击或者右键菜单打开表。'
HELP_SELECT_COL_TITLE = '表字段的选择'
HELP_SELECT_COL_INFO = '打开数据库连接后，需要选中表，提供多种方式选择，选中表或选中表中部分字段后，' \
                   '生成器将会记录下您选择的表字段信息。点击生成按钮可查看到当前已选择的表字段信息。'
HELP_PATH_GENERATOR_TITLE = '按生成路径选择生成器'
HELP_PATH_GENERATOR_INFO = '系统提供两种路径生成器，生成到指定路径生成器和生成到指定项目生成器。顾名思义，' \
                           '生成到指定路径生成器将会要求您指定一个目标目录，填写相关信息即可生成，' \
                           '所有生成的文件都会被保存到您指定的目录中；生成到指定项目生成器将会要求您指定一个项目路径，' \
                           '填写相关项目路径信息即可生成，所有生成的文件将会按照包名和路径自动填入项目的相应位置，' \
                           '若路径包名配置正确，生成后的代码无需修改即可启动测试。'
HELP_PROJECT_GENERATOR_TITLE = '按生成功能选择生成器'
HELP_PROJECT_GENERATOR_INFO = '在您选择指定路径生成器或指定项目生成器后，您需要填写的是生成mybatis代码需要的信息，' \
                              'mybatis生成器将会生成Java实体类文件、mapper接口文件、xml配置文件。系统另外提供扩展版的spring生成器，' \
                              'spring生成器在mybatis生成器基础之上进行扩展，可生成service接口、service实现类、controller类，' \
                              '不过需要注意的是，必须填写完全mybatis生生器配置页才可开启spring生成器配置页面的输入项。'
"""关于信息"""
ABOUT_TITLE = '关于生成器'
GENERATOR_TITLE = '生成器分类'
ABOUT_MYBATIS_TITLE = 'mybatis生成器'
ABOUT_MYBATIS_INFO = '1.根据官方mybatis样例代码格式制作。可以生成Java实体类文件、mapper接口文件、xml配置文件。' \
                     '\n2.在mapper接口文件和xml文件中默认增加了列表查询语句，即实现了增删改查列表功能。\n3.与官方生成器不同的是，' \
                     '生成器可以提供部分字段的生成，例如在原有表结构上新增了一些字段，生成器将会生成这部分字段所对应的要改变的代码' \
                     '（Java实体类文件、xml文件），将新增部分粘贴在原代码处即可。\n4.Java实体类文件默认使用lombok的@Data注解' \
                     '替代冗余的属性get和set方法。\n'
ABOUT_SPRING_TITLE = 'spring生成器'
ABOUT_SPRING_INFO = '1.基于mybatis生成器进行扩展，生成spring框架所需的相应业务代码，可生成service、serviceImpl、controller类。' \
                    '需要注意的是，如果选择的是表的部分字段，将不生成这三个文件，因为对业务表的新增字段通常不影响上层接口。\n'
ABOUT_PATH_TITLE = '生成器路径分类'
APPOINT_PATH = '指定路径'
APPOINT_PATH_INFO = '生成到指定路径意味着所有的文件都将生成到同一个目录下，此时所填写的包名仅仅是作为代码中package关键字的值，' \
                    '生成到指定目录后，需要手动拷贝至自己的项目下。'
APPOINT_PROJECT = '指定项目地址'
APPOINT_PROJECT_INFO = '生成到指定项目意味着所有生成的文件都将按照规则被放置在相应的项目目录下。此时的项目路径需要填写正确，' \
                       '输入项都会做相应检查。如果输入路径包名都正确，那么生成的spring全套代码是可以直接运行的。'
