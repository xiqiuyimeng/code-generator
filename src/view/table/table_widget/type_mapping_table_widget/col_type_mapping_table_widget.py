# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, pyqtSignal

from src.constant.table_constant import DEL_MAPPING_GROUP_BOX_TITLE, DEL_MAPPING_GROUP_PROMPT, \
    DEL_COL_TYPE_MAPPING_PROMPT, DEL_COL_TYPE_MAPPING_TITLE
from src.service.system_storage.col_type_mapping_sqlite import ColTypeMapping
from src.view.box.message_box import pop_question
from src.view.table.table_header.col_type_mapping_table_header import ColTypeMappingTableHeader, \
    ColTypeMappingTableHeaderABC, ColTypeMappingFrozenTableHeader
from src.view.table.table_item.table_item import make_checkbox_num_widget
from src.view.table.table_widget.table_widget_abc import TableWidgetABC

_author_ = 'luwt'
_date_ = '2023/2/15 18:05'


class ColTypeMappingTableWidgetABC(TableWidgetABC):
    
    def __init__(self, *args):
        # 表头控件
        self.header_widget: ColTypeMappingTableHeaderABC = ...
        super().__init__(*args)

    def setup_other_ui(self):
        self.set_column_count()
        # 第一列之后的所有列，设置表格编辑器代理
        self.set_text_input_delegate(range(2, self.columnCount()))
        self.setup_header()
        # 表头高度写死，表头有两行，所以高度定位表头行高度2倍
        self.horizontalHeader().setFixedHeight(self.header_widget.rowHeight(0) << 1)
        # 设置窗口层次，表头始终在表格上方，始终保持视图关系为表头在表格上方
        self.viewport().stackUnder(self.header_widget)
        self.header_widget.show()

    def remove_row(self):
        rm_index_list = list()
        for row in range(self.rowCount()):
            cell_widget = self.cellWidget(row, 0)
            if cell_widget.check_box.checkState():
                rm_index_list.append(row)
        # 执行删除
        [self.removeRow(idx) for idx in sorted(rm_index_list, reverse=True)]
        # 对行进行重排序
        for row in range(self.rowCount()):
            cell_widget = self.cellWidget(row, 0)
            cell_widget.check_label.setText(str(row + 1))

    def set_column_count(self): ...

    def setup_header(self): ...


class ColTypeMappingFrozenTableWidget(ColTypeMappingTableWidgetABC):

    def setup_other_ui(self):
        super().setup_other_ui()
        # 隐藏2列之后的空白列
        [self.setColumnHidden(idx, True) for idx in range(2, self.columnCount())]
        # 关闭滚动条
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_column_count(self):
        # 设置表格2列
        self.setColumnCount(2)

    def setup_header(self):
        # 创建表头控件
        self.header_widget = ColTypeMappingFrozenTableHeader(self, self.parent())

    def resizeEvent(self, e) -> None:
        # 设置表头位置，resize 方法在表格展示的时候会调用，
        # 由于table frame的layout已经清空了边距，所以表头起始点无需移位
        self.header_widget.setGeometry(self.frameWidth(), self.frameWidth(),
                                       self.columnWidth(0) + self.columnWidth(1),
                                       self.horizontalHeader().height())
        super().resizeEvent(e)


