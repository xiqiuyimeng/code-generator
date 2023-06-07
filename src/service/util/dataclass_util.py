# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/7 9:20'


def init(cls):
    """给数据类增加init方法"""
    def __init__(cls_obj, **kwargs):
        for k, v in kwargs.items():
            setattr(cls_obj, k, v)
    cls.__init__ = __init__
    return cls


def import_export(key_cols=tuple()):
    """给数据类添加转化导入导出实体方法"""
    def wrapper(cls):
        # 转化导入实体对象
        def convert_import_method(cls_obj, **kwargs):
            for k, v in kwargs.items():
                if hasattr(cls_obj, k):
                    setattr(cls_obj, k, v)
            return cls_obj
        cls.convert_import = convert_import_method

        # 转化导出实体对象
        def convert_export_method(cls_obj, **kwargs):
            for k, v in kwargs.items():
                if hasattr(cls_obj, k) or k in key_cols:
                    setattr(cls_obj, k, v)
            return cls_obj
        cls.convert_export = convert_export_method
        return cls
    return wrapper


