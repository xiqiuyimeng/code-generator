# -*- coding: utf-8 -*-
"""
获取数据库游标
"""
import pymysql
from logger.log import logger as log
_author_ = 'luwt'
_date_ = '2020/4/19 12:55'


class Cursor:
    """获取mysql数据库游标"""

    def __init__(self, conn_name, host, user, pwd,
                 port=3306, charset='utf8'):
        self.conn_name = conn_name
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.charset = charset
        self.conn = self.get_mysql_conn()
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self.cursor

    def get_mysql_conn(self):
        """打开数据库连接（host/端口/用户名/密码/编码）"""
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                passwd=self.pwd,
                charset=self.charset
            )
            log.info(f"[{self.conn_name}]获取数据库连接成功")
            return conn
        except Exception as e:
            log.error(f"[{self.conn_name}]连接数据库失败：{e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
            log.error(f"[{self.conn_name}]数据库操作产生异常 type:{exc_type}")
            log.error(f"[{self.conn_name}]数据库操作产生异常 value:{exc_val}")
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
        log.info(f"[{self.conn_name}]成功关闭数据库连接")

