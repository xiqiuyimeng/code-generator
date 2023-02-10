# -*- coding: utf-8 -*-
import threading

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QMovie, QIcon

from src.exception.exception import ThreadStopException
from src.service.system_storage.sqlite_abc import set_thread_terminate
from src.view.box.message_box import pop_fail
from src.view.custom_widget.loading_widget import LoadingMaskWidget, RefreshLoadingMaskWidget
from src.view.tree.tree_item.tree_item_func import get_item_opened_tab, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/5/10 16:46'


# ----------------------- thread worker ABC -----------------------


class ThreadWorkerABC(QThread):
    """异步工作任务基类，定义最基本工作流程"""

    success_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # 标识是否在进行 数据库相关任务
        self.modifying_db_task = False
        self.thread_id = ...

    def run(self):
        try:
            self.thread_id = threading.get_ident()
            self.do_run()
        except Exception as e:
            # 如果是自定义的停止线程异常，那么不需要处理异常，其他异常再进行异常处理
            if not isinstance(e, ThreadStopException):
                self.do_exception(e)
        finally:
            self.do_finally()

    def do_run(self): ...

    def do_exception(self, e: Exception): ...

    def do_finally(self): ...


# ----------------------- thread worker manager ABC -----------------------


class ThreadExecutorABC(QObject):
    """对应 ThreadWorkerABC 设定，负责管理调度异步任务，与view交互工作"""

    def __init__(self, window, error_box_title):
        super().__init__()
        self.window = window
        self.error_box_title = error_box_title

        # 异步任务开始前的准备工作
        self.pre_process()
        # 自定义线程工作对象
        self.worker = self.get_worker()
        # 获取成功失败信息
        self.worker.error_signal.connect(lambda error_msg: self.fail(error_msg))
        self.worker.success_signal.connect(lambda *args: self.success(*args))

    def start(self):
        self.worker.start()

    def success(self, *args):
        self.post_process()
        self.success_post_process(*args)

    def fail(self, error_msg):
        self.post_process()
        self.fail_post_process()
        pop_fail(error_msg, self.error_box_title, self.window)

    def worker_terminate(self, terminate_callback=None):
        if self.worker.isRunning():
            # 如果线程正在处理数据库操作，那么应当抛出异常，使线程中的事务回滚，不产生脏数据
            if self.worker.modifying_db_task:
                # 修改线程内使用连接的标志位，抛出异常，使线程任务结束
                set_thread_terminate(self.worker.thread_id, True)
            else:
                # 如果是普通任务，那么直接停止线程
                self.worker.terminate()
                self.worker.wait()
        # 停止后，首先调用回调函数
        if terminate_callback:
            terminate_callback()
        self.post_process()

    def pre_process(self):
        """前置处理，异步任务开始前的一些准备工作"""
        pass

    def get_worker(self) -> ThreadWorkerABC: ...

    def post_process(self):
        """通用后置处理，任务结束后的一些通用工作"""
        pass

    def success_post_process(self, *args): ...

    def fail_post_process(self): ...


# ----------------------- loading mask thread worker manager ABC -----------------------


class LoadingMaskThreadExecutor(ThreadExecutorABC):
    """使用遮罩层作为任务开始时前置动作的调度器"""

    def __init__(self, masked_widget, *args):
        self.loading_movie = QMovie(":/gif/loading.gif")
        self.masked_widget = masked_widget
        self.loading_mask = LoadingMaskWidget(self.masked_widget, self.loading_movie)
        super().__init__(*args)

    def pre_process(self):
        self.loading_mask.start()

    def post_process(self):
        self.loading_mask.stop()


# ----------------------- icon movie thread worker manager ABC -----------------------


class IconMovieThreadExecutor(ThreadExecutorABC):
    """使用图标动画作为任务开始时前置动作的调度器"""

    def __init__(self, item, *args):
        self.item = item
        self.icon_movie = QMovie(":/gif/loading_simple.gif")
        self.icon = self.item.icon(0)
        super().__init__(*args)

    def pre_process(self):
        self.icon_movie.start()
        self.icon_movie.frameChanged.connect(lambda: self.item.setIcon(0, QIcon(self.icon_movie.currentPixmap())))

    def post_process(self):
        self.icon_movie.stop()
        self.item.setIcon(0, self.icon)


# ----------------------- icon movie and loading mask thread worker manager ABC -----------------------

