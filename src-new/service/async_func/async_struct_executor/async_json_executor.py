# -*- coding: utf-8 -*-
import json

from PyQt5.QtCore import pyqtSignal

from service.async_func.async_struct_executor.async_struct_executor import PrettyStructWorker, PrettyStructExecutor, \
    OpenStructWorker, OpenStructExecutor
from service.system_storage.data_type import get_data_type
from service.system_storage.ds_table_info_sqlite import DsTableInfo, ColTypeEnum
from view.tree.tree_item.tree_item_func import get_item_opened_record

_author_ = 'luwt'
_date_ = '2022/12/5 10:13'


# ---------------------------------------- 异步美化json文件 start ---------------------------------------- #

class PrettyJsonWorker(PrettyStructWorker):
    success_signal = pyqtSignal(str)

    def do_beautify(self):
        # 解析美化
        return json.dumps(json.loads(self.data), ensure_ascii=False, indent=4)


class PrettyJsonExecutor(PrettyStructExecutor):

    def get_worker(self) -> PrettyStructWorker:
        return PrettyJsonWorker(self.data, self.struct_type)


# ---------------------------------------- 异步美化json文件 end ---------------------------------------- #


# ---------------------------------------- 打开json结构体 start ---------------------------------------- #

class OpenJsonWorker(OpenStructWorker):

    def parse(self):
        # 解析
        struct_content_dict = json.loads(self.struct_info.content)
        return self.do_parse(struct_content_dict)

    def do_parse(self, obj_dict: dict, parent_id=0):
        col_list = list()
        for name, value in obj_dict.items():
            col_info = self.assemble_table_info(name, value, parent_id)
            col_list.append(col_info)
            # 如果是字典，那么继续解析，当前列类型为对象
            if isinstance(value, dict):
                col_info.col_type = ColTypeEnum.obj.value
                self.table_info_sqlite.insert(col_info)
                col_info.children = self.do_parse(value, col_info.id)
            elif isinstance(value, list):
                self.parse_array(value, col_info)
            else:
                # 基本数据类型，结束
                col_info.col_type = ColTypeEnum.col.value
                self.table_info_sqlite.insert(col_info)
        return col_list

    def parse_array(self, value_list, col_info):
        # 对于list，只需要取第一个元素即可获取类型
        value_obj = value_list[0]
        # 将当前列类型，置为数组
        col_info.col_type = ColTypeEnum.array.value
        # 根据第一个元素的类型，决定整个数组的数据类型
        col_info.data_type = col_info.data_type.format(get_data_type(value_obj))
        col_info.full_data_type = col_info.full_data_type.format(get_data_type(value_obj))
        # 如果数组下元素为字典，那么继续解析
        if isinstance(value_obj, dict):
            self.table_info_sqlite.insert(col_info)
            # 只有在字典类型的时候，才指定子元素列表
            col_info.children = self.do_parse(value_obj, col_info.id)
        elif isinstance(value_obj, list):
            # 如果是list类型，继续解析，对于列表类型，那么无需指定子元素列表，
            # 因为对于json来说，只有k v结构，才应被当做一条列信息对待，
            # 而列表本身，应被作为一条数组类型的列来看待
            self.parse_array(value_obj, col_info)
        else:
            # 如果数组元素为基本数据类型，那么结束，最终的数据类型应类似于：string []
            self.table_info_sqlite.insert(col_info)

    def assemble_table_info(self, name, value, parent_id):
        col_info = DsTableInfo()
        col_info.col_name = name
        col_info.checked = self.opened_table_item.checked
        # 获取变量值的数据类型映射值
        data_type = get_data_type(value)
        col_info.data_type = data_type
        col_info.full_data_type = data_type
        col_info.parent_id = parent_id
        col_info.parent_tab_id = self.table_tab_id

        # 获取顺序值
        max_order_param = {
            'parent_tab_id': self.table_tab_id,
            'parent_id': parent_id
        }
        col_info.item_order = self.table_info_sqlite.get_max_order(max_order_param)
        return col_info


class OpenJsonExecutor(OpenStructExecutor):

    def get_worker(self) -> OpenStructWorker:
        return OpenJsonWorker(get_item_opened_record(self.item))

# ---------------------------------------- 打开json结构体 end ---------------------------------------- #
