# -*- coding: utf-8 -*-
from functools import wraps
from exception_enum import *
_author_ = 'luwt'
_date_ = '2020/6/11 17:37'


def get_exc_str(e):
    if isinstance(e, str):
        return e
    else:
        return get_exc_str(e[0])


def exc_handle():
    """异常处理"""
    def handle(f):
        @wraps(f)
        def wrapper_exc(*args, **kw):
            # 获取原函数返回值并返回，否则将丢失原函数返回值
            f_res = None
            try:
                f_res = f(*args, **kw)
            except Exception as e:
                print(f"运行异常: {get_exc_str(e.args)}")
            return f_res
        return wrapper_exc
    return handle


@exc_handle()
def a():
    ExceptionEnum.param_path_error.assert_true()


a()
