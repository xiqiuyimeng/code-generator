# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/15 11:36'


OVERVIEW_TEXT = '模板方法详情页，包含方法名和方法编辑区两部分，这里的方法统一都是 python 方法，不支持其他语言'

TEMPLATE_FUNC_NAME_LABEL_TEXT = '模板方法名：'
TEMPLATE_FUNC_NAME_HELP_TEXT = '模板方法名无法输入，只能由系统从方法编辑区提取解析出来，并且如果方法编辑区编写了多个方法，' \
                               '系统只能解析出第一个方法作为方法名，所以如果必须定义多个方法，应将其他方法定义为最外层方法的内部方法使用'

TEMPLATE_FUNC_EDIT_LABEL_TEXT = '方法编辑区：'
TEMPLATE_FUNC_EDIT_HELP_TEXT = '方法编辑区只能编写 python 方法，建议可以在专业编辑器中调试方法后，再录入编辑区，编辑区不支持调试功能，' \
                               '第一个定义的方法，将被抽取解析方法名，作为当前模板方法的方法名'
