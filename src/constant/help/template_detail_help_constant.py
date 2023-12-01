# -*- coding: utf-8 -*-

_author_ = 'luwt'
_date_ = '2023/6/15 11:34'


OVERVIEW_TEXT = '模板详情页包含基本信息、模板配置、模板文件三部分，下面进行详细介绍' \
                '<p class="import">需要注意的是，所有操作必须在点击保存按钮后才会保存修改，否则离开页面，将丢弃所有修改</p>'

TEMPLATE_BASIC_INFO_LABEL_TEXT = '基本信息：'
TEMPLATE_BASIC_INFO_HELP_TEXT = '主要存储模板名称和备注信息'

TEMPLATE_CONFIG_LABEL_TEXT = '模板配置：'
TEMPLATE_CONFIG_HELP_TEXT = '<p>模板配置包含两部分</p>' \
                            '<ol>' \
                            ' <li>模板输出路径配置：模板输出路径配置，将决定模板文件的实际输出路径。通过添加输出路径配置并关联模板文件，' \
                            '在生成时，将会动态构建出用户需要填写的，模板文件输出路径表单。系统在获取到用户输入的表单数据后，' \
                            '将作为模板文件输出路径使用，当然也支持提取用户输入值作为变量在模板中使用，具体可参考模板配置详情帮助信息' \
                            '   <ol>' \
                            '     <li>增删输出配置项：新增或移除输出配置项，如果输出配置关联了模板文件，移除配置项后将自动解除关联</li>' \
                            '     <li>生成文件输出路径配置：系统将自动根据当前已存在的模板文件构造出默认的输出路径配置项</li>' \
                            '     <li>维护文件输出路径：当输出配置项存在时，点击按钮将跳转至维护模板输出配置和文件关系页面</li>' \
                            '     <li>预览模板配置页：当输出配置项存在时，可以动态渲染出生成时，用户看到的输出配置表单样式效果</li>' \
                            '   </ol>' \
                            ' </li>' \
                            ' <li>模板变量配置：模板变量配置的作用是，为模板提供一些额外的变量，例如需要用户输入的一些动态变量，' \
                            '皆可通过变量配置的方式提供给模板，目的是实现模板使用过程中动态接受用户输入' \
                            '   <ol>' \
                            '     <li>增删变量配置项：新增或移除变量配置项</li>' \
                            '     <li>预览模板配置页：当变量配置项存在时，可以动态渲染出生成时，用户看到的变量配置表单样式效果</li>' \
                            '   </ol>' \
                            ' </li>' \
                            '</ol>'