class IconMovieLoadingMaskThreadExecutor(ThreadExecutorABC):
    """支持使用多个动画，用于多组树节点icon movie + 对应tab的 masked widget，根据给定的item，对所有子节点处理"""

    def __init__(self, item, window, error_box_title, success_callback=None, fail_callback=None):
        self.item = item
        self.success_callback = success_callback
        self.fail_callback = fail_callback
        self.tab_widget = ...
        self.loading_gif = ":/gif/loading.gif"
        self.icon_movie = QMovie(":/gif/loading_simple.gif")
        # 首先获取 item 下所有的子节点，key -> item id, value -> item item_icon tab_dict
        self.item_dict = dict()
        self.get_item_dict(item, window)
        super().__init__(window, error_box_title)

    def get_item_dict(self, item, window):
        # 设置 item 标志
        self.item_pre_process(item)
        # 如果存在子元素，那么当前节点一定不存在tab
        if item.childCount():
            self.item_dict[id(item)] = {
                "item": item,
                "item_icon": item.icon(0),
            }
            for i in range(item.childCount()):
                child_item = item.child(i)
                # 设置 child_item 标志
                self.item_pre_process(child_item)
                self.item_dict[id(child_item)] = {
                    "item": child_item,
                    "item_icon": child_item.icon(0),
                    "tab_dict": self.get_tab_dict(child_item, window)
                }
                # 递归处理
                self.get_item_dict(child_item, window)
        else:
            self.item_dict[id(item)] = {
                "item": item,
                "item_icon": item.icon(0),
                "tab_dict": self.get_tab_dict(item, window)
            }

    def get_tab_dict(self, item, window):
        tab = get_item_opened_tab(item)
        if tab:
            if self.tab_widget is Ellipsis:
                self.tab_widget = tab.parent().parent()
            tab_dict = {
                "tab": tab,
                "tab_icon": self.tab_widget.tabIcon(self.tab_widget.indexOf(tab)),
                "loading_mask": RefreshLoadingMaskWidget(window, tab, QMovie(self.loading_gif))
            }
        else:
            tab_dict = None
        return tab_dict

    def pre_process(self):
        # 开启动画
        self.icon_movie.start()
        self.icon_movie.frameChanged.connect(lambda: self.start_movie(QIcon(self.icon_movie.currentPixmap())))

    def start_movie(self, current_icon):
        for value_dict in self.item_dict.values():
            item = value_dict.get('item')
            tab_dict = value_dict.get('tab_dict')
            if tab_dict:
                tab_index = self.tab_widget.indexOf(tab_dict.get('tab'))
                self.tab_widget.setTabIcon(tab_index, current_icon)
                loading_mask = tab_dict.get('loading_mask')
                loading_mask.start()
            # 首先同步到树节点 icon
            item.setIcon(0, current_icon)

    def post_process(self):
        # 结束动画
        self.icon_movie.stop()
        sorted_values = sorted(self.item_dict.values(),
                               key=lambda x: get_item_opened_record(x.get('item')).level, reverse=True)
        for value_dict in sorted_values:
            self._stop_movie(value_dict)

    def stop_one_movie(self, item):
        # 弹出字典中的元素，停止动画
        self._stop_movie(self.item_dict.pop(id(item)))

    def _stop_movie(self, value_dict):
        item = value_dict.get('item')
        item_icon = value_dict.get('item_icon')
        tab_dict = value_dict.get('tab_dict')
        if tab_dict:
            tab_icon = tab_dict.get('tab_icon')
            loading_mask = tab_dict.get('loading_mask')
            loading_mask.stop()
            self.tab_widget.setTabIcon(self.tab_widget.indexOf(tab_dict.get('tab')), tab_icon)
        item.setIcon(0, item_icon)
        self.item_post_process(item)

    def success_post_process(self, *args):
        if self.success_callback:
            self.success_callback(*args)

    def fail_post_process(self):
        if self.fail_callback:
            self.fail_callback()

    def item_pre_process(self, item): ...

    def item_post_process(self, item): ...


# ----------------------- refresh movie worker manager ABC -----------------------

class RefreshMovieThreadExecutor(IconMovieLoadingMaskThreadExecutor):

    def __init__(self, tree_widget, *args):
        self.tree_widget = tree_widget
        super().__init__(*args)

    def item_pre_process(self, item):
        node = self.tree_widget.get_item_node(item)
        node.is_refreshing = True
        # 隐藏节点复选框
        node.hide_check_box()

    def item_post_process(self, item):
        node = self.tree_widget.get_item_node(item)
        node.is_refreshing = False
        # 在每个节点调用的时候，都触发下减少父节点记录的刷新节点数
        self.sub_parent_refreshed_child_count(item)
        node.show_check_box()

    def pre_process(self):
        # 在开启线程时进行
        # 以当前节点为顶级节点，记录其下子节点刷新节点数
        self.add_child_refreshed_child_count(self.item)
        # 从当前节点向上传递刷新节点数
        self.add_parent_refreshed_child_count()
        super().pre_process()

    def add_parent_refreshed_child_count(self):
        # 向上传递刷新节点数的变化
        parent_item = self.item.parent()
        if parent_item:
            self.tree_widget.get_item_node(parent_item).add_refreshing_child_count()

    def add_child_refreshed_child_count(self, item):
        # 找出当前节点下刷新节点数，递归向下处理
        child_count = item.childCount()
        if child_count:
            for idx in range(child_count):
                child_item = item.child(idx)
                child_node = self.tree_widget.get_item_node(child_item)
                # 只记录正在刷新的节点
                if not child_node.is_refreshing:
                    continue
                self.tree_widget.get_item_node(item).refreshing_child_count += 1
                # 递归处理子节点
                self.add_child_refreshed_child_count(child_item)

    def sub_parent_refreshed_child_count(self, item):
        # 向上传递刷新节点数的变化
        parent_item = item.parent()
        if parent_item:
            self.tree_widget.get_item_node(parent_item).sub_refreshing_child_count()
