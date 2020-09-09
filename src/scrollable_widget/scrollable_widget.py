# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, QRect
from PyQt5.QtWidgets import QAbstractScrollArea, QTreeWidget, QTableWidget, QScrollArea, QTextBrowser, \
    QTreeWidgetItem, QStyle

_author_ = 'luwt'
_date_ = '2020/8/24 15:41'


class MyScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, a0):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)

    def leaveEvent(self, a0):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)


class MyTreeWidget(QTreeWidget, MyScrollableWidget):

    # 定义信号，发送点击复选框的树节点和选中状态：全选、部分选、未选择
    item_checkbox_clicked = pyqtSignal(QTreeWidgetItem, int)
    # 作为是否点击复选框标志，方便节点项处理
    checkbox_clicked = False

    def mousePressEvent(self, event):
        """
        鼠标点击事件，点击控件时，判断是否是点击的复选框，复选框需要单独处理，
        其中计算坐标逻辑参考自https://stackoverflow.com/questions/8274123/position-of-icon-in-qtreewidgetitem
        """
        # 当前点击的modelIndex
        clicked_index = self.indexAt(event.pos())
        # 确认是有效索引
        if not clicked_index.isValid():
            return
        # 获取树控件的x位置
        tree_x = self.header().sectionViewportPosition(0)
        # 获取根项目的x坐标，计算其他项目需要这一项
        root_x = self.visualRect(self.rootIndex()).x()
        # 获取点击项所占据的矩形，也就是当前项的可视化矩形大小
        view_rect = self.visualRect(clicked_index)
        # 计算元素的x坐标
        item_x = tree_x + view_rect.x() - root_x
        # 计算复选框的矩形大小
        checkbox_rect = QRect(item_x,
                              view_rect.y(),
                              self.style().pixelMetric(QStyle.PM_IndicatorWidth),
                              view_rect.height())
        # 如果点击位置在复选框范围内
        if checkbox_rect.contains(event.pos()):
            # 标志项置为True
            self.checkbox_clicked = True
        super().mousePressEvent(event)


class MyTableWidget(QTableWidget, MyScrollableWidget):

    # 定义信号，点击第一列复选框时，发送当前选中状态和第二列的字段名称
    item_checkbox_clicked = pyqtSignal(bool, str)


class MyScrollArea(QScrollArea, MyScrollableWidget):
    ...


class MyTextBrowser(QTextBrowser, MyScrollableWidget):
    ...
