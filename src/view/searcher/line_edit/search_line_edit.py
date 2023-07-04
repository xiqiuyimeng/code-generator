# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLineEdit

_author_ = 'luwt'
_date_ = '2022/5/9 19:00'


class SearcherLineEdit(QLineEdit):
    # 编辑文本，新增文本时搜索信号
    search_text_signal = pyqtSignal(str)
    # 清除搜索信号
    clear_search_signal = pyqtSignal()
    # 上下箭头选择信号
    up_down_select_signal = pyqtSignal(int)
    # 回退搜索信号
    back_select_signal = pyqtSignal()

    def __init__(self, dock_widget):
        super().__init__()
        self.dock_widget = dock_widget
        # 原来拥有焦点的控件
        self.search_widget = ...
        self.max_width = ...
        self.origin_text_len = 0
        self.right_palette = self.palette()
        self.textEdited.connect(self.text_edit_slot)

    def set_max_width(self, max_width):
        self.max_width = max_width

    def paint_wrong_color(self):
        wrong_palette = QPalette()
        wrong_palette.setColor(QPalette.Text, Qt.red)
        self.setPalette(wrong_palette)

    def paint_right_color(self):
        self.setPalette(self.right_palette)

    def text_edit_slot(self):
        # 宽度根据文本内容适当调整，但是应有个最大值
        width_hint = self.sizeHint().width()
        if width_hint <= self.max_width:
            self.setFixedWidth(width_hint)
        text_len = len(self.text())
        # 搜索信号，当文本在增加时触发，如果文本在减少，那么应该触发回退搜索信号
        if text_len > self.origin_text_len:
            self.search_text_signal.emit(self.text())
        self.origin_text_len = text_len

    def start_search(self, search_widget):
        self.dock_widget.show()
        self.search_widget = search_widget
        # 设置文本框最大宽度
        self.set_max_width(self.search_widget.width() * 0.75)
        # 转移焦点
        self.search_widget.clearFocus()
        self.setFocus()

    def keyPressEvent(self, event):
        # esc 触发关闭搜索
        if event.key() == Qt.Key_Escape:
            self.clear_search()
        # 上下箭头触发上下选择
        elif event.key() == Qt.Key_Up or event.key() == Qt.Key_Down:
            self.up_down_select_signal.emit(event.key())
        # 左右移动箭头屏蔽，不允许移动光标，home按键屏蔽，不允许移动光标
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Right or event.key() == Qt.Key_Home:
            pass
        # 回退键，触发回退搜索
        elif event.key() == Qt.Key_Backspace:
            self.back_select_signal.emit()
            # 回退也需要触发控件删除文本操作
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def clear_search(self):
        self.clear()
        self.dock_widget.hide()
        # 还原焦点
        self.clearFocus()
        self.search_widget.setFocus()
        self.search_widget = ...
        self.origin_text_len = 0
        self.max_width = ...
        # 发送信号
        self.clear_search_signal.emit()

    def sizeHint(self):
        return QSize(self.fontMetrics().width(self.text()) + self.fontMetrics().maxWidth(),
                     self.fontMetrics().height() + self.fontMetrics().descent())

    def mousePressEvent(self, event):
        # 屏蔽鼠标移动光标能力
        pass

    def mouseMoveEvent(self, event):
        # 屏蔽鼠标选择文本能力
        pass

    def mouseDoubleClickEvent(self, event):
        # 屏蔽双击鼠标选中文本功能
        pass

    def contextMenuEvent(self, event):
        # 屏蔽右键菜单
        pass