class ColTypeMappingTableWidget(ColTypeMappingTableWidgetABC):
    # 表头复选框状态变化信号
    header_check_changed = pyqtSignal(int)

    def __init__(self, *args):
        # 冻结前两列的表格
        self.frozen_column_table: ColTypeMappingFrozenTableWidget = ...
        self.need_sync_col_type = False
        super().__init__(*args)

    def set_column_count(self):
        # 表格设置为5列
        self.setColumnCount(5)

    def setup_header(self):
        # 创建表头控件
        self.header_widget = ColTypeMappingTableHeader(self, self.parent())

    def setup_frozen_table(self):
        if self.frozen_column_table is Ellipsis:
            # 开启同步列类型数据
            self.need_sync_col_type = True
            # 冻结表
            self.frozen_column_table = ColTypeMappingFrozenTableWidget(self.parent())
            # 设置冻结列表格的位置
            self.update_frozen_table_geometry()
            # 当前表视图层次关系为：底表 --> 底表表头 --> 冻结列表格 --> 冻结列表头
            self.header_widget.viewport().stackUnder(self.frozen_column_table)
            self.frozen_column_table.show()

            self.verticalScrollBar().valueChanged.connect(self.frozen_column_table.verticalScrollBar().setValue)
            # 连接冻结表头的信号
            self.frozen_column_table.header_widget.header_clicked.connect(self.link_header_check_state)
            # 转发信号
            self.frozen_column_table.header_widget.header_check_changed.connect(self.header_check_changed.emit)
            # 数据变化信号
            self.frozen_column_table.cellChanged.connect(self.sync_col_type)

    def update_frozen_table_geometry(self):
        # 设置冻结列表格的位置，宽度保持两列宽度，高度应该减去水平滚动条的高度，
        # 由于已经隐藏水平滚动条，如果不减去滚动条高度，将导致冻结列表格实际高度大于底表
        self.frozen_column_table.setGeometry(self.geometry().x(), self.geometry().y(),
                                             self.columnWidth(0) + self.columnWidth(1),
                                             self.geometry().height() - self.horizontalScrollBar().height())

    def link_header_check_state(self, check_state):
        # 冻结表表头复选框状态变化，应该联动底表复选框状态
        self.header_widget.link_header_check_state(check_state)

    def sync_col_type(self, row, col):
        if self.need_sync_col_type and col == 1:
            self.item(row, col).setText(self.frozen_column_table.item(row, col).text())

    def resizeEvent(self, e) -> None:
        # 设置表头位置，resize 方法在表格展示的时候会调用，
        # 由于table frame的layout已经清空了边距，所以表头起始点无需移位
        self.header_widget.setGeometry(self.frameWidth(), self.frameWidth(),
                                       self.viewport().width(), self.horizontalHeader().height())
        # 如果冻结表格存在，同步位置（在回显数据时需要，因为回显数据会处理表结构，也就是会创建冻结表格，并且创建在表格展示之前，
        # 导致其获取到的位置不对，需要在展示表格的时候，更新一次）
        if self.frozen_column_table is not Ellipsis:
            self.update_frozen_table_geometry()
        super().resizeEvent(e)

    def connect_other_signal(self):
        # 转发信号
        self.header_widget.header_check_changed.connect(self.header_check_changed.emit)
        # 连接单元格变化信号
        self.cellChanged.connect(self._cell_change_slot)

    def _cell_change_slot(self, row, col):
        # 当映射列名称 列中的单元格数据变化，且当前单元格被选中时，可以判定单元格刚编辑完成，
        # 此时应该整列所有的单元格，保持数据一致，因为对于映射列名称来说，每一行都应该是一致的
        if (col - 2) % 3 == 0 and self.item(row, col).isSelected():
            mapping_col_name = self.item(row, col).text()
            [self.item(row_idx, col).setText(mapping_col_name) for row_idx in range(self.rowCount())]

    def add_type_mapping(self):
        # 增加一个新的类型映射行
        row = self.rowCount()
        if self.frozen_column_table is not Ellipsis:
            # 不需要向底表同步
            self.need_sync_col_type = False
            self._sync_frozen_col_data()
            self.frozen_column_table.insert_row(row)
            check_box_num_widget = make_checkbox_num_widget(row + 1, self.check_box_clicked_slot)
            self.frozen_column_table.setCellWidget(row, 0, check_box_num_widget)
            self.frozen_column_table.setItem(row, 1, self.make_item())
            self.need_sync_col_type = True
        self.insert_row(row)
        self.setCellWidget(row, 0, make_checkbox_num_widget(row + 1, self.check_box_clicked_slot))
        # 设置每个单元格
        [self.setItem(row, col, self.make_item()) for col in range(self.columnCount())]
        # 重新计算表头复选框状态
        self.calculate_header_checked()
        # 同步上一行所有映射列名称数据
        self._sync_last_mapping_col_text(row)

    def check_box_clicked_slot(self, check_state, row_num):
        # 如果冻结表格存在，那么当前点击的复选框，应当是冻结表，所以需要同步复选框状态到底表
        if self.frozen_column_table is not Ellipsis:
            self.cellWidget(int(row_num) - 1, 0).check_box.setCheckState(check_state)
        # 计算表头复选框状态
        self.calculate_header_checked()

    def calculate_header_checked(self):
        if self.frozen_column_table is not Ellipsis:
            self.frozen_column_table.header_widget.calculate_header_check_state()
        self.header_widget.calculate_header_check_state()

    def _sync_last_mapping_col_text(self, row):
        # 同步上一个映射列名称到当前列下面单元格，需要保持映射列名称一致
        if row > 0:
            # 找出所有映射列名称 列索引
            mapping_col_idx_list = list(filter(lambda x: (x - 2) % 3 == 0, range(2, self.columnCount())))
            for col_idx in mapping_col_idx_list:
                last_mapping_col_name = self.item(row - 1, col_idx).text()
                # 给当前列行赋值
                self.item(row, col_idx).setText(last_mapping_col_name)

    def del_type_mapping(self):
        check_count = list(filter(lambda x:
                                  self.cellWidget(x, 0).check_box.checkState() == Qt.Checked,
                                  range(self.rowCount())))
        if not pop_question(DEL_COL_TYPE_MAPPING_PROMPT.format(len(check_count)), DEL_COL_TYPE_MAPPING_TITLE, self):
            return
        # 移除类型映射行，根据选中情况来删除
        if self.frozen_column_table is not Ellipsis:
            self.frozen_column_table.remove_row()
        self.remove_row()
        self.calculate_header_checked()

    def add_type_mapping_group(self):
        # 增加1组3列
        column_count = self.columnCount()
        [self.insertColumn(col + column_count) for col in range(3)]
        # 设置新增的单元格
        [self.setItem(row, col + column_count, self.make_item()) for col in range(3)
         for row in range(self.rowCount())]
        # 表头同时增加3列
        self.header_widget.add_type_mapping_group()
        # 设置编辑器代理
        self.set_text_input_delegate(range(1, self.columnCount()))

        # 添加类型映射组的时候，考虑构建冻结列表格
        self.setup_frozen_table()

        # 添加类型映射组后，应该考虑数据是否需要同步
        self._sync_frozen_col_data()
        # 重新计算表头复选框状态
        self.calculate_header_checked()

    def del_type_mapping_group(self):
        # 如果当前只有默认映射组，那么不执行删除
        if self.header_widget.max_group_num == 0:
            return
        group_title = self.header_widget.get_mapping_group_title(self.columnCount() - 1)
        if not pop_question(DEL_MAPPING_GROUP_PROMPT.format(group_title),
                            DEL_MAPPING_GROUP_BOX_TITLE, self):
            return
        # 移除最后一个映射组
        column_count = self.columnCount()
        self.removeColumn(column_count - 1)
        self.removeColumn(column_count - 2)
        self.removeColumn(column_count - 3)

        # 移除表头映射组
        self.header_widget.del_type_mapping_group()

    def _sync_frozen_col_data(self):
        # 当前行数
        row = self.rowCount()
        # 如果当前表已经插入过行，冻结列表格需要同步插入，并拷贝数据
        if row > self.frozen_column_table.rowCount():
            for idx in range(self.frozen_column_table.rowCount(), row):
                self.frozen_column_table.insert_row(idx)
                checkbox_num_widget = make_checkbox_num_widget(idx + 1, self.check_box_clicked_slot)
                # 复制底表复选框状态
                checkbox_num_widget.check_box.setCheckState(self.cellWidget(idx, 0).check_box.checkState())
                self.frozen_column_table.setCellWidget(idx, 0, checkbox_num_widget)
                original_item = self.item(idx, 1)
                if original_item:
                    self.frozen_column_table.setItem(idx, 1, self.make_item(original_item.text()))

    def _get_col_type(self, row):
        return self.item(row, 1).text() if self.frozen_column_table is Ellipsis \
            else self.frozen_column_table.item(row, 1).text()

    def _set_col_type_item(self, row, col_type):
        if self.frozen_column_table is not Ellipsis:
            # 不需要向底表同步
            self.need_sync_col_type = False
            self.frozen_column_table.setItem(row, 1, self.make_item(col_type))
            self.need_sync_col_type = True
        self.setItem(row, 1, self.make_item(col_type))

    def sync_col_types(self, col_types):
        exists_col_types = list(map(lambda x: self._get_col_type(x), range(self.rowCount())))
        for idx, col_type in enumerate(col_types):
            if col_type in exists_col_types:
                continue
            self.add_type_mapping()
            self._set_col_type_item(self.rowCount() - 1, col_type)

    def collect_data(self):
        # 收集数据，类型：list [ColTypeMapping]
        col_type_mapping_data: list[ColTypeMapping] = list()
        for row in range(self.rowCount()):
            if self.frozen_column_table is not Ellipsis:
                col_type = self.frozen_column_table.item(row, 1).text()
            else:
                col_type = self.item(row, 1).text()
            # 第一组为固定组
            col_type_mapping_data.append(self.assemble_col_type_mapping_data(row, 0, col_type))
            # 收集额外组数据
            for group_num in range(1, self.header_widget.max_group_num + 1):
                current_group_data = self.assemble_col_type_mapping_data(row, group_num, col_type)
                if current_group_data:
                    col_type_mapping_data.append(current_group_data)
        return col_type_mapping_data

    def assemble_col_type_mapping_data(self, row, group_num, col_type):
        start_col = group_num * 3 + 2
        mapping_col_name = self.item(row, start_col).text()
        mapping_type = self.item(row, start_col + 1).text()
        import_desc = self.item(row, start_col + 2).text()

        col_type_mapping = ColTypeMapping()
        col_type_mapping.ds_col_type = col_type
        if mapping_col_name:
            col_type_mapping.mapping_col_name = mapping_col_name
        if mapping_type:
            col_type_mapping.mapping_type = mapping_type
        if import_desc:
            col_type_mapping.import_desc = import_desc
        col_type_mapping.group_num = group_num
        return col_type_mapping

    def check_fragmentary_data(self):
        """检查表格中，所有映射列名称和映射类型是否已经填写完成，如果没有，应该返回提示"""
        fragmentary_data_prompt_list = list()
        # 首先检查第二列，数据源列类型
        for row_idx in range(self.rowCount()):
            if not self.item(row_idx, 1).text():
                fragmentary_data_prompt_list.append(f'[{self.header_widget.get_ds_col_type_title()}]')
                break
        # 找出所有映射列名称和映射类型 列索引
        mapping_col_idx_list = list(filter(lambda x: (x - 2) % 3 in (0, 1), range(2, self.columnCount())))
        for col_idx in mapping_col_idx_list:
            group_title = self.header_widget.get_mapping_group_title(col_idx)
            if (col_idx - 2) % 3 == 0:
                col_title = self.header_widget.get_mapping_col_name_title()
            else:
                col_title = self.header_widget.get_mapping_type_title()
            for row_idx in range(self.rowCount()):
                if not self.item(row_idx, col_idx).text():
                    fragmentary_data_prompt_list.append(f'[{group_title}]-[{col_title}]')
                    break
        return fragmentary_data_prompt_list

    def fill_table(self, type_mapping):
        max_group_num = type_mapping.max_col_type_group_num
        # 首先渲染表结构，如果最大组号大于0，那么需要新增类型映射组
        if max_group_num:
            [self.add_type_mapping_group() for group_num in range(max_group_num)]
        # 渲染数据
        col_type_mappings = type_mapping.type_mapping_cols
        if not col_type_mappings:
            return
        current_row, current_ds_col_type = -1, ...
        for col_type_mapping in col_type_mappings:
            # 如果列类型不同，那么应当插入下一行
            if current_ds_col_type != col_type_mapping.ds_col_type:
                current_ds_col_type = col_type_mapping.ds_col_type
                self.add_type_mapping()
                current_row += 1
            # 设置列类型
            if col_type_mapping.group_num == 0:
                if self.frozen_column_table is not Ellipsis:
                    # 不需要向底表同步
                    self.need_sync_col_type = False
                    self.frozen_column_table.item(current_row, 1).setText(current_ds_col_type)
                    self.need_sync_col_type = True
                self.item(current_row, 1).setText(current_ds_col_type)
            # 后续按组来赋值，只需要给底表赋值即可
            start_col = col_type_mapping.group_num * 3 + 2
            # 如果是第一行需要赋值映射列名称，其他行在添加行时，会自动复制上一行的数据
            if current_row == 0:
                self.item(current_row, start_col).setText(col_type_mapping.mapping_col_name)
            self.item(current_row, start_col + 1).setText(col_type_mapping.mapping_type)
            self.item(current_row, start_col + 2).setText(col_type_mapping.import_desc)
