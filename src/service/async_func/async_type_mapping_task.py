# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.col_type_mapping_sqlite import ColTypeMappingSqlite
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.type_mapping_sqlite import TypeMappingSqlite, TypeMapping
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/2/13 9:05'


# ----------------------- 读取类型映射信息 start ----------------------- #

class ReadTypeMappingWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(TypeMapping)

    def __init__(self, type_mapping_id):
        super().__init__()
        self.type_mapping_id = type_mapping_id

    def do_run(self):
        log.info("开始读取类型映射详细信息")
        # 查询类型映射信息
        param = TypeMapping()
        param.id = self.type_mapping_id
        type_mapping = TypeMappingSqlite().select_one(param)
        if not type_mapping:
            raise Exception('未查询到类型映射信息')
        # 查询列类型映射组信息
        type_mapping.type_mapping_cols = ColTypeMappingSqlite().get_by_parent_id(self.type_mapping_id)
        self.success_signal.emit(type_mapping)
        log.info("读取类型映射详细信息成功")

    def get_err_msg(self) -> str:
        return '读取类型映射信息失败'


class ReadTypeMappingExecutor(LoadingMaskThreadExecutor):

    def __init__(self, type_mapping_id, *args):
        self.type_mapping_id = type_mapping_id
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return ReadTypeMappingWorker(self.type_mapping_id)

# ----------------------- 读取类型映射信息 end ----------------------- #


# ----------------------- 添加类型映射 start ----------------------- #

class AddTypeMappingWorker(ThreadWorkerABC):
    
    def __init__(self, type_mapping: TypeMapping):
        super().__init__()
        self.type_mapping = type_mapping

    @transactional
    def do_run(self):
        log.info(f'开始保存类型映射 [{self.type_mapping.mapping_name}]')
        # 保存类型映射，首先保存类型映射信息
        TypeMappingSqlite().save_type_mapping(self.type_mapping)
        # 保存列类型映射组信息
        if self.type_mapping.type_mapping_cols:
            for col_type_mapping in self.type_mapping.type_mapping_cols:
                col_type_mapping.parent_id = self.type_mapping.id
            ColTypeMappingSqlite().save_col_type_mappings(self.type_mapping.type_mapping_cols)
        self.success_signal.emit()
        log.info(f'保存类型映射 [{self.type_mapping.mapping_name}] 成功')

    def get_err_msg(self) -> str:
        return f'保存 [{self.type_mapping.mapping_name}] 类型映射信息失败'


class AddTypeMappingExecutor(LoadingMaskThreadExecutor):
    
    def __init__(self, type_mapping: TypeMapping, *args):
        self.type_mapping = type_mapping
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AddTypeMappingWorker(self.type_mapping)

    def success_post_process(self, *args):
        pop_ok(f'[{self.type_mapping.mapping_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)

# ----------------------- 添加类型映射 end ----------------------- #


# ----------------------- 编辑类型映射 start ----------------------- #

class EditTypeMappingWorker(ThreadWorkerABC):

    def __init__(self, type_mapping: TypeMapping):
        super().__init__()
        self.type_mapping = type_mapping

    @transactional
    def do_run(self):
        log.info(f'开始编辑类型映射信息 [{self.type_mapping.mapping_name}]')
        # 首先更新类型映射信息
        TypeMappingSqlite().update(self.type_mapping)
        # 处理列类型映射信息
        ColTypeMappingSqlite().edit_col_type_mappings(self.type_mapping.type_mapping_cols, self.type_mapping.id)
        self.success_signal.emit()
        log.info(f'编辑类型映射信息 [{self.type_mapping.mapping_name}] 结束')

    def get_err_msg(self) -> str:
        return f'编辑类型映射 [{self.type_mapping.mapping_name}] 失败'


class EditTypeMappingExecutor(LoadingMaskThreadExecutor):

    def __init__(self, type_mapping: TypeMapping, *args):
        self.type_mapping = type_mapping
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return EditTypeMappingWorker(self.type_mapping)

    def success_post_process(self, *args):
        pop_ok(f'[{self.type_mapping.mapping_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)

# ----------------------- 编辑类型映射 end ----------------------- #


# ----------------------- 删除类型映射 start ----------------------- #

class DelTypeMappingWorker(ThreadWorkerABC):

    def __init__(self, type_mapping_ids, type_mapping_names):
        super().__init__()
        self.type_mapping_ids = type_mapping_ids
        self.type_mapping_names = type_mapping_names

    @transactional
    def do_run(self):
        log.info(f'开始删除类型映射 [{self.type_mapping_names}]')
        # 首先删除类型映射
        TypeMappingSqlite().batch_delete(self.type_mapping_ids)
        ColTypeMappingSqlite().delete_by_parent_ids(self.type_mapping_ids)
        self.success_signal.emit()
        log.info(f'删除类型映射 [{self.type_mapping_names}] 成功')

    def get_err_msg(self) -> str:
        return f'删除类型映射 [{self.type_mapping_names}] 失败'


class DelTypeMappingExecutor(LoadingMaskThreadExecutor):

    def __init__(self, type_mapping_id, type_mapping_name, row_index, *args):
        self.type_mapping_id = type_mapping_id
        self.type_mapping_name = type_mapping_name
        self.row_index = row_index
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTypeMappingWorker((self.type_mapping_id, ), (self.type_mapping_name, ))

    def success_post_process(self, *args):
        self.success_callback(self.row_index)


class BatchDelTypeMappingExecutor(LoadingMaskThreadExecutor):

    def __init__(self, type_mapping_ids, type_mapping_names, *args):
        self.type_mapping_ids = type_mapping_ids
        self.type_mapping_names = type_mapping_names
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTypeMappingWorker(self.type_mapping_ids, self.type_mapping_names)

# ----------------------- 删除类型映射 end ----------------------- #


# ----------------------- 获取类型映射列表 start ----------------------- #

class ListTypeMappingWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info("读取类型映射列表")
        # 读取数据库中缓存的类型映射列表
        type_mapping_list = TypeMappingSqlite().select_by_order(TypeMapping())
        self.success_signal.emit(type_mapping_list)
        log.info("读取类型映射列表成功")

    def get_err_msg(self) -> str:
        return '读取类型映射列表失败'


class ListTypeMappingExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ListTypeMappingWorker()

# ----------------------- 获取类型映射列表 end ----------------------- #
