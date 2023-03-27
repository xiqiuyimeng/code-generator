# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.template_dialog_constant import DEL_CONFIG_PROMPT, DEL_CONFIG_BOX_TITLE, BATCH_DEL_CONFIG_PROMPT, \
    TEMPLATE_CONFIG_HEADER_LABELS
from src.service.system_storage.template_config_sqlite import TemplateConfig
from src.view.box.message_box import pop_question
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/3/20 11:47'


class TemplateConfigTableWidget(CustomTableWidget):
    # 编辑行信号，发送模板配置数据和行序号
    row_edit_signal = pyqtSignal(TemplateConfig, int)

    def __init__(self, *args):
        super().__init__(TEMPLATE_CONFIG_HEADER_LABELS, *args)

    def do_fill_row(self, row_index, template_config, fill_create_time=True):
        data_tuple = (template_config.config_name, template_config.output_var_name,
                      template_config.config_value_widget)
        for i in range(1, 4):
            self.setItem(row_index, i, self.make_item(data_tuple[i - 1]))
        self.setItem(row_index, 4, self.make_item('是' if template_config.is_required else '否'))
        self.setItem(row_index, 5, self.make_item(template_config.config_desc))

    def emit_row_edit_signal(self, order_item, row_id):
        row_idx = int(order_item.text()) - 1
        self.row_edit_signal.emit(order_item.row_data, row_idx)

    def get_exists_names_and_var_names(self):
        exists_names, exists_var_names = list(), list()
        for row in range(self.rowCount()):
            exists_names.append(self.item(row, 1).text())
            exists_var_names.append(self.item(row, 2).text())
        return exists_names, exists_var_names

    def remove_row(self, row_index, config_name):
        if not pop_question(DEL_CONFIG_PROMPT.format(config_name), DEL_CONFIG_BOX_TITLE, self):
            return
        self.del_row(row_index)

    def remove_rows(self):
        # 获取选中多少行，进行删除提示
        delete_names = self.get_all_checked_id_names()[1]
        if not pop_question(BATCH_DEL_CONFIG_PROMPT.format(len(delete_names)), DEL_CONFIG_BOX_TITLE, self):
            return
        self.del_rows()

    def collect_data(self):
        return [self.get_row_data(row) for row in range(self.rowCount())]

    def get_row_data(self, row):
        # 收集数据
        check_num_widget = self.cellWidget(row, 0)
        order_item = check_num_widget.check_label
        return order_item.row_data