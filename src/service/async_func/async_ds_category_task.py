# -*- coding: utf-8 -*-
from PyQt6.QtCore import pyqtSignal

from src.constant.window_constant import SWITCH_DS_CATEGORY_TITLE
from src.enum.ds_category_enum import get_ds_category_list
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.ds_category_sqlite import DsCategorySqlite
from src.service.util.ds_category_util import get_current_ds_category
from src.service.util.system_storage_util import transactional

_author_ = 'luwt'
_date_ = '2022/9/26 18:33'


# ----------------------- 初始化 datasource category start ----------------------- #
class InitDsCategoryWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.ds_category_sqlite = ...

    def do_run(self):
        log.info('读取数据源种类列表')
        if self.ds_category_sqlite is Ellipsis:
            self.ds_category_sqlite = DsCategorySqlite()
        ds_categories = self.get_ds_categories()
        # 返回数据
        self.success_signal.emit(ds_categories)
        log.info('读取数据源种类列表成功')

    def get_ds_categories(self):
        ds_categories = self.ds_category_sqlite.select_by_order()
        # 如果不能查到数据，或数据不正确，都应重新初始化
        if not ds_categories or not get_current_ds_category(ds_categories):
            return self.init_ds_categories()
        return ds_categories

    @transactional
    def init_ds_categories(self):
        # 上述条件不满足，则进行初始化，将库里原有数据清空，初始化数据
        log.info('数据源种类列表数据初始化')
        self.ds_category_sqlite.drop_table()
        DsCategorySqlite().batch_insert(get_ds_category_list())
        log.info('数据源种类列表数据初始化成功')
        return self.get_ds_categories()


class InitDsCategoryExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return InitDsCategoryWorker()


# ----------------------- 初始化 datasource category end ----------------------- #

# ----------------------- 切换 datasource category start ----------------------- #

class SwitchDsCategoryWorker(InitDsCategoryWorker):

    def __init__(self, switch_ds_category):
        super().__init__()
        self.switch_ds_category = switch_ds_category

    @transactional
    def do_run(self):
        log.info(f'{SWITCH_DS_CATEGORY_TITLE} {self.switch_ds_category}')
        self.ds_category_sqlite = DsCategorySqlite()
        self.ds_category_sqlite.switch_ds_category(self.switch_ds_category)
        super().do_run()
        log.info(f'{SWITCH_DS_CATEGORY_TITLE} {self.switch_ds_category} 成功')

    def get_err_msg(self) -> str:
        return f'{SWITCH_DS_CATEGORY_TITLE} {self.switch_ds_category} 失败'


class SwitchDsCategoryExecutor(LoadingMaskThreadExecutor):

    def __init__(self, switch_ds_category, *args):
        self.switch_ds_category = switch_ds_category
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return SwitchDsCategoryWorker(self.switch_ds_category)

# ----------------------- 切换 datasource category end ----------------------- #
