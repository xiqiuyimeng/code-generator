# -*- coding: utf-8 -*-
from queue import Queue

from PyQt5.QtCore import pyqtSignal

from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, ThreadExecutorABC
from service.system_storage.opened_tree_item_sqlite import OpenedTreeItem, ExpandedEnum, OpenedTreeItemSqlite, \
    CurrentEnum
from view.tree.tree_widget.tree_item_func import get_item_opened_record, set_item_opened_record

_author_ = 'luwt'
_date_ = '2022/10/3 10:10'


class ItemChangedWorker(ThreadWorkerABC):

    success_signal = pyqtSignal()

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def do_run(self):
        while True:
            method, opened_item = self.queue.get()
            if method == 'item_collapsed':
                OpenedTreeItemSqlite().update(opened_item)
            elif method == 'item_expanded':
                OpenedTreeItemSqlite().update(opened_item)
            elif method == 'current_item_changed':
                OpenedTreeItemSqlite().item_current_changed(opened_item)
            log.info(f'{method}: {opened_item}')

    def do_exception(self, e: Exception):
        log.exception('更改树节点状态异常')


class ItemChangedExecutor(ThreadExecutorABC):

    def __init__(self):
        self.queue = Queue()
        super().__init__(None, None)

    def get_worker(self) -> ThreadWorkerABC:
        return ItemChangedWorker(self.queue)

    def item_collapsed(self, item):
        opened_record: OpenedTreeItem = get_item_opened_record(item)
        opened_record.expanded = ExpandedEnum.collapsed.value
        set_item_opened_record(item, opened_record)
        self.queue.put(('item_collapsed', opened_record))

    def item_expanded(self, item):
        opened_record: OpenedTreeItem = get_item_opened_record(item)
        opened_record.expanded = ExpandedEnum.expanded.value
        set_item_opened_record(item, opened_record)
        self.queue.put(('item_expanded', opened_record))

    def current_item_changed(self, current_item):
        current_opened_record: OpenedTreeItem = get_item_opened_record(current_item)
        current_opened_record.is_current = CurrentEnum.is_current.value
        set_item_opened_record(current_item, current_opened_record)
        self.queue.put(('current_item_changed', current_opened_record))

    def not_current_item(self, item):
        opened_item = get_item_opened_record(item)
        opened_item.is_current = CurrentEnum.not_current.value
        set_item_opened_record(item, opened_item)
        self.queue.put(('current_item_changed', opened_item))
