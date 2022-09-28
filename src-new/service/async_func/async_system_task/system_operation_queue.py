# -*- coding: utf-8 -*-
import threading
from queue import Queue

_author_ = 'luwt'
_date_ = '2022/9/26 18:29'


class SystemOperationQueue:

    def __init__(self):
        # 负责传输系统操作记录
        self.queue = Queue()
        # 消费队列元素的线程
        self.consumer_thread = threading.Thread(target=self.consume)

    def produce(self, operation):
        self.queue.put(operation)

    def consume(self):
        while True:
            get = self.queue.get()
            print(get)

