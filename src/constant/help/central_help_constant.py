# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/14 18:08'


OVERVIEW_TEXT = '主界面包含标题栏、菜单栏、工具栏、主数据区域，主数据区域包含左侧数据源列表、右侧打开数据表后的字段表格，以下是详细介绍'

TITLE_BAR_LABEL_TEXT = '标题栏：'
TITLE_BAR_HELP_TEXT = '标题栏包含标题、快捷按钮（最小化、最大化、退出）'

MENU_BAR_LABEL_TEXT = '菜单栏：'
MENU_BAR_HELP_TEXT = '<p>菜单栏包含文件、帮助两个主菜单<p>' \
                     '<ol>' \
                     '  <li>文件菜单：' \
                     '    <ol>' \
                     '      <li>切换数据源种类：用于切换sql数据源或结构体数据源</li>' \
                     '      <li>添加数据源：用于添加当前数据源种类下所支持的数据源</li>' \
                     '      <li>刷新：刷新选中的数据源列表项</li>' \
                     '      <li>类型映射：进入类型映射管理页</li>' \
                     '      <li>模板：进入模板管理页</li>' \
                     '      <li>生成：在选中数据源数据后，开始生成代码流程</li>' \
                     '      <li>清空选择：清空当前数据源种类下所有选中数据</li>' \
                     '      <li>退出：退出生成器</li>' \
                     '    </ol>' \
                     '  </li>' \
                     '  <li>帮助菜单：' \
                     '    <ol>' \
                     '      <li>帮助：打开帮助信息页</li>' \
                     '      <li>关于：打开生成器介绍信息页</li>' \
                     '    </ol>' \
                     '  </li>' \
                     '</ol>'

TOOL_BAR_LABEL_TEXT = '工具栏：'
TOOL_BAR_HELP_TEXT = '<p>工具栏包含以下常用工具<p>' \
                     '<ol>' \
                     '  <li>切换数据源种类：用于切换sql数据源或结构体数据源</li>' \
                     '  <li>添加数据源：用于添加当前数据源种类下所支持的数据源</li>' \
                     '  <li>刷新：刷新选中的数据源列表项</li>' \
                     '  <li>类型映射：进入类型映射管理页</li>' \
                     '  <li>模板：进入模板管理页</li>' \
                     '  <li>生成：在选中数据源数据后，开始生成代码流程</li>' \
                     '  <li>清空选择：清空当前数据源种类下所有选中数据</li>' \
                     '  <li>帮助：打开帮助信息页</li>' \
                     '  <li>关于：打开生成器介绍信息页</li>' \
                     '  <li>退出：退出生成器</li>' \
                     '</ol>'

MAIN_AREA_LABEL_TEXT = '主数据区域：'
MAIN_AREA_HELP_TEXT = '<p>主数据区域包含左侧数据源列表、右侧打开数据表后的字段表格</p>' \
                      '<ol>' \
                      ' <li>左侧数据源列表：左侧用来维护数据源信息，通过添加数据源功能添加数据源后，将会展示在列表中，' \
                      '双击可打开数据源，进行其他操作，例如刷新数据源信息、选中数据表进行生成' \
                      '<p class=import>系统内所有的树控件、列表控件都支持搜索功能，按 ctrl + F 进行搜索，Esc关闭搜索</p></li>' \
                      ' <li>右侧打开数据表后的字段表格：在打开数据表后，右侧将展示数据表具体信息，' \
                      '可以进行编辑修改，编辑后将会保存到本地，不修改数据源的源信息</li>' \
                      '</ol>'
