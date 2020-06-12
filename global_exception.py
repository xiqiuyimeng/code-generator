# -*- coding: utf-8 -*-
from functools import wraps
_author_ = 'luwt'
_date_ = '2020/6/11 17:37'


def exc_handle():
    """异常处理"""
    def handle(f):
        @wraps(f)
        def wrapper_exc(*args, **kw):
            # 获取原函数返回值并返回，否则将丢失原函数返回值
            try:
                f_res = f(*args, **kw)
                return f_res
            except Exception as e:
                print(e)
        return wrapper_exc
    return handle

