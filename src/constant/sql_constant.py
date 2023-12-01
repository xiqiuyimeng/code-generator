# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/2/24 14:00'


# ---------- 查询数据库结构sql start ---------- #

# sqlite 查询数据库列表sql
SQLITE_QUERY_DB_SQL = 'PRAGMA database_list;'
# sqlite 检查数据库是否存在sql
SQLITE_CHECK_DB_SQL = 'SELECT name FROM pragma_database_list WHERE name = "{}"'
# sqlite 查询数据库表名sql
SQLITE_QUERY_TB_SQL = 'select tbl_name from sqlite_master where tbl_name != "sqlite_sequence";'
# sqlite 检查数据库表是否存在sql，这里需指定格式化字符串使用的索引，第一个是库，第二个是表，这里只用表，所以指定索引为1
SQLITE_CHECK_TB_SQL = 'SELECT name FROM sqlite_master WHERE type = "table" and name = "{1}"'
# sqlite 查询数据库表列名sql，这里也使用表，所以指定索引为1
SQLITE_QUERY_COL_SQL = 'PRAGMA table_info(`{1}`);'

# mysql查询数据库列表sql
MYSQL_QUERY_DB_SQL = 'show databases'
# mysql检查数据库表sql
MYSQL_CHECK_DB_SQL = 'show databases like "{}"'
# mysql查询数据库中的表名sql
MYSQL_QUERY_TB_SQL = 'show tables from {}'
# mysql检查表sql
MYSQL_CHECK_TB_SQL = 'show tables from {} like "{}"'
# mysql获取表注释sql
MYSQL_QUERY_TB_COMMENT_SQL = 'show table status from {} like "{}"'
# mysql查询数据库表的列名sql
MYSQL_QUERY_COL_SQL = "show full columns from `{}`.`{}`"

# oracle查询数据库列表sql
ORACLE_QUERY_DB_SQL = 'select distinct(OWNER) from all_tables order by OWNER'
# oracle检查数据库sql
ORACLE_CHECK_DB_SQL = 'select distinct(OWNER) from all_tables where OWNER = \'{}\''
# oracle查询数据库中的表名sql
ORACLE_QUERY_TB_SQL = 'select TABLE_NAME from ALL_TABLES where OWNER = \'{}\' order by TABLE_NAME'
# oracle检查表sql
ORACLE_CHECK_TB_SQL = 'select TABLE_NAME from ALL_TABLES where OWNER = \'{}\' and TABLE_NAME = \'{}\''
# oracle查询数据库表的列名sql
ORACLE_QUERY_COL_SQL = """
select ATC.COLUMN_NAME, ATC.DATA_TYPE, ATC.DATA_LENGTH, ATC.DATA_PRECISION, ATC.DATA_SCALE,
       ATC.CHAR_USED, UCC.COMMENTS, nvl2(UP.CONSTRAINT_TYPE, 'Y', 'N') as PRIMARY_KEY
from ALL_TAB_COLS ATC
    inner join USER_COL_COMMENTS UCC on ATC.TABLE_NAME = UCC.TABLE_NAME and ATC.COLUMN_NAME = UCC.COLUMN_NAME
    left join (select COLUMN_NAME, CONSTRAINT_TYPE, UC.TABLE_NAME
               from USER_CONS_COLUMNS UCC inner join USER_CONSTRAINTS UC
                on UCC.CONSTRAINT_NAME = UC.CONSTRAINT_NAME and
                   UCC.TABLE_NAME = UC.TABLE_NAME and
                   UCC.OWNER = UC.OWNER and UC.CONSTRAINT_TYPE = 'P') UP
        on UP.COLUMN_NAME = ATC.COLUMN_NAME and UP.TABLE_NAME = ATC.TABLE_NAME
where ATC.OWNER = '{}' and ATC.TABLE_NAME = '{}'
order by ATC.COLUMN_ID"""

# ---------- 查询数据库结构sql end ---------- #
