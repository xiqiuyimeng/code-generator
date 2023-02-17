# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal

from src.constant.constant import ADD_FOLDER_TITLE, EDIT_FOLDER_TITLE, DEL_STRUCT_TITLE
from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from src.service.system_storage.ds_table_tab_sqlite import DsTableTab, DsTableTabSqlite
from src.service.system_storage.ds_category_sqlite import DsCategoryEnum
from src.service.system_storage.opened_tree_item_sqlite import OpenedTreeItemSqlite, OpenedTreeItem
from src.service.system_storage.sqlite_abc import transactional
from src.service.system_storage.struct_sqlite import StructSqlite, StructInfo
from src.service.system_storage.struct_type import FolderTypeEnum, get_struct_type
from src.view.box.message_box import pop_ok
from src.view.tree.tree_item.tree_item_func import get_item_opened_record, get_children_opened_ids

_author_ = 'luwt'
_date_ = '2022/11/21 13:03'


# ---------------------------------------- 添加结构体 start ---------------------------------------- #

class AddStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(OpenedTreeItem)

    def __init__(self, struct_info: StructInfo, parent_opened_item: OpenedTreeItem):
        super().__init__()
        self.struct_info = struct_info
        self.parent_opened_item = parent_opened_item

    @transactional
    def do_run(self):
        # 保存打开记录
        opened_struct = OpenedTreeItemSqlite().add_struct_opened_item(self.struct_info.struct_name,
                                                                      self.parent_opened_item.id,
                                                                      self.parent_opened_item.level + 1)
        # 保存结构体信息
        self.struct_info.opened_item_id = opened_struct.id
        StructSqlite().insert(self.struct_info)
        opened_struct.data_type = get_struct_type(self.struct_info.struct_type)
        log.info(f'[{self.struct_info.struct_name}]保存成功')
        self.success_signal.emit(opened_struct)

    def do_exception(self, e: Exception):
        err_msg = f'添加{self.struct_info.struct_type}失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class AddStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, struct_info: StructInfo,
                 parent_opened_item: OpenedTreeItem,
                 masked_widget, window, callback):
        self.struct_info = struct_info
        self.parent_opened_item = parent_opened_item
        self.callback = callback
        super().__init__(masked_widget, window, f'保存{struct_info.struct_type}')

    def get_worker(self) -> ThreadWorkerABC:
        return AddStructWorker(self.struct_info, self.parent_opened_item)

    def success_post_process(self, *args):
        pop_ok(f'[{self.struct_info.struct_name}]\n保存{self.struct_info.struct_type}成功',
               f'保存{self.struct_info.struct_type}', self.window)
        self.callback(*args)


# ---------------------------------------- 添加结构体 end ---------------------------------------- #


# ---------------------------------------- 删除结构体 start ---------------------------------------- #

