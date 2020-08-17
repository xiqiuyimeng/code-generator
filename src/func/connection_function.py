# -*- coding: utf-8 -*-
"""
处理连接相关功能，打开连接、关闭连接、测试连接

"""
from src.constant.constant import TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT
from src.db.cursor_proxy import DBExecutor

_author_ = 'luwt'
_date_ = '2020/7/7 16:09'


def open_connection(gui, conn_id, conn_name):
    """
    根据连接名称，从当前维护的连接字典中获取一个数据库连接操作对象，
    若不存在，则打开一个新的数据库操作对象，并放入连接字典
    :param gui: 启动的主窗口界面对象
    :param conn_id: 连接id，在页面展示的连接字典中的key为连接的id，
        可取出当前点击的连接完整信息
    :param conn_name: 连接名称，作为已连接数据库的连接字典key。
    """
    # 如果该连接已经打开，直接取，否则获取新的连接
    if not gui.connected_dict.get(conn_name):
        # id name host port user pwd
        conn_info = gui.display_conn_dict.get(conn_id)
        executor = DBExecutor(*conn_info[2:])
        gui.connected_dict[conn_name] = executor
    else:
        executor = gui.connected_dict.get(conn_name)
    return executor


def close_connection(gui, conn_name):
    """
    关闭指定连接，若无指定连接，则关闭所有，清空连接字典
    :param gui: 启动的主窗口界面对象
    :param conn_name: 连接名称，作为已连接数据库的连接字典key。
    """
    if conn_name and gui.connected_dict.get(conn_name):
        gui.connected_dict.get(conn_name).exit()
        del gui.connected_dict[conn_name]
    else:
        [executor.exit() for executor in gui.connected_dict.values()]
        gui.connected_dict.clear()


def test_connection(connection):
    """
    测试连接
    :param connection: 连接对象
    """
    try:
        with DBExecutor(
                connection.host,
                connection.port,
                connection.user,
                connection.pwd
        ) as cur:
            cur.test_conn()
        return True, TEST_CONN_SUCCESS_PROMPT
    except Exception as e:
        return False, f'{TEST_CONN_FAIL_PROMPT}\t\n {e.args[0]} - {e.args[1]}'
