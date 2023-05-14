# -*- coding: utf-8 -*-
import dataclasses

from PyQt5.QtCore import pyqtSignal

from src.constant.export_import_constant import TYPE_MAPPING_DATA_KEY
from src.logger.log import logger as log
from src.service.async_func.async_import_export_task import ImportDataWorker, ImportDataExecutor, ExportDataWorker, \
    ExportDataExecutor, OverrideDataWorker, OverrideDataExecutor
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.col_type_mapping_sqlite import ColTypeMappingSqlite, ImportExportColTypeMapping, \
    ColTypeMapping
from src.service.system_storage.conn_type import check_conn_type
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.struct_type import check_struct_type
from src.service.system_storage.type_mapping_sqlite import TypeMappingSqlite, TypeMapping, ImportExportTypeMapping
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
        type_mapping = TypeMappingSqlite().get_type_mapping_by_id(self.type_mapping_id)
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
            ColTypeMappingSqlite().batch_save(self.type_mapping.type_mapping_cols, self.type_mapping.id)
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


# ----------------------- 导入类型映射 start ----------------------- #

class ImportTypeMappingWorker(ImportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TYPE_MAPPING_DATA_KEY
        self.type_mapping_sqlite = TypeMappingSqlite()
        self.col_type_mapping_sqlite = ColTypeMappingSqlite()
        self.exists_type_mapping_names = ...

    def convert_to_model(self, import_data):
        # 之所以要经历两次转化，是为了规范数据
        import_type_mapping = ImportExportTypeMapping().convert_import(**import_data)
        # 第二次转为可插入数据库的实体
        type_mapping = TypeMapping(**dataclasses.asdict(import_type_mapping))
        if import_type_mapping.type_mapping_cols:
            import_cols = [ImportExportColTypeMapping().convert_import(**col)
                           for col in import_type_mapping.type_mapping_cols]
            import_type_mapping.type_mapping_cols = import_cols
            type_mapping.type_mapping_cols = [ColTypeMapping(**col)
                                              for col in type_mapping.type_mapping_cols]
        return type_mapping

    def get_unique_key(self, row: TypeMapping) -> str:
        # 获取唯一键，标识数据唯一性
        return row.mapping_name

    def pre_process_before_check_data(self):
        # 查出所有的类型映射名称
        self.exists_type_mapping_names = self.type_mapping_sqlite.get_all_mapping_names()

    def check_data_exists(self, unique_key) -> bool:
        return unique_key in self.exists_type_mapping_names

    def check_data_legal(self, data_row: TypeMapping) -> bool:
        # 前面已经检查过了映射名称，现在检查数据源类型是否合法
        data_row_legal = data_row.ds_type and (check_conn_type(data_row.ds_type)
                                               or check_struct_type(data_row.ds_type))
        if not data_row_legal:
            return data_row_legal
        # 检查映射列类型
        if data_row.type_mapping_cols:
            # 映射组
            mapping_col_group_dict = dict()
            for col in data_row.type_mapping_cols:
                # 1. 数据源列类型不能为空
                if not col.ds_col_type:
                    return False
                # 2. 组号必须存在，且为大于0的整数
                if col.group_num is None or not isinstance(col.group_num, int) or col.group_num < 0:
                    return False
                # 3. 映射类型必须存在
                if not col.mapping_type:
                    return False
                # 4. 映射列名称不能为空
                if not col.mapping_col_name:
                    return False
                # 放入组内
                mapping_col_list = mapping_col_group_dict.get(col.group_num)
                if not mapping_col_list:
                    mapping_col_list = list()
                    mapping_col_group_dict[col.group_num] = mapping_col_list
                mapping_col_list.append(col)

            # 5. 组号必须为连续的整数
            for group_num in range(len(mapping_col_group_dict)):
                if group_num not in mapping_col_group_dict:
                    return False
            # 6. 映射列名称，同组内相同，不同组保持唯一性；数据源列类型不同组必须相同
            group_mapping_col_name_set, ds_col_type_set = set(), set()
            for group_num, mapping_col_list in mapping_col_group_dict.items():
                if len(set([mapping_col.mapping_col_name for mapping_col in mapping_col_list])) != 1:
                    return False
                # 判断映射列名称是否重复
                current_group_mapping_col_name = mapping_col_list[0].mapping_col_name
                if current_group_mapping_col_name in group_mapping_col_name_set:
                    return False
                group_mapping_col_name_set.add(current_group_mapping_col_name)

                # 7. 数据源列类型同组内保持唯一性，不同组必须相同
                current_ds_col_type_set = set([mapping_col.ds_col_type for mapping_col in mapping_col_list])
                # 同组保持不同
                if len(current_ds_col_type_set) != len(mapping_col_list):
                    return False
                if not ds_col_type_set:
                    ds_col_type_set = current_ds_col_type_set
                # 不同组需要保持相同
                if current_ds_col_type_set != ds_col_type_set:
                    return False
        return True

    @transactional
    def import_data(self, data_list):
        # 批量保存类型映射
        self.type_mapping_sqlite.batch_save_type_mappings(data_list)
        # 保存列类型映射组信息
        for type_mapping in data_list:
            if type_mapping.type_mapping_cols:
                self.col_type_mapping_sqlite.batch_save(type_mapping.type_mapping_cols, type_mapping.id)

    def get_err_msg(self) -> str:
        return '导入类型映射失败'


class ImportTypeMappingExecutor(ImportDataExecutor):

    def get_worker(self) -> ImportTypeMappingWorker:
        return ImportTypeMappingWorker(self.file_path)

# ----------------------- 导入类型映射 end ----------------------- #


# ----------------------- 覆盖数据 start ----------------------- #

class OverrideTypeMappingWorker(OverrideDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.type_mapping_sqlite = TypeMappingSqlite()
        self.col_type_mapping_sqlite = ColTypeMappingSqlite()

    def batch_delete_origin_data(self):
        id_list = self.type_mapping_sqlite.get_id_by_names(self.data_list)
        self.type_mapping_sqlite.batch_delete(id_list)
        self.col_type_mapping_sqlite.delete_by_parent_ids(id_list)

    def batch_insert_data_list(self):
        # 批量保存类型映射
        self.type_mapping_sqlite.batch_save_type_mappings(self.data_list)
        # 保存列类型映射组信息
        for type_mapping in self.data_list:
            if type_mapping.type_mapping_cols:
                self.col_type_mapping_sqlite.batch_save(type_mapping.type_mapping_cols, type_mapping.id)


class OverrideTypeMappingExecutor(OverrideDataExecutor):

    def get_worker(self) -> OverrideTypeMappingWorker:
        return OverrideTypeMappingWorker(self.data_list)

# ----------------------- 覆盖数据 end ----------------------- #


# ----------------------- 导出类型映射 start ----------------------- #

class ExportTypeMappingWorker(ExportDataWorker):

    def __init__(self, *args):
        super().__init__(*args)
        self.data_key = TYPE_MAPPING_DATA_KEY

    def export_data(self) -> list[dict]:
        # 查询类型映射信息
        type_mapping_list = TypeMappingSqlite().export_type_mapping_by_ids(self.row_ids)
        if not type_mapping_list:
            raise Exception('未获取到类型映射信息')
        # 根据类型映射id查询类型映射组信息
        col_type_mapping_list = ColTypeMappingSqlite().export_by_parent_ids(self.row_ids)
        # 对映射组信息分组
        if col_type_mapping_list:
            col_type_mapping_dict = dict()
            for col_type_mapping in col_type_mapping_list:
                col_type_mappings = col_type_mapping_dict.get(col_type_mapping.parent_id)
                # 如果之前没存储过，那么创建list
                if col_type_mappings is None:
                    col_type_mappings = list()
                    col_type_mapping_dict[col_type_mapping.parent_id] = col_type_mappings
                col_type_mappings.append(col_type_mapping)
            # 类型映射匹配映射组信息
            for type_mapping in type_mapping_list:
                type_mapping.type_mapping_cols = col_type_mapping_dict.get(type_mapping.id)
        return [dataclasses.asdict(x) for x in type_mapping_list]

    def get_err_msg(self) -> str:
        return '导出类型映射失败'


class ExportTypeMappingExecutor(ExportDataExecutor):

    def get_worker(self) -> ExportTypeMappingWorker:
        return ExportTypeMappingWorker(self.row_ids, self.file_path)

# ----------------------- 导出类型映射 end ----------------------- #
