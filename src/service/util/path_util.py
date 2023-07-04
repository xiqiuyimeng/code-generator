# -*- coding: utf-8 -*-
import os
import platform
import re

_author_ = 'luwt'
_date_ = '2023/5/7 9:25'


windows_dir_pattern = r'[^:*?"<>|]+'


def check_dir_legal(current_dir):
    # 文件夹长度不允许超过255字符
    if len(current_dir) > 255:
        return False
    # Windows需要校验，目录是否合法
    elif platform.system() == 'Windows':
        return re.fullmatch(windows_dir_pattern, current_dir)
    return True


def check_path_legal(path):
    if not os.path.isdir(path):
        parent_path, child_dir = os.path.split(path)
        # 如果当前拆分子目录合法，继续递归父路径
        if check_dir_legal(child_dir):
            return check_path_legal(parent_path)
    else:
        return True
