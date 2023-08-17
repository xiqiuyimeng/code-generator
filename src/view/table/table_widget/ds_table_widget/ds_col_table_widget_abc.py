# -*- coding: utf-8 -*-

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView, QWidget

from src.constant.constant import COMBO_BOX_YES_TXT, COMBO_BOX_NO_TXT
from src.constant.table_constant import DS_TABLE_HEADER_LABELS
from src.service.async_func.async_tab_table_task import AsyncSaveTabObjExecutor
from src.service.system_storage.ds_table_col_info_sqlite import DsTableColInfo
from src.view.table.table_header.check_box_table_header import CheckBoxHeader
from src.view.table.table_item.table_item_delegate import ComboboxDelegate, TextInputDelegate
from src.view.table.table_widget.table_widget_abc import TableWidgetABC

_author_ = 'luwt'
_date_ = '2022/12/6 15:50'


class DsColTableWidgetABC(TableWidgetABC):

    def __init__(self, tree_widget, parent, cols):
        self.tree_widget = tree_widget
        self.cols = cols
        # 获取tab widget中的队列线程执行器
        self.async_save_executor = self.get_async_save_executor()
        # 选中数据
        self.tree_data = self.tree_widget.tree_data
        self.tree_item = parent.tree_item
        self.table_header: CheckBoxHeader = ...
        # 保存代理引用
        self.combox_delegate: ComboboxDelegate = ...
        self.text_input_delegate: TextInputDelegate = ...
        super().__init__(parent)

    def get_async_save_executor(self) -> AsyncSaveTabObjExecutor:
        return self.tree_widget.get_current_tab_widget().async_save_executor

    def setup_other_ui(self):
        # 设置表格列数
        self.setColumnCount(6)
        # 实例化自定义表头
        self.table_header = self.get_header(DS_TABLE_HEADER_LABELS)
        # 表头高度写死
        self.horizontalHeader().setFixedHeight(self.table_header.rowHeight(0))
        # 设置窗口层次，表头在表格上方
        self.viewport().stackUnder(self.table_header)

        # 设置表头列宽度，第一列全选列
        self.horizontalHeader().resizeSection(0, 80)
        # 第二列字段列，根据大小自动调整宽度
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        # 最后备注列拉伸到最大
        self.horizontalHeader().setStretchLastSection(True)

        # 设置第五列（是否是主键）combox代理项，在编辑时触发
        self.combox_delegate = ComboboxDelegate()
        self.setItemDelegateForColumn(4, self.combox_delegate)
        # 第2,3,4,6列设置编辑代理项
        self.text_input_delegate = TextInputDelegate()
        for col in (1, 2, 3, 5):
            self.setItemDelegateForColumn(col, self.text_input_delegate)

    def get_header(self, header_labels) -> CheckBoxHeader:
        ...

    def resizeEvent(self, e) -> None:
        self.table_header.setGeometry(self.frameWidth(), self.frameWidth(),
                                      self.viewport().width(), self.horizontalHeader().height())
        # 表头每列的宽度，应该跟表格内每列宽度一致
        for col in range(self.columnCount()):
            self.table_header.horizontalHeader().resizeSection(col, self.columnWidth(col))
        super().resizeEvent(e)

    def connect_other_signal(self):
        # 单行数据变化时，触发
        self.itemChanged.connect(self.data_change)
        # 连接表头复选框点击信号，向下传递选中状态，例如父表表头选中，对应子表表头也应选中
        self.table_header.header_clicked.connect(self.batch_deal_checked)

    def data_change(self, item):
        # 保存数据
        self.save_data(item.row(), item.column(), item.text())

    def batch_deal_checked(self, check_state):
        # 调用批量处理方法保存数据
        self.batch_update_check_state(self.cols, check_state)

    def fill_table(self):
        """
        根据列数据构建表格
        """
        # 屏蔽信号
        self.blockSignals(True)
        # 填充数据
        for i, col in enumerate(self.cols):
            # 插入新的一行
            self.insert_row(i)
            # 设置checkbox在第一列
            self.setCellWidget(i, 0, self.make_checkbox_num_widget(i, col))

            self.setItem(i, 1, self.make_item(col.col_name))
            self.setItem(i, 2, self.make_item(col.data_type))
            self.setItem(i, 3, self.make_item(col.full_data_type))
            self.setItem(i, 4, self.make_item(COMBO_BOX_YES_TXT if col.is_pk else COMBO_BOX_NO_TXT))
            self.setItem(i, 5, self.make_item(col.col_comment if col.col_comment else ''))

        # 后置处理
        self.fill_post_process()
        # 处理表头复选框
        self.table_header.calculate_header_check_state()
        # 表格填充完毕再恢复信号
        self.blockSignals(False)

    def make_checkbox_num_widget(self, row_index, col_data) -> QWidget:
        ...

    def fill_post_process(self):
        ...

    def add_checked_data(self, cols):
        ...

    def remove_checked_data(self, cols):
        ...

    def remove_all_table_checked(self, cols):
        ...

    def update_checked_data(self, col_data):
        ...

    def click_row_checkbox(self, checked, row):
        row = int(row) - 1
        # 将列数据置为选中状态，保存数据
        self.save_data(row, 0, checked.value)
        # 联动表头
        self.table_header.calculate_header_check_state()

    def save_data(self, row, col, data):
        # 根据row找到对应的列信息数据
        col_data = self.cols[row]
        modify_col_data = DsTableColInfo()
        modify_col_data.id = col_data.id

        if col == 0:
            col_data.checked = data
            modify_col_data.checked = data

            # 保存到树选中数据中，由于保存的列对象是从 self.cols中取的，
            # 所以树中保存的列对象引用指向列表中对象，在数据变化时，无需手动同步
            # 如果是选中，则为添加数据，否则为删除数据
            # 当复选框状态变化时，再处理添加或删除选中数据
            if col_data.checked:
                self.add_checked_data(col_data)
            else:
                self.remove_checked_data(col_data)
        elif col == 1:
            col_data.col_name = data
            modify_col_data.col_name = data

            # 当名称变化时，需要同步更新选中数据
            if col_data.checked:
                self.update_checked_data(col_data)
        elif col == 2:
            col_data.data_type = data
            modify_col_data.data_type = data
        elif col == 3:
            col_data.full_data_type = data
            modify_col_data.full_data_type = data
        elif col == 4:
            is_pk = 1 if data == COMBO_BOX_YES_TXT else 0
            col_data.is_pk = is_pk
            modify_col_data.is_pk = is_pk
        elif col == 5:
            col_data.col_comment = data
            modify_col_data.col_comment = data

        # 保存数据
        self.async_save_executor.save_table_data(modify_col_data)

    def batch_update_check_state(self, cols, check_state):
        modify_col_data_list = list()
        for col in cols:
            if col.checked != check_state.value:
                col.checked = check_state.value
                modify_col_data = DsTableColInfo()
                modify_col_data.id = col.id
                modify_col_data.checked = check_state.value
                modify_col_data_list.append(modify_col_data)
        if not modify_col_data_list:
            return
        # 保存数据
        self.async_save_executor.batch_save_data(modify_col_data_list)
        # 批量选中数据或取消选中
        if check_state == Qt.CheckState.Unchecked:
            self.remove_all_table_checked(cols)
        elif check_state == Qt.CheckState.Checked:
            self.add_checked_data(cols)
