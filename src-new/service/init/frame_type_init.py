# -*- coding: utf-8 -*-
"""
初始化数据
"""

from service.system_storage.frame_type_sqlite import FrameTypeSqlite, FrameType

_author_ = 'luwt'
_date_ = '2022/9/26 18:54'


frame_type_dict = [{'id': 1, 'name': 'sql数据源', 'type': 0, 'frame_order': 1, 'is_current': 1},
                   {'id': 2, 'name': 'structure数据源', 'type': 0, 'frame_order': 2, 'is_current': 0},
                   {'id': 3, 'name': 'sql数据源', 'type': 1, 'frame_order': 1, 'is_current': 1},
                   {'id': 4, 'name': 'structure数据源', 'type': 1, 'frame_order': 2, 'is_current': 0}]


# 初始化frame type
def init_frame_type():
    frame_types = FrameTypeSqlite().select(FrameType())
    if frame_types:
        frame_type_tuple = get_current_frame_type(frame_types)
        if frame_type_tuple:
            return frame_type_tuple
    return do_init_frame_type()


def get_current_frame_type(frame_types):
    tree_frame_types = tuple(filter(lambda x: x.type == 0 and x.is_current == 1, frame_types))
    table_frame_types = tuple(filter(lambda x: x.type == 1 and x.is_current == 1, frame_types))
    if tree_frame_types and len(tree_frame_types) == 1 and table_frame_types and len(table_frame_types) == 1:
        tree_frame_type = tree_frame_types[0]
        table_frame_type = table_frame_types[0]
        return tree_frame_type, table_frame_type


def do_init_frame_type():
    # 上述条件不满足，则进行初始化，将库里原有数据清空，初始化数据
    FrameTypeSqlite().drop_table()
    frame_types = list(map(lambda x: FrameType(**x), frame_type_dict))
    [FrameTypeSqlite().insert(frame_type) for frame_type in frame_types]
    return get_current_frame_type(frame_types)
