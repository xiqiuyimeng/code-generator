# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/13 18:10'

HELP_TITLE = '帮助信息'

CENTRAL_HELP = '主界面'
SQL_DS_HELP = 'sql数据源'
FOLDER_HELP = '结构体文件夹'
STRUCT_DS_HELP = '结构体数据源'
TYPE_MAPPING_TABLE_HELP = '类型映射管理'
TYPE_MAPPING_DETAIL_HELP = '类型映射详情'
DS_COL_TYPE_HELP = '数据源列类型'
TEMPLATE_TABLE_HELP = '模板管理'
TEMPLATE_DETAIL_HELP = '模板详情'
TEMPLATE_CONFIG_HELP = '模板配置详情'
TEMPLATE_FILE_OUTPUT_CONFIG_MAINTAIN_HELP = '模板文件输出配置维护'
TEMPLATE_FUNC_DETAIL_HELP = '模板方法详情'
TEMPLATE_COPY_FUNC_HELP = '复制其他模板方法'
IMPORT_DATA_HELP = '导入数据'
IMPORT_ERROR_DATA_HELP = '导入数据异常处理'
EXPORT_DATA_HELP = '导出数据'

HELP_TYPE_DICT = {
    CENTRAL_HELP: 'CentralHelpWidget',
    SQL_DS_HELP: 'SqlDsHelpWidget',
    FOLDER_HELP: 'FolderHelpWidget',
    STRUCT_DS_HELP: 'StructDsHelpWidget',
    TYPE_MAPPING_TABLE_HELP: 'TypeMappingTableHelpWidget',
    TYPE_MAPPING_DETAIL_HELP: 'TypeMappingDetailHelpWidget',
    DS_COL_TYPE_HELP: 'DsColTypeHelpWidget',
    TEMPLATE_TABLE_HELP: 'TemplateTableHelpWidget',
    TEMPLATE_DETAIL_HELP: 'TemplateDetailHelpWidget',
    TEMPLATE_CONFIG_HELP: 'TemplateConfigHelpWidget',
    TEMPLATE_FILE_OUTPUT_CONFIG_MAINTAIN_HELP: 'TemplateFileOutputConfigMaintainHelpWidget',
    TEMPLATE_FUNC_DETAIL_HELP: 'TemplateFuncDetailHelpWidget',
    TEMPLATE_COPY_FUNC_HELP: 'TemplateCopyFuncHelpWidget',
    IMPORT_DATA_HELP: 'ImportDataHelpWidget',
    IMPORT_ERROR_DATA_HELP: 'ImportErrorDataHelpWidget',
    EXPORT_DATA_HELP: 'ExportDataHelpWidget',
}

TEXT_BROWSER_STYLE = '''
<style>
    p {
        line-height: 1.8;
    }
    ol,li {
        line-height: 1.8;
    }
    ul,li {
        line-height: 1.8;
    }
    .import {
        color: red
    }
</style>
'''

MULTI_LINE_LABEL_STYLE = '''
<style>
    p {
        line-height: 1.8;
    }
    .import {
        color: red
    }
</style>
'''