class DelStructWorker(ThreadWorkerABC):

    def __init__(self, opened_item, reorder_items):
        super().__init__()
        self.opened_item = opened_item
        self.reorder_items = reorder_items

    @transactional
    def do_run(self):
        # 删除结构体
        StructSqlite().delete_by_opened_item_id(self.opened_item.id)
        # 删除 opened item 记录
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.delete(self.opened_item.id)
        # 重新排序需要排序的 opened item
        opened_tree_item_sqlite.reorder_opened_items(self.reorder_items)
        log.info(f'{self.opened_item.item_name}删除成功')
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'[{self.opened_item.item_name}]删除失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class DelStructExecutor(IconMovieThreadExecutor):

    def __init__(self, item, opened_item, reorder_items, callback, window):
        self.opened_item = opened_item
        self.reorder_items = reorder_items
        self.callback = callback
        super().__init__(item, window, DEL_STRUCT_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return DelStructWorker(self.opened_item, self.reorder_items)
    
    def success_post_process(self, *args):
        self.callback()


# ---------------------------------------- 删除结构体 end ---------------------------------------- #


# ---------------------------------------- 编辑结构体 start ---------------------------------------- #

class EditStructWorker(ThreadWorkerABC):

    def __init__(self, struct_info: StructInfo):
        super().__init__()
        self.struct_info = struct_info

    @transactional
    def do_run(self):
        # 更新结构体
        StructSqlite().update(self.struct_info)
        # 更新打开记录
        update_param = OpenedTreeItem()
        update_param.id = self.struct_info.opened_item_id
        update_param.item_name = self.struct_info.struct_name
        OpenedTreeItemSqlite().update(update_param)
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'修改{self.struct_info.struct_type}失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class EditStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, struct_info: StructInfo, masked_widget, window, callback):
        self.struct_info = struct_info
        self.callback = callback
        super().__init__(masked_widget, window, f'修改{struct_info.struct_type}')

    def get_worker(self) -> ThreadWorkerABC:
        return EditStructWorker(self.struct_info)

    def success_post_process(self, *args):
        pop_ok(f'[{self.struct_info.struct_name}]\n修改{self.struct_info.struct_type}成功',
               f'修改{self.struct_info.struct_type}', self.window)
        self.callback(*args)


# ---------------------------------------- 编辑结构体 end ---------------------------------------- #

# ---------------------------------------- 查询结构体 start ---------------------------------------- #

class QueryStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(StructInfo)

    def __init__(self, opened_struct_id):
        super().__init__()
        self.opened_struct_id = opened_struct_id

    def do_run(self):
        struct_info = StructSqlite().get_struct_info(self.opened_struct_id)
        if struct_info:
            self.success_signal.emit(struct_info)
        else:
            self.success_signal.emit(StructInfo())

    def do_exception(self, e: Exception):
        err_msg = '查询结构体失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class QueryStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, opened_struct_id, callback, masked_widget, window):
        self.opened_struct_id = opened_struct_id
        self.callback = callback
        super().__init__(masked_widget, window, '查询结构体')

    def get_worker(self) -> ThreadWorkerABC:
        return QueryStructWorker(self.opened_struct_id)

    def success_post_process(self, *args):
        self.callback(*args)

# ---------------------------------------- 查询结构体 end ---------------------------------------- #


# ---------------------------------------- 获取所有结构体 start ---------------------------------------- #

class ListStructWorker(ThreadWorkerABC):
    # 打开表中的查询结果，包含文件夹和结构体保存记录
    opened_items_signal = pyqtSignal(list)
    # 结构体表中查询结果
    struct_list_signal = pyqtSignal(list)
    # tab页表信息查询结果
    tab_info_signal = pyqtSignal(list)

    def do_run(self):
        folder_type = FolderTypeEnum.folder_type.value
        # 读取结构体具体信息
        struct_info_list = StructSqlite().select_list()
        # 转换为dict，key：opened_item_id，value：struct info
        struct_opened_dict = dict(map(lambda x: (x.opened_item_id, x), struct_info_list))

        ds_category = DsCategoryEnum.struct_ds_category.value.name
        # 读取打开记录表中的信息，获取所有的文件夹和结构体记录
        opened_item_sqlite = OpenedTreeItemSqlite()
        max_level = opened_item_sqlite.get_max_level(ds_category)
        children_generator = opened_item_sqlite.recursive_get_children(0, 0, ds_category, max_level)
        for children in children_generator:
            for child in children:
                # 设置结构体类型
                if child.id in struct_opened_dict:
                    child.data_type = struct_opened_dict.get(child.id).struct_type_info
                else:
                    child.data_type = folder_type
            self.opened_items_signal.emit(children)

        # 读取tab信息
        self.get_tab_cols()
        log.info('获取所有结构体成功')

    def get_tab_cols(self):
        tab_param = DsTableTab()
        tab_param.ds_category = DsCategoryEnum.struct_ds_category.value.name
        tab_list = DsTableTabSqlite().select_by_order(tab_param)
        for tab in tab_list:
            tab.col_list = DsTableColInfoSqlite().get_tab_cols(tab.id)
        self.tab_info_signal.emit(tab_list)

    def do_finally(self):
        # 结束信号
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = '获取所有结构体失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, reopen_items_callback, reopen_tab_callback, reopen_end_callback, masked_widget, window):
        self.reopen_end_callback = reopen_end_callback
        super().__init__(masked_widget, window, '获取所有结构体列表')

        self.reopen_items_callback = reopen_items_callback
        self.reopen_tab_callback = reopen_tab_callback

        self.worker.opened_items_signal.connect(self.reopen_items_callback)
        self.worker.tab_info_signal.connect(self.reopen_tab_callback)

    def get_worker(self) -> ThreadWorkerABC:
        return ListStructWorker()

    def success_post_process(self):
        self.reopen_end_callback()

    def fail_post_process(self):
        self.reopen_end_callback()


# ---------------------------------------- 获取所有结构体 end ---------------------------------------- #


# ---------------------------------------- 添加结构体文件夹 start ---------------------------------------- #

class AddFolderWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(OpenedTreeItem)

    def __init__(self, folder_name, parent_id, level):
        self.folder_name = folder_name
        self.parent_id = parent_id
        self.level = level
        super().__init__()

    def do_run(self):
        opened_item = OpenedTreeItemSqlite().add_struct_opened_item(self.folder_name,
                                                                    self.parent_id,
                                                                    self.level)
        opened_item.data_type = FolderTypeEnum.folder_type.value
        self.success_signal.emit(opened_item)

    def do_exception(self, e: Exception):
        error_msg = f'[{self.folder_name}]\n添加文件夹失败'
        log.exception(error_msg)
        self.error_signal.emit(f'{error_msg}\n{e.args[0]}')


class AddFolderExecutor(LoadingMaskThreadExecutor):

    def __init__(self, folder_name, parent_id, level, masked_widget, window, callback):
        self.folder_name = folder_name
        self.parent_id = parent_id
        self.level = level
        self.callback = callback
        super().__init__(masked_widget, window, ADD_FOLDER_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return AddFolderWorker(self.folder_name, self.parent_id, self.level)

    def success_post_process(self, *args):
        pop_ok(f'[{self.folder_name}]\n添加文件夹成功', ADD_FOLDER_TITLE, self.window)
        self.callback(*args)


# ---------------------------------------- 添加结构体文件夹 end ---------------------------------------- #


# ---------------------------------------- 编辑结构体文件夹 start ---------------------------------------- #

class EditFolderWorker(ThreadWorkerABC):

    def __init__(self, folder_item):
        super().__init__()
        self.folder_item = folder_item

    def do_run(self):
        OpenedTreeItemSqlite().update(self.folder_item)
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        error_msg = f'[{self.folder_item.item_name}]\n编辑文件夹失败'
        log.exception(error_msg)
        self.error_signal.emit(f'{error_msg}\n{e.args[0]}')


class EditFolderExecutor(LoadingMaskThreadExecutor):

    def __init__(self, folder_item: OpenedTreeItem, masked_widget, window, callback):
        self.folder_item = folder_item
        self.callback = callback
        super().__init__(masked_widget, window, EDIT_FOLDER_TITLE)

    def get_worker(self) -> ThreadWorkerABC:
        return EditFolderWorker(self.folder_item)

    def success_post_process(self, *args):
        pop_ok(f'[{self.folder_item.item_name}]\n编辑文件夹成功', EDIT_FOLDER_TITLE, self.window)
        self.callback(*args)


# ---------------------------------------- 编辑结构体文件夹 end ---------------------------------------- #


# ---------------------------------------- 删除结构体文件夹 start ---------------------------------------- #

class DelFolderWorker(ThreadWorkerABC):

    def __init__(self, folder_name, delete_opened_ids, reorder_items, tab_ids):
        super().__init__()
        self.folder_name = folder_name
        self.delete_opened_ids = delete_opened_ids
        self.reorder_items = reorder_items
        self.tab_ids = tab_ids

    @transactional
    def do_run(self):
        # 删除当前文件夹下所有结构体，包括当前文件夹
        StructSqlite().delete_by_opened_item_ids(self.delete_opened_ids)
        # 删除 opened item 记录
        opened_tree_item_sqlite = OpenedTreeItemSqlite()
        opened_tree_item_sqlite.batch_delete(self.delete_opened_ids)
        # 对被影响到的连接项进行重排序
        if self.reorder_items:
            opened_tree_item_sqlite.reorder_opened_items(self.reorder_items)
        if self.tab_ids:
            # 删除tab
            DsTableTabSqlite().batch_delete(self.tab_ids)
            # 删除 数据列信息
            DsTableColInfoSqlite().delete_by_parent_tab_ids(self.tab_ids)
        self.success_signal.emit()

    def do_exception(self, e: Exception):
        err_msg = f'删除文件夹 [{self.folder_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class DelFolderExecutor(IconMovieThreadExecutor):

    def __init__(self, folder_name, reorder_items, tab_indexes,
                 tab_ids, callback, item, window):
        self.folder_name = folder_name
        self.reorder_items = reorder_items
        self.tab_indexes = tab_indexes
        self.tab_ids = tab_ids
        self.callback = callback
        super().__init__(item, window, '删除文件夹')

    def get_worker(self) -> ThreadWorkerABC:
        # 获取要删除的节点对象
        opened_record = get_item_opened_record(self.item)
        # 获取子节点所有id
        delete_opened_ids = get_children_opened_ids(self.item)
        delete_opened_ids.append(opened_record.id)
        return DelFolderWorker(self.folder_name, delete_opened_ids,
                               self.reorder_items, self.tab_ids)

    def success_post_process(self, *args):
        self.callback(self.tab_indexes)


# ---------------------------------------- 删除结构体文件夹 end ---------------------------------------- #


# ---------------------------------------- 异步读取文件 start ---------------------------------------- #

class ReadFileWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(int, str)

    def __init__(self, file_url, struct_type):
        super().__init__()
        self.file_url = file_url
        self.struct_type = struct_type

    def do_run(self):
        with open(self.file_url, 'r', encoding='utf-8') as f:
            for index, line in enumerate(f):
                self.success_signal.emit(index, line.rstrip("\n"))

    def do_exception(self, e: Exception):
        err_msg = f'读取文件失败：[{self.file_url}]'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ReadFileExecutor(LoadingMaskThreadExecutor):

    def __init__(self, file_url, struct_type, masked_widget, window, callback):
        self.file_url = file_url
        self.struct_type = struct_type
        self.callback = callback
        super().__init__(masked_widget, window, f'读取{self.struct_type}文件')

    def get_worker(self) -> ThreadWorkerABC:
        return ReadFileWorker(self.file_url, self.struct_type)

    def success_post_process(self, *args):
        self.callback(*args)

# ---------------------------------------- 异步读取文件 end ---------------------------------------- #
