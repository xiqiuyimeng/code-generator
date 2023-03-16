# -*- coding: utf-8 -*-
from PyQt5.QtCore import QSize, QRect, Qt
from PyQt5.QtGui import QColor, QTextFormat, QPainter
from PyQt5.QtWidgets import QWidget, QTextEdit

from src.view.custom_widget.scrollable_widget import ScrollableTextEdit

_author_ = 'luwt'
_date_ = '2023/3/14 14:45'


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.text_editor = editor

    def sizeHint(self):
        return QSize(self.editor.get_line_number_area_width(), 0)

    def paintEvent(self, event):
        # 交给编辑器来绘制
        self.text_editor.line_number_area_paint_event(event)


class TextEditor(ScrollableTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 行号区域
        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        # 创建编辑器时，需要计算行号区域宽度并突出显示第一行
        self.update_line_number_area_width()
        self.highlight_current_line()

    def get_line_number_area_width(self):
        """该函数计算小部件的宽度。我们将编辑器最后一行中的位数乘以数字的最大宽度"""
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self):
        self.setViewportMargins(self.get_line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """滚动编辑器视口后将调用此槽。作为参数给出的 QRect 是要更新（重绘）的编辑区域的一部分。 保存视图垂直滚动的像素数 dy"""
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width()

    def resizeEvent(self, event):
        """当编辑器的大小发生变化时，我们还需要调整行号区域的大小"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.get_line_number_area_width(), cr.height()))

    def highlight_current_line(self):
        """当光标位置发生变化时，我们突出显示当前行，即包含光标的行"""
        extra_selections = list()
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            # 设置高亮背景色
            line_color = QColor(Qt.blue).lighter(160)

            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            # QPlainTextEdit提供了同时拥有多个选择的可能性。我们可以设置这些选择的字符格式（QTextCharFormat）。
            # 在设置新的QPlainTextEdit：：ExtraSelection之前，我们清除光标选择，否则当用户用鼠标选择多行时，几行将突出显示
            selection.cursor.clearSelection()
            extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

    def line_number_area_paint_event(self, event):
        """每当它收到绘制事件时都会调用 。我们从绘制小部件的背景开始"""
        painter = QPainter(self.lineNumberArea)

        # 现在，我们将遍历所有可见的行，并在每行的额外区域中绘制行号。
        # 请注意，在纯文本编辑中，每行将包含一个 QTextBlock; 但是，如果启用了换行，则一行可能会跨越文本编辑视口中的多行。
        # 我们获取第一个文本块的顶部和底部 y 坐标，并在循环中的每次迭代中根据当前文本块的高度调整这些值。
        # 请注意，除了检查块是否在区域视口中外，我们还检查块是否可见 - 例如，块可以被放置在文本编辑上的窗口隐藏。
        block = self.firstVisibleBlock()
        block_num = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(),
                                 self.fontMetrics().height(), Qt.AlignRight,
                                 str(block_num + 1))

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_num += 1
