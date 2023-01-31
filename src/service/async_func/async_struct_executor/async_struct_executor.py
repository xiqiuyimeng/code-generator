# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from constant.constant import FOLDER_TYPE
from logger.log import logger as log
from service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor, IconMovieThreadExecutor, \
    RefreshMovieThreadExecutor
from service.system_storage.ds_table_col_info_sqlite import DsTableColInfoSqlite
from service.system_storage.ds_table_tab_sqlite import DsTableTabSqlite, DsTableTab
from service.system_storage.sqlite_abc import transactional
from service.system_storage.struct_sqlite import StructSqlite
from service.util.struct_util import *
from view.tree.tree_item.tree_item_func import get_item_opened_tab, get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/12/5 15:35'


# ---------------------------------------- 异步美化结构体 start ---------------------------------------- #

class PrettyStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(str)

    def __init__(self, data, beautifier_executor_type):
        super().__init__()
        self.data = data
        self.beautifier_executor_type = beautifier_executor_type

    def do_run(self):
        # 解析美化
        beautifier_executor = globals()[self.beautifier_executor_type](self.data)
        result = beautifier_executor.beautify()
        self.success_signal.emit(result)

    def do_exception(self, e: Exception):
        err_msg = '美化结构体失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class PrettyStructExecutor(LoadingMaskThreadExecutor):

    def __init__(self, data, beautifier_executor_type, masked_widget, window, callback):
        self.data = data
        self.beautifier_executor_type = beautifier_executor_type
        self.callback = callback
        super().__init__(masked_widget, window, f'美化结构体')

    def get_worker(self) -> ThreadWorkerABC:
        return PrettyStructWorker(self.data, self.beautifier_executor_type)

    def success_post_process(self, *args):
        self.callback(*args)


# ---------------------------------------- 异步美化结构体 end ---------------------------------------- #


# ---------------------------------------- 打开结构体 start ---------------------------------------- #

class OpenStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, opened_table_item):
        super().__init__()
        self.opened_table_item = opened_table_item
        self.struct_parser_type = opened_table_item.data_type.parse_executor
        self.struct_info = ...
        self.table_tab_id = ...

    def do_run(self):
        # 读取结构体内容
        self.struct_info = StructSqlite().get_struct_info(self.opened_table_item.id)
        if self.struct_info:
            # 解析转化
            struct_parser: StructParser = globals()[self.struct_parser_type](self.struct_info.content)
            column_list = struct_parser.parse()
            if not column_list:
                # 如果不能解析出结果，那么应该返回错误
                raise Exception('解析结构体结果为空')
            table_tab = self.save_parse_result(column_list)
            self.success_signal.emit(table_tab)
        else:
            self.success_signal.emit(DsTableTab())

    @transactional
    def save_parse_result(self, column_list):
        self.modifying_db_task = True
        # 存储tab信息
        table_tab = DsTableTabSqlite().add_tab(self.opened_table_item)
        self.table_tab_id = table_tab.id
        table_tab.col_list = column_list
        # 保存列信息, 选中状态与树节点保持一致
        DsTableColInfoSqlite().save_cols(column_list, self.table_tab_id,
                                         self.opened_table_item.checked,
                                         parent_id=0)
        self.modifying_db_task = False
        return table_tab

    def do_exception(self, e: Exception):
        err_msg = f'打开{self.opened_table_item.item_name}失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class OpenStructExecutor(IconMovieThreadExecutor):

    def __init__(self, item, window, callback, fail_callback):
        self.item = item
        self.callback = callback
        self.fail_callback = fail_callback
        super().__init__(item, window, '打开结构体')

    def get_worker(self) -> ThreadWorkerABC:
        return OpenStructWorker(get_item_opened_record(self.item))

    def success_post_process(self, *args):
        self.callback(*args)

    def fail_post_process(self):
        self.fail_callback()

# ---------------------------------------- 打开结构体 end ---------------------------------------- #


# ---------------------------------------- 刷新结构体 start ---------------------------------------- #

class RefreshStructWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(DsTableTab)

    def __init__(self, struct_parser_type, table_tab):
        super().__init__()
        self.struct_parser_type = struct_parser_type
        self.table_tab = table_tab
        self.struct_info = ...

    def do_run(self):
        """重写run方法，实现刷新逻辑"""
        # 读取结构体内容
        self.struct_info = StructSqlite().get_struct_info(self.table_tab.parent_opened_id)
        if self.struct_info:
            # 解析转化
            struct_parser: StructParser = globals()[self.struct_parser_type](self.struct_info.content)
            column_list = struct_parser.parse()
            if not column_list:
                # 如果不能解析出结果，那么应该返回错误
                raise Exception('刷新失败，解析结构体结果为空')
            self.refresh_struct(column_list)
            self.success_signal.emit(self.table_tab)
        else:
            raise Exception('查询不到结构体信息')

    @transactional
    def refresh_struct(self, column_list):
        self.modifying_db_task = True
        # 保存新的列信息
        DsTableColInfoSqlite().refresh_tab_cols(self.table_tab.id, column_list)
        self.table_tab.col_list = column_list
        self.modifying_db_task = False

    def do_exception(self, e: Exception):
        err_msg = f'刷新 [{self.struct_info.struct_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class RefreshStructExecutor(RefreshMovieThreadExecutor):

    def __init__(self, tree_widget, item, window, table_tab, success_callback):
        self.table_tab = table_tab
        super().__init__(tree_widget, item, window, '刷新结构体', success_callback)

    def get_worker(self) -> ThreadWorkerABC:
        struct_parser_type = get_item_opened_record(self.item).data_type.parse_executor
        return RefreshStructWorker(struct_parser_type, self.table_tab)


# ---------------------------------------- 刷新结构体 end ---------------------------------------- #


# ---------------------------------------- 刷新文件夹 start ---------------------------------------- #

class RefreshFolderWorker(ThreadWorkerABC):
    refresh_item_signal = pyqtSignal(tuple)

    def __init__(self, struct_items, folder_name):
        super().__init__()
        self.struct_items = struct_items
        self.folder_name = folder_name
        self.struct_sqlite = StructSqlite()
        self.table_info_sqlite = DsTableColInfoSqlite()

    def do_run(self):
        # 循环处理
        for item, opened_record, table_tab in self.struct_items:
            struct_parser_type = opened_record.data_type.parse_executor
            struct_info = self.struct_sqlite.get_struct_info(opened_record.id)
            if struct_info:
                struct_parser = globals()[struct_parser_type](struct_info.content)
                column_list = struct_parser.parse()
                if not column_list:
                    # 错误处理
                    raise Exception(f'刷新失败，解析结构体结果为空: [{struct_info.struct_name}]')
                self.refresh_struct(column_list, table_tab)
                # 发射当前成功结构体信号
                self.refresh_item_signal.emit((item, table_tab))
            else:
                # 如果查不到结构体信息，发射错误信号
                raise Exception(f'查询不到结构体信息: [{struct_info.struct_name}]')
        self.success_signal.emit()

    @transactional
    def refresh_struct(self, column_list, table_tab):
        self.modifying_db_task = True
        # 保存新的列信息
        DsTableColInfoSqlite().refresh_tab_cols(table_tab.id, column_list)
        table_tab.col_list = column_list
        self.modifying_db_task = False

    def do_exception(self, e: Exception):
        err_msg = f'刷新 [{self.folder_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class RefreshFolderExecutor(RefreshMovieThreadExecutor):

    def __init__(self, tree_widget, item, window, refresh_item_callback):
        self.struct_items, self.folder_items = list(), list()
        self.get_refresh_items(item)
        # 如果没有需要刷新的结构体节点，那么直接结束
        if not self.struct_items:
            return
        super().__init__(tree_widget, item, window, '刷新文件夹')

        self.worker.refresh_item_signal.connect(refresh_item_callback)

    def get_refresh_items(self, item):
        """获取需要刷新的节点，只搜索打开表的结构体节点及其上层节点"""
        opened_record = get_item_opened_record(item)
        # 如果是文件夹节点
        if opened_record.data_type.type == FOLDER_TYPE:
            if item.childCount():
                refresh_flag = False
                for index in range(item.childCount()):
                    child_item = item.child(index)
                    refresh_flag |= self.get_refresh_items(child_item)
                if refresh_flag:
                    # 如果当前文件夹下存在刷新的节点，那么当前节点也需要刷新
                    self.folder_items.append(item)
                    # 将标志位返回
                    return True
        else:
            # 对于结构体节点，尝试获取tab
            opened_tab = get_item_opened_tab(item)
            if opened_tab:
                self.struct_items.append((item, opened_record, opened_tab.table_tab), )
                return True
        return False

    def get_item_dict(self, item, window):
        """重写父方法，实现自定义获取item dict"""
        for folder_item in self.folder_items:
            # 设置 item 标志位
            self.item_dict[id(folder_item)] = {
                "item": folder_item,
                "item_icon": folder_item.icon(0),
            }
        for struct_values in self.struct_items:
            struct_item = struct_values[0]
            self.item_dict[id(struct_item)] = {
                "item": struct_item,
                "item_icon": struct_item.icon(0),
                "tab_dict": self.get_tab_dict(struct_item, window)
            }

    def get_worker(self) -> ThreadWorkerABC:
        return RefreshFolderWorker(self.struct_items, self.item.text(0))

# ---------------------------------------- 刷新文件夹 end ---------------------------------------- #
