# -*- coding: utf-8 -*-
"""
自定义表头类，实现了复选框全选功能
"""
from PyQt5 import QtWidgets, QtCore
_author_ = 'luwt'
_date_ = '2020/6/21 9:21'


class CheckBoxHeader(QtWidgets.QHeaderView):
    """自定义表头类，参考自 https://www.pythonf.cn/read/108150"""

    # 自定义 复选框全选信号
    select_all_clicked = QtCore.pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False
        # 用来放所有复选框
        self.all_header_combobox = list()

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2)

        if logicalIndex == 0:
            option = QtWidgets.QStyleOptionButton()
            option.rect = QtCore.QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QtWidgets.QStyle.State_Enabled | QtWidgets.QStyle.State_Active
            if self.isOn:
                option.state |= QtWidgets.QStyle.State_On
            else:
                option.state |= QtWidgets.QStyle.State_Off
            self.style().drawControl(QtWidgets.QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width \
                    and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.isOn:
                    self.isOn = False
                else:
                    self.isOn = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.isOn)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 仅仅作为修改所有单元格复选框状态的方法，不作为槽方法
    def change_state(self, isOn):
        # 如果行表头复选框为勾选状态
        if isOn:
            # 将所有的复选框都设为勾选状态
            for i in self.all_header_combobox:
                i.setCheckState(QtCore.Qt.Checked)
        else:
            for i in self.all_header_combobox:
                i.setCheckState(QtCore.Qt.Unchecked)

    def set_header_checked(self, checked):
        if checked:
            self.isOn = True
            # 更新表头控件
            self.updateSection(0)
        else:
            self.isOn = False
            # 更新表头控件
            self.updateSection(0)
