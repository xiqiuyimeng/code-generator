# -*- coding: utf-8 -*-
from service.async_func.async_task_abc import ThreadWorkerABC

_author_ = 'luwt'
_date_ = '2022/9/26 18:33'


class SystemThreadWorker(ThreadWorkerABC):

    def __init__(self):
        super().__init__()

    def do_run(self): ...

    def do_exception(self, e: Exception): ...



