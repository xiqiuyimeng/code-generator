# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtWidgets import QHeaderView, QStyleOptionButton, QStyle

_author_ = 'luwt'
_date_ = '2022/5/10 15:12'


class CheckBoxHeader(QHeaderView):
    """自定义复选框表头类"""

    # 自定义 表头复选框状态
    header_check_state = pyqtSignal(int)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        # 标识未选中状态
        self.check_state = Qt.Unchecked
        # 用来放所有复选框
        self.checkbox_list = list()

    def paintSection(self, painter, rect, index):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, index)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2)

        if index == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.check_state == Qt.Checked:
                option.state |= QStyle.State_On
            elif self.check_state == Qt.PartiallyChecked:
                option.state |= QStyle.State_NoChange
            elif self.check_state == Qt.Unchecked:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == 0:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width \
                    and self._y_offset < event.pos().y() < self._y_offset + self._height:
                # 鼠标点击只有两种状态，全选和未选中
                # 如果之前的状态是未选中或部分选中，那么点击后，应该是全选
                if self.check_state == Qt.Unchecked or self.check_state == Qt.PartiallyChecked:
                    self.check_state = Qt.Checked
                # 如果之前的状态是选中，点击后应该是未选中
                elif self.check_state == Qt.Checked:
                    self.check_state = Qt.Unchecked
                    # 当用户点击了行表头复选框，发射 自定义信号 header_check_state
                self.header_check_state.emit(self.check_state)
                self.change_state(self.check_state)
                # 调用表格控件中批量保存复选框数据方法
                self.parent().batch_update_check_state(self.check_state)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 仅仅作为修改所有单元格复选框状态的方法，不作为槽方法
    def change_state(self, check_state):
        # 如果行表头复选框为勾选状态
        if check_state == Qt.Checked:
            # 将所有的复选框都设为勾选状态
            for checkbox in self.checkbox_list:
                if checkbox.checkState() != Qt.Checked:
                    checkbox.setCheckState(Qt.Checked)
        elif check_state == Qt.Unchecked:
            for checkbox in self.checkbox_list:
                if checkbox.checkState() != Qt.Unchecked:
                    checkbox.setCheckState(Qt.Unchecked)

    def set_header_checked(self, check_state):
        if check_state == Qt.Unchecked:
            self.check_state = Qt.Unchecked
            # 更新表头控件
            self.updateSection(0)
        elif check_state == Qt.PartiallyChecked:
            self.check_state = Qt.PartiallyChecked
            # 更新表头控件
            self.updateSection(0)
        elif check_state == Qt.Checked:
            self.check_state = Qt.Checked
            # 更新表头控件
            self.updateSection(0)

    def change_header_state(self, check_state):
        # 1.由树节点调用，当点击树节点复选框时，联动表复选框，2.点击子表所在父行复选框，触发子表复选框变化
        self.set_header_checked(check_state)
        self.change_state(check_state)

    def link_header_checked(self):
        # 判断列表中所有项的选中状态，以决定表头复选框状态
        len_checked_list = len(list(filter(lambda x: x.checkState() == Qt.Checked, self.checkbox_list)))
        len_partially_checked_list = len(list(filter(
            lambda x: x.checkState() == Qt.PartiallyChecked, self.checkbox_list)))
        len_checkbox = len(self.checkbox_list)
        check_state = Qt.Unchecked
        if len_checked_list == len_checkbox:
            check_state = Qt.Checked
        elif len_checked_list == 0:
            # 如果没有全选复选框，存在部分选中复选框，那么应该为部分选中状态，否则为未选中
            if len_partially_checked_list:
                check_state = Qt.PartiallyChecked
            else:
                check_state = Qt.Unchecked
        elif len_checked_list < len_checkbox:
            check_state = Qt.PartiallyChecked
        self.set_header_checked(check_state)
        # 发射当前选中状态信号
        self.header_check_state.emit(check_state)

