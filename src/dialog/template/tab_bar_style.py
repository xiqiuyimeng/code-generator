# -*- coding: utf-8 -*-
from PyQt5.QtCore import QRect, QPoint
from PyQt5.QtWidgets import QStyle, QStyleOptionTab, QTabBar, QStylePainter, QTabWidget

_author_ = 'luwt'
_date_ = '2020/9/22 17:29'


class TabBar(QTabBar):

    def __init__(self, parent):
        super().__init__(parent)

    def tabSizeHint(self, index):
        s = QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QStylePainter(self)
        opt = QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QRect(QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            # 旋转90度
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QStyle.CE_TabBarTabLabel, opt)
            painter.restore()


class TabWidget(QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)
        self.setTabBar(TabBar(self))
        # 选项卡在标签的右侧
        self.setTabPosition(QTabWidget.West)
