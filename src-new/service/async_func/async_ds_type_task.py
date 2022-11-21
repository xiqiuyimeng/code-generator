# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from service.system_storage.sqlite_abc import transactional
from service.util.ds_type_util import get_current_datasource_type
from service.system_storage.ds_type_sqlite import DatasourceTypeSqlite, DatasourceType, DatasourceTypeEnum

from logger.log import logger as log

_author_ = 'luwt'
_date_ = '2022/9/26 18:33'


# ----------------------- 初始化 datasource type start ----------------------- #
class InitDsTypeWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    @transactional
    def do_run(self):
        log.info("读取数据源类型列表")
        datasource_types = self.get_ds_types()
        # 返回数据
        self.success_signal.emit(datasource_types)

    def get_ds_types(self):
        ds_types = DatasourceTypeSqlite().select_by_order(DatasourceType())
        # 如果不能查到数据，或数据不正确，都应重新初始化
        if not ds_types or not get_current_datasource_type(ds_types):
            return self.init_ds_types()
        return ds_types

    def init_ds_types(self):
        # 上述条件不满足，则进行初始化，将库里原有数据清空，初始化数据
        log.info("数据源类型列表数据初始化")
        DatasourceTypeSqlite().drop_table()
        datasource_types = list()
        for ds_type in DatasourceTypeEnum:
            datasource_types.append(ds_type.value)
        DatasourceTypeSqlite().batch_insert(datasource_types)
        return self.get_ds_types()


class InitDsTypeExecutor(LoadingMaskThreadExecutor):

    def __init__(self, callback, *args):
        self.callback = callback
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return InitDsTypeWorker()

    def success_post_process(self, *args):
        self.callback(*args)


# ----------------------- 初始化 datasource type end ----------------------- #

# ----------------------- 切换 datasource type start ----------------------- #

class SwitchDsTypeWorker(InitDsTypeWorker):

    def __init__(self, switch_ds_type):
        super().__init__()
        self.switch_ds_type = switch_ds_type

    def do_run(self):
        log.info(f'切换数据源类型 ==> {self.switch_ds_type}')
        DatasourceTypeSqlite().switch_ds_type(self.switch_ds_type)
        super().do_run()

    def do_exception(self, e: Exception):
        # 记录错误日志
        log.exception('切换数据源类型失败')
        self.error_signal.emit('切换数据源类型失败')


class SwitchDsTypeExecutor(LoadingMaskThreadExecutor):

    def __init__(self, switch_ds_type, callback, *args):
        self.switch_ds_type = switch_ds_type
        self.callback = callback
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return SwitchDsTypeWorker(self.switch_ds_type)

    def success_post_process(self, *args):
        self.callback(*args)

# ----------------------- 切换 datasource type end ----------------------- #
