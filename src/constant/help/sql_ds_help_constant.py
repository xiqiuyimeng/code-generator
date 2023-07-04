# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/15 11:32'


OVERVIEW_TEXT = '目前sql数据源支持三种数据源：sqlite、mysql、oracle，对于sql数据源来说，都存在连接、库、表、列四级概念，' \
                '所以主数据区域，左侧数据源列表，将以树节点形式维护数据库层级关系，对于数据表的详细信息，也就是列将展示在主数据区域右侧，' \
                '当打开数据表时，在右侧将展示数据表的列信息。' \
                '<p class="import">需要注意的是刷新最大粒度支持刷新整个连接，并且与打开操作互斥，当刷新进行中时，' \
                '无法进行其他操作，需要等待操作完成，如果子节点处于刷新或打开中，那么父节点也无法关闭、无法刷新</p>'

SQLITE_LABEL_TEXT = 'sqlite：'
SQLITE_HELP_TEXT = 'sqlite 是非网络型数据库，所以只需要选择本地 sqlite 数据库文件即可连接'

MYSQL_LABEL_TEXT = 'mysql：'
MYSQL_HELP_TEXT = '<p>mysql 是网络型数据库，需要通过网络连接，所以需要填写以下信息</p>' \
                  '<ul>' \
                  ' <li>主机：主机地址，mysql 数据库的ip地址，默认本机 localhost</li>' \
                  ' <li>端口号：mysql 数据库的端口号，默认 3306</li>' \
                  ' <li>用户名：连接 mysql 数据库使用的用户名，默认 root</li>' \
                  ' <li>密码：连接 mysql 数据库使用的密码，这里不会加密，方便查看</li>' \
                  '</ul>'

ORACLE_LABEL_TEXT = 'oracle：'
ORACLE_HELP_TEXT = '<p>oracle 是网络型数据库，需要通过网络连接，所以需要填写以下信息</p>' \
                   '<ul>' \
                   ' <li>主机：主机地址，oracle 数据库的ip地址，默认本机 localhost</li>' \
                   ' <li>服务：service name 或 sid，连接 oracle 数据库时必须提供，默认 XE</li>' \
                   ' <li>端口号：oracle 数据库的端口号，默认 1521</li>' \
                   ' <li>用户名：连接 oracle 数据库使用的用户名</li>' \
                   ' <li>密码：连接 oracle 数据库使用的密码，这里不会加密，方便查看</li>' \
                   '</ul>'
