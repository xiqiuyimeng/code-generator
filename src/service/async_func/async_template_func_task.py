# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.logger.log import logger as log
from src.service.async_func.async_task_abc import ThreadWorkerABC, LoadingMaskThreadExecutor
from src.service.system_storage.template_func_sqlite import TemplateFunc, TemplateFuncSqlite
from src.view.box.message_box import pop_ok

_author_ = 'luwt'
_date_ = '2023/3/28 11:02'


# ----------------------- 添加模板方法 start ----------------------- #

class AddTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func: TemplateFunc):
        super().__init__()
        self.template_func = template_func

    def do_run(self):
        log.info(f'开始保存模板方法 [{self.template_func.func_name}]')
        TemplateFuncSqlite().save_template_func(self.template_func)
        self.success_signal.emit()
        log.info(f'保存模板方法 [{self.template_func.func_name}] 成功')

    def do_exception(self, e: Exception):
        err_msg = f'保存 [{self.template_func.func_name}] 模板方法信息失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class AddTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func: TemplateFunc, *args):
        self.template_func = template_func
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return AddTemplateFuncWorker(self.template_func)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template_func.func_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 添加模板方法 end ----------------------- #


# ----------------------- 编辑模板方法 start ----------------------- #

class EditTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func: TemplateFunc):
        super().__init__()
        self.template_func = template_func

    def do_run(self):
        log.info(f'开始编辑模板方法信息 [{self.template_func.func_name}]')
        TemplateFuncSqlite().update(self.template_func)
        self.success_signal.emit()
        log.info(f'编辑模板方法信息 [{self.template_func.func_name}] 结束')

    def do_exception(self, e: Exception):
        err_msg = f'编辑模板方法 [{self.template_func.func_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class EditTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func: TemplateFunc, *args):
        self.template_func = template_func
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return EditTemplateFuncWorker(self.template_func)

    def success_post_process(self, *args):
        pop_ok(f'[{self.template_func.func_name}]\n保存成功',
               self.error_box_title, self.window)
        super().success_post_process(*args)


# ----------------------- 编辑模板方法 end ----------------------- #


# ----------------------- 删除模板方法 start ----------------------- #

class DelTemplateFuncWorker(ThreadWorkerABC):

    def __init__(self, template_func_id, template_func_name):
        super().__init__()
        self.template_func_id = template_func_id
        self.template_func_name = template_func_name

    def do_run(self):
        log.info(f'开始删除模板方法 [{self.template_func_name}]')
        TemplateFuncSqlite().delete(self.template_func_id)
        self.success_signal.emit()
        log.info(f'删除模板方法 [{self.template_func_name}] 成功')

    def do_exception(self, e: Exception):
        err_msg = f'删除模板方法 [{self.template_func_name}] 失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class DelTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def __init__(self, template_func_id, template_func_name, *args):
        self.template_func_id = template_func_id
        self.template_func_name = template_func_name
        super().__init__(*args)

    def get_worker(self) -> ThreadWorkerABC:
        return DelTemplateFuncWorker(self.template_func_id, self.template_func_name)


# ----------------------- 删除模板方法 end ----------------------- #

# ----------------------- 清空模板方法 start ----------------------- #

class ClearTemplateFuncWorker(ThreadWorkerABC):

    def do_run(self):
        log.info(f'开始清空模板方法')
        TemplateFuncSqlite().drop_template_func_table()
        self.success_signal.emit()
        log.info(f'清空模板方法成功')

    def do_exception(self, e: Exception):
        err_msg = f'清空模板方法失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ClearTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ClearTemplateFuncWorker()


# ----------------------- 清空模板方法 end ----------------------- #


# ----------------------- 获取模板方法列表 start ----------------------- #

class ListTemplateFuncWorker(ThreadWorkerABC):
    success_signal = pyqtSignal(list)

    def do_run(self):
        log.info("读取模板方法列表")
        template_list = TemplateFuncSqlite().select_by_order(TemplateFunc())
        self.success_signal.emit(template_list)
        log.info("读取模板方法列表成功")

    def do_exception(self, e: Exception):
        err_msg = '读取模板方法列表失败'
        log.exception(err_msg)
        self.error_signal.emit(f'{err_msg}\n{e.args[0]}')


class ListTemplateFuncExecutor(LoadingMaskThreadExecutor):

    def get_worker(self) -> ThreadWorkerABC:
        return ListTemplateFuncWorker()

# ----------------------- 获取模板方法列表 end ----------------------- #

