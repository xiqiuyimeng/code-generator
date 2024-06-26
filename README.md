# code-generator
1. 设计宗旨：帮助用户完成有规则的、重复性的工作，提高效率
2. 开发技术：代码使用 `Python` 开发，GUI界面使用 `PyQt6` 模块开发，生成代码使用 `Jinja2` 模板引擎动态渲染数据，系统中缓存的数据使用 `sqlite` 数据库存储，数据库地址：`家目录/.generator_db/generator_db`
3. 使用方法：
   1. 首先添加数据源，目前系统支持两大类数据源，sql数据源和结构体数据源，其中sql数据源目前支持：`sqlite`, `mysql`, `oracle`，结构体数据源目前支持 `json`
   2. 添加类型映射数据，类型映射数据作用是，在生成代码时，对数据源的字段类型进行转化，转化为代码中实际使用的类型，类型映射中，增加了组的概念，一个类型映射组将保持唯一的映射列名称，映射列名称将作为在模板中引用该映射组的唯一标识
   3. 添加模板数据，模板包含四个部分：
      1. 模板基本信息：模板基本信息作为对模板的基本描述信息
      2. 模板配置信息：模板配置信息包括两部分，输出路径配置信息，负责维护代码文件输出路径信息；变量配置信息，负责维护模板文件中需要用到的一些用户输入的数据，通过变量配置作为桥梁来接收用户输入
      3. 模板文件：模板文件包含两部分，文件名模板，负责维护文件名的生成规则，可以引用模板方法；文件内容模板，负责维护文件内容生成规则，可以引用数据源列数据、类型映射、模板方法、变量配置数据，来完成模板的编写
      4. 模板方法：在模板内不便处理的数据，可以利用模板方法来处理，模板方法语言为 `Python`，所以需要遵循 `Python` 语法，编写好的模板方法，可以在模板内引用，来达到增强处理数据的目的
   4. 打开数据源，选择表或字段，开始生成，选择合适的类型映射，选择合适的模板，并填写对应的模板配置信息，填写完毕可以进一步选择生成到文件，或预览生成结果，预览结果支持修改
   5. 项目预设了一套类型映射文件与模板文件，文件地址：`static/prebuild_import_data`，可直接启动后，导入使用
   6. 在页面树结构及列表结构中，均可使用智能搜索组件，启动方法为`Ctrl F`，已实现类似`Jetbrains`家族工具中快捷智能搜索模式
4. 程序启动：切换到程序目录下，安装 `requirement.txt` 中所需要的依赖包，`pip install -r requirement.txt`，另外开发程序时使用的 `Python` 版本为 `3.9`，没有对低版本进行测试
5. 打包方法：切换到程序目录下，执行 `pyinstaller main.spec`，需要将 `main.spec` 文件中 `pathex` 变量指定为实际打包时的项目地址，`datas` 变量中包含一个元祖，元祖第一个元素指定为实际打包时项目静态资源文件目录，第二个元素为在项目中使用的地址，无需改动