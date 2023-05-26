# -*- coding: utf-8 -*-
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtWidgets import QItemDelegate, QWidget, QStyleOptionViewItem, QComboBox

from src.constant.constant import COMBO_BOX_YES_TXT, COMBO_BOX_NO_TXT
from src.view.dialog.table_item_delegate.table_item_input_delegate_dialog import TableItemInputDelegateDialog

_author_ = 'luwt'
_date_ = '2022/10/11 17:54'


class ComboboxDelegate(QItemDelegate):

    def __init__(self, value_list=None, default_idx=None):
        self.value_list = value_list if value_list else [COMBO_BOX_YES_TXT, COMBO_BOX_NO_TXT]
        self.default_idx = default_idx if default_idx is not None else 1
        super().__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        """创建编辑器，只有在编辑时才会触发，编辑器控件选择combox"""
        combox = QComboBox(parent)
        combox.addItems(self.value_list)
        combox.setCurrentIndex(self.default_idx)
        return combox


class TextInputDelegate(QItemDelegate):

    def __init__(self, duplicate_prompt=None, get_exists_data_list_func=None):
        # 数据重复提示语
        self.duplicate_prompt = duplicate_prompt
        # 获取不重复数据列表的方法
        self.get_exists_data_list_func = get_exists_data_list_func
        self.input_dialog: TableItemInputDelegateDialog = ...
        # 新数据
        self.new_data = ...
        super().__init__()

    def createEditor(self, parent: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex) -> QWidget:
        """创建编辑器，只有在编辑时才会触发，编辑器控件选择combox"""
        self.input_dialog = TableItemInputDelegateDialog(index.row(), index.column(),
                                                         bool(self.get_exists_data_list_func),
                                                         self.duplicate_prompt)
        self.input_dialog.setModal(True)
        self.input_dialog.save_signal.connect(self.update_new_data)
        return self.input_dialog

    def update_new_data(self, data):
        self.new_data = data

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        """将模型中的数据，赋值到对话框中"""
        if self.get_exists_data_list_func:
            self.input_dialog.frame.set_exists_data_list(self.get_exists_data_list_func(index))
        self.input_dialog.frame.echo_dialog_data(index.model().data(index))

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex) -> None:
        """提交对话框的数据到模型中，只要对话框关闭就会触发，所以这里需要判断是否是对话框保存后触发的"""
        if self.new_data is not Ellipsis:
            model.setData(index, self.new_data)
            # 提交数据到模型后，将当前单元格数据重置
            self.new_data = ...

    def updateEditorGeometry(self, editor: QWidget, option: 'QStyleOptionViewItem', index: QModelIndex):
        """调整文本输入对话框位置"""
        editor.resize_dialog()
