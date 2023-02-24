# -*- coding: utf-8 -*-
"""
所有用到的常量
"""
import os

_author_ = 'luwt'
_date_ = '2020/4/20 10:40'


# windows家目录变量：USERPROFILE，unix：HOME
SYS_DB_PATH = os.path.join(os.environ['USERPROFILE'], '.generator_db')


DS_TYPE_COMBO_BOX_PLACEHOLDER_TXT = '请选择数据源类型'
