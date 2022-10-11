# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt, QRect
from PyQt5.QtWidgets import QHeaderView, QStyleOptionButton, QStyle

_author_ = 'luwt'
_date_ = '2022/5/10 15:12'


class CheckBoxHeader(QHeaderView):
    """自定义表头类，参考自 https://www.pythonf.cn/read/108150"""

    # 自定义 复选框全选信号
    select_all_clicked = pyqtSignal(bool)
    # 这4个变量控制列头复选框的样式，位置以及大小
    _x_offset = 3
    _y_offset = 0
    _width = 20
    _height = 20

    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.is_on = False
        # 用来放所有复选框
        self.all_header_combobox = list()

    def paintSection(self, painter, rect, index):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, index)
        painter.restore()

        self._y_offset = int((rect.height() - self._width) / 2)

        if index == 0:
            option = QStyleOptionButton()
            option.rect = QRect(rect.x() + self._x_offset, rect.y() + self._y_offset, self._width, self._height)
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.is_on:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if 0 == index:
            x = self.sectionPosition(index)
            if x + self._x_offset < event.pos().x() < x + self._x_offset + self._width \
                    and self._y_offset < event.pos().y() < self._y_offset + self._height:
                if self.is_on:
                    self.is_on = False
                else:
                    self.is_on = True
                    # 当用户点击了行表头复选框，发射 自定义信号 select_all_clicked()
                self.select_all_clicked.emit(self.is_on)
                self.change_state(self.is_on)

                self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)

    # 仅仅作为修改所有单元格复选框状态的方法，不作为槽方法
    def change_state(self, on):
        # 如果行表头复选框为勾选状态
        if on:
            # 将所有的复选框都设为勾选状态
            for i in self.all_header_combobox:
                i.setCheckState(Qt.Checked)
        else:
            for i in self.all_header_combobox:
                i.setCheckState(Qt.Unchecked)

    def set_header_checked(self, checked):
        if checked:
            self.is_on = True
            # 更新表头控件
            self.updateSection(0)
        else:
            self.is_on = False
            # 更新表头控件
            self.updateSection(0)
