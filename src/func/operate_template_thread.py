﻿# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

from src.constant_.constant import COPY_TEMPLATE, DEL_TEMPLATE, OPERATION_FAILED, DEL_ACTION, COPY_ACTION
from src.little_widget.loading_widget import LoadingMask
from src.little_widget.message_box import pop_fail
from src.sys.sys_info_storage.template_sqlite import TemplateSqlite

_author_ = 'luwt'
_date_ = '2020/9/21 16:35'


class OperateTemplateWorker(QThread):

    result = pyqtSignal(bool, object)

    def __init__(self, action, selected_templates):
        super().__init__()
        self.action = action
        self.selected_templates = selected_templates

    def run(self):
        try:
            if self.action == COPY_ACTION:
                self.batch_copy_template()
            elif self.action == DEL_ACTION:
                self.batch_delete_template()
        except Exception as e:
            self.result.emit(False, f'{OPERATION_FAILED}\t\n {e}')

    def batch_copy_template(self):
        templates = TemplateSqlite().batch_copy(self.selected_templates)
        self.result.emit(True, templates)

    def batch_delete_template(self):
        TemplateSqlite().batch_delete(self.selected_templates)
        self.result.emit(True, None)


class OperateTemplate:

    def __init__(self, gui, action, selected_templates):
        # 调用者
        self.gui = gui
        self.loading_mask = LoadingMask(self.gui, ":/gif/loading.gif")
        self.loading_mask.show()
        self.action = action
        self.selected_templates = selected_templates
        self.operate_template()

    def operate_template(self):
        self.worker = OperateTemplateWorker(self.action, list(map(lambda x: x[1], self.selected_templates)))
        self.worker.result.connect(lambda flag, result: self.handle_ui(flag, result))
        self.worker.start()

    def handle_ui(self, flag, result):
        if self.action == COPY_ACTION:
            self.handle_ui_copy(flag, result)
        elif self.action == DEL_ACTION:
            self.handle_ui_delete(flag, result)

    def handle_ui_copy(self, flag, result):
        self.loading_mask.close()
        if flag:
            # 渲染表
            self.gui.fill_table(result, self.gui.tableWidget.rowCount())
            self.gui.table_header.set_header_checked(False)
        else:
            pop_fail(COPY_TEMPLATE, result)

    def handle_ui_delete(self, flag, result):
        if flag:
            self.loading_mask.close()
            delete_rows = sorted(list(map(lambda x: x[0], self.selected_templates)), reverse=True)
            # 已经删除完毕，选中列表可以清除
            self.selected_templates.clear()
            # 删除全选框中的元素
            [self.gui.table_header.all_header_combobox.remove(self.gui.tableWidget.item(row, 0))
             for row in delete_rows]
            # 删除页面行
            [self.gui.tableWidget.removeRow(row) for row in delete_rows]
            self.gui.table_header.set_header_checked(False)
            # 最后一个是最小的行号，在这个行号以后都需要调整
            min_row = delete_rows[-1]
            need_update = (list(range(self.gui.tableWidget.rowCount())))[min_row:]
            if need_update:
                [self.gui.tableWidget.item(row, 0).setText(row + 1) for row in need_update]
                # 重新构建事件
                self.gui.rebuild_pop_menu(need_update)
        else:
            pop_fail(DEL_TEMPLATE, result)

