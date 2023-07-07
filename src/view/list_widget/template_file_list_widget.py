# -*- coding: utf-8 -*-
from PyQt6.QtWidgets import QListWidgetItem

from src.constant.list_constant import TEMPLATE_TYPE_NAME, EDIT_FILE_BOX_TITLE
from src.enum.common_enum import CurrentEnum, TabOpenedEnum
from src.view.list_widget.custom_list_widget import CustomListWidget
from src.view.list_widget.list_item_func import get_template_file_data, set_template_file_data

_author_ = 'luwt'
_date_ = '2023/3/12 9:55'


class TemplateFileListWidget(CustomListWidget):

    def __init__(self, parent_dialog, edit_file_name_func, *args):
        self.parent_dialog = parent_dialog
        self.edit_file_name_func = edit_file_name_func
        super().__init__(TEMPLATE_TYPE_NAME, *args)

    def connect_signal(self):
        super().connect_signal()
        # 双击
        self.doubleClicked.connect(self.open_tab)

    def fill_list_widget(self, template_files):
        for template_file in template_files:
            self.add_list_file_item(template_file)

    def open_tab(self, idx):
        current_text = self.itemFromIndex(idx).text()
        current_tab_indexes = self.search_tab(current_text)
        if current_tab_indexes:
            index = current_tab_indexes[0]
            self.parent_dialog.file_tab_widget.setCurrentIndex(index)
        else:
            self.parent_dialog.file_tab_widget.add_file_tab(get_template_file_data(self.currentItem()))

    def edit_item_func(self, item):
        self.edit_file_name_func(EDIT_FILE_BOX_TITLE, item.text())

    def remove_item_func(self, item):
        # 移除对应的tab页
        current_tab_indexes = self.search_tab(item.text())
        if current_tab_indexes:
            self.parent_dialog.file_tab_widget.removeTab(current_tab_indexes[0])
        super().remove_item_func(item)
        # 判断是否有绑定输出配置，如果绑定的配置和文件是1:1，询问是否同步删除配置
        template_file = get_template_file_data(item)
        if template_file.output_config_id:
            self.parent_dialog.output_config_widget.config_table.del_bind_file_row(template_file)

    def clear_items_func(self):
        super().clear_items_func()
        self.parent_dialog.file_tab_widget.clear()
        # 处理绑定的配置项
        self.parent_dialog.output_config_widget.config_table.clear_bind_file_rows()

    def search_tab(self, text):
        return [tab_idx for tab_idx in range(self.parent_dialog.file_tab_widget.count())
                if self.parent_dialog.file_tab_widget.tabText(tab_idx) == text]

    def add_list_file_item(self, template_file):
        # 添加模板文件
        file_item = QListWidgetItem(template_file.file_name)
        self.addItem(file_item)
        # 保存引用
        set_template_file_data(file_item, template_file)
        # 设置当前项
        self.setCurrentItem(file_item)

    def locate_file(self):
        file_tab_widget = self.parent_dialog.file_tab_widget
        current_tab_text = file_tab_widget.tabText(file_tab_widget.currentIndex())
        if current_tab_text:
            current_index = [row for row in range(self.count()) if self.item(row).text() == current_tab_text][0]
            self.setCurrentRow(current_index)

    def collect_template_files(self):
        file_tab_widget = self.parent_dialog.file_tab_widget
        # 将tab按名称，tab widget 放入字典，方便下面查询是否打开了tab
        name_tab_dict = {file_tab_widget.tabText(tab_idx): file_tab_widget.widget(tab_idx)
                         for tab_idx in range(file_tab_widget.count())}
        # 遍历列表项，收集数据，如果打开了tab页，文件内容使用tab页中的数据
        if not self.count():
            return
        template_files = list()
        for list_idx in range(self.count()):
            list_item = self.item(list_idx)
            template_file = get_template_file_data(list_item)
            template_file.is_current = CurrentEnum.is_current.value \
                if self.currentRow() == list_idx else CurrentEnum.not_current.value
            tab_widget = name_tab_dict.get(list_item.text())
            if tab_widget:
                template_file.file_content = tab_widget.content_editor.toPlainText()
                template_file.file_name_template = tab_widget.file_name_edit.text()
                template_file.tab_opened = TabOpenedEnum.opened.value
                template_file.is_current_tab = CurrentEnum.is_current.value \
                    if file_tab_widget.currentWidget() is tab_widget else CurrentEnum.not_current.value
                template_file.tab_item_order = file_tab_widget.indexOf(tab_widget)
            else:
                template_file.tab_opened = TabOpenedEnum.not_opened.value
            template_files.append(template_file)
        return template_files

    def collect_unbind_config_files(self):
        """收集未关联输出配置的文件"""
        template_files = list()
        for idx in range(self.count()):
            template_file = get_template_file_data(self.item(idx))
            if not template_file.output_config_id:
                template_files.append(template_file)
        return template_files
