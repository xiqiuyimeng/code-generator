# -*- coding: utf-8 -*-
from PyQt5.QtCore import QModelIndex, QRect
from PyQt5.QtWidgets import QItemDelegate, QWidget, QStyleOptionViewItem, QComboBox

from src.view.custom_widget.scrollable_widget import ScrollableTextEdit

_author_ = 'luwt'
_date_ = '2022/10/11 17:54'


class ComboboxDelegate(QItemDelegate):

    def __init__(self):
        super().__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        """创建编辑器，只有在编辑时才会触发，编辑器控件选择combox"""
        combox = QComboBox(parent)
        combox.addItem('是')
        combox.addItem('否')
        combox.setCurrentIndex(1)
        return combox


class TextInputDelegate(QItemDelegate):

    def __init__(self):
        super().__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        """创建编辑器，只有在编辑时才会触发，编辑器控件选择combox"""
        text_edit = ScrollableTextEdit(parent)
        return text_edit

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        """调整文本输入框位置，编辑框高度变大"""
        editor.setGeometry(QRect(option.rect.x(), option.rect.y(), option.rect.width(), option.rect.height() << 2))

