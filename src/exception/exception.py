# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/1/16 15:37'


class ThreadStopException(Exception):

    def __init__(self, err_msg):
        super().__init__()
        self.err_msg = err_msg
