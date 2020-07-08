# -*- coding: utf-8 -*-
"""
处理连接相关功能，打开连接、关闭连接、测试连接

"""
from constant import TEST_CONN_MENU, TEST_CONN_SUCCESS_PROMPT, TEST_CONN_FAIL_PROMPT
from cursor_proxy import DBExecutor
from message_box import pop_ok, pop_fail

_author_ = 'luwt'
_date_ = '2020/7/7 16:09'


def open_connection(gui, conn_id):
    """
    根据连接名称，从当前维护的连接字典中获取一个数据库连接操作对象，
    若不存在，则打开一个新的数据库操作对象，并放入连接字典
    :param gui: 启动的主窗口界面对象
    :param conn_id: 连接id，连接字典中的key为连接的id
    """
    # 如果该连接已经打开，直接取，否则获取新的连接
    if not gui.connected_dict.get(conn_id):
        # id name host port user pwd
        conn_info = gui.conns_dict.get(conn_id)
        executor = DBExecutor(*conn_info[2:])
        gui.connected_dict[conn_id] = executor
    else:
        executor = gui.connected_dict.get(conn_id)
    return executor


def close_connection(gui, conn_id):
    """
    关闭指定连接，若无指定连接，则关闭所有，清空连接字典
    :param gui: 启动的主窗口界面对象
    :param conn_id: 连接id
    """
    if conn_id and gui.connected_dict.get(conn_id):
        gui.connected_dict.get(conn_id).exit()
        del gui.connected_dict[conn_id]
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
        pop_ok(TEST_CONN_MENU, TEST_CONN_SUCCESS_PROMPT)
    except Exception as e:
        pop_fail(TEST_CONN_MENU, f'{TEST_CONN_FAIL_PROMPT}\t\n'
                                 f'{e.args[0]} - {e.args[1]}')
        print(e)
