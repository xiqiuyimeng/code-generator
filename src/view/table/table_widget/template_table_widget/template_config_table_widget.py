# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal

from src.constant.constant import COMBO_BOX_YES_TXT, COMBO_BOX_NO_TXT
from src.constant.template_dialog_constant import DEL_CONFIG_PROMPT, DEL_CONFIG_BOX_TITLE, BATCH_DEL_CONFIG_PROMPT, \
    TEMPLATE_VAR_CONFIG_HEADER_LABELS, TEMPLATE_OUTPUT_CONFIG_HEADER_LABELS, UNBIND_FILE_TOOL_TIP, \
    DEL_OUTPUT_CONFIG_PROMPT, BATCH_DEL_OUTPUT_CONFIG_PROMPT
from src.service.system_storage.template_config_sqlite import TemplateConfig
from src.view.box.message_box import pop_question
from src.view.table.table_widget.custom_table_widget import CustomTableWidget

_author_ = 'luwt'
_date_ = '2023/3/20 11:47'


class TemplateConfigTableWidgetABC(CustomTableWidget):
    """模板配置表格控件抽象类"""
    # 编辑行信号，发送模板配置数据和行序号
    row_edit_signal = pyqtSignal(TemplateConfig, int)

    def do_fill_row(self, row_index, template_config, fill_create_time=True):
        for col, data in enumerate(self.get_row_fill_data_tuple(template_config), 1):
            self.setItem(row_index, col, self.make_item(data))

    def get_row_fill_data_tuple(self, template_config) -> tuple:
        ...

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
        if pop_question(DEL_CONFIG_PROMPT.format(config_name), DEL_CONFIG_BOX_TITLE, self):
            self.del_row(row_index)

    def remove_rows(self):
        # 获取选中多少行，进行删除提示
        delete_names = self.get_all_checked_id_names()[1]
        if pop_question(BATCH_DEL_CONFIG_PROMPT.format(len(delete_names)), DEL_CONFIG_BOX_TITLE, self):
            self.del_rows()

    def collect_data(self):
        return [self.get_row_data(row) for row in range(self.rowCount())]

    def get_row_data(self, row):
        # 收集数据
        check_num_widget = self.cellWidget(row, 0)
        order_item = check_num_widget.check_label
        return order_item.row_data


class TemplateOutputConfigTableWidget(TemplateConfigTableWidgetABC):
    """模板输出路径配置表格控件"""

    def __init__(self, *args):
        super().__init__(TEMPLATE_OUTPUT_CONFIG_HEADER_LABELS, *args)

    def get_row_fill_data_tuple(self, template_config) -> tuple:
        return template_config.config_name, template_config.output_var_name, template_config.config_value_widget, \
            COMBO_BOX_YES_TXT if template_config.is_required else COMBO_BOX_NO_TXT, \
            len(template_config.bind_file_list) if template_config.bind_file_list else 0, \
            template_config.config_desc

    def show_tool_tip(self, model_index):
        # 如果是关联文件列，执行特定的气泡提示
        if model_index.column() == 5:
            # 获取关联文件列表
            bind_file_list = self.get_row_data(model_index.row()).bind_file_list
            if bind_file_list:
                tool_tip = ', \n'.join([tp_file.file_name for tp_file in bind_file_list])
            else:
                tool_tip = UNBIND_FILE_TOOL_TIP
            self.setToolTip(tool_tip)
        else:
            super().show_tool_tip(model_index)

    def del_row(self, row):
        self.unbind_config_file(row)
        super().del_row(row)

    def del_rows(self):
        for row_index in reversed(range(self.rowCount())):
            if self.cellWidget(row_index, 0).check_box.checkState():
                self.unbind_config_file(row_index)
        super().del_rows()

    def unbind_config_file(self, row):
        output_config = self.get_row_data(row)
        if not output_config.bind_file_list:
            return
        for file in output_config.bind_file_list:
            file.output_config_id = None

    def del_bind_file_row(self, template_file):
        for row_index in range(self.rowCount()):
            config = self.get_row_data(row_index)
            if config.bind_file_list and template_file in config.bind_file_list:
                # 如果文件列表只有一个文件，那么询问是否删除配置，否则移除当前文件即可
                if len(config.bind_file_list) == 1:
                    if pop_question(DEL_OUTPUT_CONFIG_PROMPT.format(config.config_name),
                                    DEL_CONFIG_BOX_TITLE, self):
                        super().del_row(row_index)
                        break
                    else:
                        config.bind_file_list = None
                else:
                    config.bind_file_list.remove(template_file)
                # 更新表格中显示的文件数量
                self.update_bind_file_num_row(row_index)
                break

    def clear_bind_file_rows(self):
        # 搜集所有绑定了文件的配置
        bind_file_config_list, row_idxes = list(), list()
        for row_index in range(self.rowCount()):
            config = self.get_row_data(row_index)
            if config.bind_file_list:
                bind_file_config_list.append(config)
                row_idxes.append(row_index)
        if not bind_file_config_list:
            return
        # 如果存在配置绑定了文件，询问是否删除
        if pop_question(BATCH_DEL_OUTPUT_CONFIG_PROMPT, DEL_CONFIG_BOX_TITLE, self):
            for row in reversed(row_idxes):
                self.removeRow(row)
            # 行序号重排序
            self.resort_row()
            # 删除行后，重新计算表头复选框状态
            self.header_widget.calculate_header_check_state()
        else:
            for config in bind_file_config_list:
                config.bind_file_list = None
                # 更新表中显示的文件数量
                self.update_bind_file_num_row(row_idxes[bind_file_config_list.index(config)])

    def update_bind_file_num_row(self, row):
        output_config = self.get_row_data(row)
        bind_file_num = len(output_config.bind_file_list) if output_config.bind_file_list else 0
        self.item(row, 5).setText(str(bind_file_num))

    def update_bind_file_num_rows(self):
        for row in range(self.rowCount()):
            self.update_bind_file_num_row(row)


class TemplateVarConfigTableWidget(TemplateConfigTableWidgetABC):
    """模板变量配置表格控件"""

    def __init__(self, *args):
        super().__init__(TEMPLATE_VAR_CONFIG_HEADER_LABELS, *args)

    def get_row_fill_data_tuple(self, template_config) -> tuple:
        return template_config.config_name, template_config.output_var_name, template_config.config_value_widget, \
            COMBO_BOX_YES_TXT if template_config.is_required else COMBO_BOX_NO_TXT, template_config.config_desc