TEMPLATE_FILE_LABEL_TEXT = '模板文件：'
TEMPLATE_FILE_HELP_TEXT = '<p>提供对模板文件的管理功能，下面是关于模板文件详细介绍<p class=import>需要注意的是，' \
                          '在模板中获取到的数据通常都是字符串类型，例如将 python 中的布尔 False 传入，' \
                          '在模板中实际获取到的也是 "False"，如果需要转为布尔类型，需要在模板方法中进行转化</p></p>' \
                          '<ol>' \
                          '  <li>文件名：主要作用是在模板文件列表中作唯一性区分</li>' \
                          '  <li>文件名模板：在生成文件时，将会以文件名模板，作为模板，生成实际的文件名，如果文件名模板未填写，' \
                          '那么系统在生成时，将默认使用模板文件名，作为模板来生成实际的文件名，以下为系统提供的，可以使用的变量' \
                          '    <ol>' \
                          '      <li>数据表名：可以通过 table_name 变量获取，例如以表名作为文件名，<br>' \
                          '文件名模板示例：{{ table_name }}</li>' \
                          '      <li>模板方法：通过模板方法添加的方法，可以在模板中直接引用，<br>' \
                          '引用方式为 {{ template_func.func_name(func_args) }}<br>' \
                          '将 func_name 替换为实际的方法名，func_args 替换为方法参数即可</li>' \
                          '    </ol>' \
                          '  </li>' \
                          '  <li>文件内容：模板引擎使用 jinja2，所以在模板文件中，请按照 jinja2 语法编写，为了方便编写模板，' \
                          '可以通过模板方法，处理数据，在模板文件中引用模板方法，达到一些特殊代码的处理效果。以下为系统提供的，' \
                          '可以使用的变量' \
                          '    <ol>' \
                          '      <li>数据表名：可以通过 table_name 变量获取，<br>' \
                          '引用方式：{{ table_name }}</li>' \
                          '      <li>数据表注释：可以通过 table_comment 变量获取，<br>' \
                          '引用方式：{{ table_comment }}</li>' \
                          '      <li>数据表字段：系统将注入数据表字段列表 col_list，所以在使用时，应先遍历字段列表，' \
                          '获取到每个字段对象时，再进行取值操作，col_list 结构体示例：' \
                          '<pre>' \
                          '[\n' \
                          '    {\n' \
                          '        "name": "col_name",\n' \
                          '        "data_type": "varchar",\n' \
                          '        "full_data_type": "varchar(32)",\n' \
                          '        "type_mapping_obj": {\n' \
                          '            "mapping_type": "String",\n' \
                          '            "import_desc": "引包声明",\n' \
                          '        },\n' \
                          '        "comment": "字段备注",\n' \
                          '        "is_pk": False,\n' \
                          '        "col_type": "col",\n' \
                          '        "children": [],\n' \
                          '    }\n' \
                          ']' \
                          '</pre>' \
                          '假设遍历获取到的字段对象，命名为 col_data，那么可以根据结构体中的 key，获取到对应的值，例如：<br>' \
                          '获取字段名称：{{ col_data.name }} <br>' \
                          '       <ol>' \
                          '         <li>name：字段名，来源于数据表</li>' \
                          '         <li>data_type：数据类型，来源于数据表</li>' \
                          '         <li>full_data_type：完整数据类型，包含长度，来源于数据表</li>' \
                          '         <li>type_mapping_obj：类型映射组对象，系统将会自动将类型映射信息附加到字段对象中，' \
                          '通过映射列名称来获取对应的映射组，例如：<br>' \
                          '当前类型映射组存在两个映射组，映射列名称分别为：mapping1， mapping2，那么将得到这样的字段对象结构' \
                          '<pre>' \
                          '[\n' \
                          '    {\n' \
                          '        "name": "col_name",\n' \
                          '        "data_type": "varchar",\n' \
                          '        "full_data_type": "varchar(32)",\n' \
                          '        "mapping1": {\n' \
                          '            "mapping_type": "String",\n' \
                          '            "import_desc": "引包声明",\n' \
                          '        },\n' \
                          '        "mapping2": {\n' \
                          '            "mapping_type": "String",\n' \
                          '            "import_desc": "引包声明",\n' \
                          '        },\n' \
                          '        "comment": "字段备注",\n' \
                          '        "is_pk": False,\n' \
                          '        "col_type": "col",\n' \
                          '        "children": [],\n' \
                          '    }\n' \
                          ']' \
                          '</pre>' \
                          '<p class=import>需要注意的是：如果当前数据类型，在类型映射中找不到，' \
                          '那么在字段对象中将不会出现映射组信息，所以在调用映射组信息字段时，需要判断是否存在，引用示例：<br>' \
                          '{{ col_data.mapping1.mapping_type if col_data.mapping1 is defined else "undefined" }}<br>' \
                          '或者：{{ col_data.mapping1.mapping_type if col_data.mapping1 else "undefined" }}<br>' \
                          '另外，在数据列字段中，is_pk 属性为布尔变量</p>' \
                          '         </li>' \
                          '         <li>comment：字段的备注，来源于数据表</li>' \
                          '         <li>is_pk：字段是否是主键，来源于数据表</li>' \
                          '         <li>col_type：字段类型，col 或者 array，如果是 array，那么可能存在 children 字段</li>' \
                          '         <li>children：嵌套子结构，在结构体数据源中可能会出现，子对象结构同当前字段对象结构</li>' \
                          '       </ol>' \
                          '      </li>' \
                          '      <li>模板方法：通过模板方法添加的方法，可以在模板中直接引用，<br>' \
                          '引用方式为 {{ template_func.func_name(func_args) }}<br>' \
                          '将 func_name 替换为实际的方法名，func_args 替换为方法参数即可</li>' \
                          '      <li>模板输出配置：在输出配置项表单页，用户输入的值，将会被收集为 k，v 结构，' \
                          'key 为 输出路径配置项对应的输出变量名，value 为用户输入的值<br>' \
                          '引用方式为：{{ output_config.var_name }}，其中 var_name 为模板输出配置项的输出变量名称</li>' \
                          '      <li>模板变量配置：在模板变量配置项表单页，用户输入的值，将会被收集为 k，v 结构，' \
                          'key 为 模板变量配置项对应的输出变量名，value 为用户输入的值<br>' \
                          '引用方式为：{{ var_config.var_name }} 其中 var_name 为模板变量配置项的输出变量名称</li>' \
                          '    </ol>' \
                          '  </li>' \
                          '</ol>'
