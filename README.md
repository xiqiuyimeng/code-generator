# mybatis-generator
mybatis反向生成器，python实现
generator是用字符串拼接实现的生成器。
mybatis_generator是借助jinja2实现的生成器。
其中的db_opt模块是我自己的连接数据库模块，getcursor提供的是获取数据库连接的方法，如果需要，请自行补充获取数据库部分代码。
暂时只是支持mysql数据库，对其他数据库未做兼容。
这个demo仅做抛砖引玉，提供思路。

已完善数据库连接代码
增加对service层和controller层模板代码的生成

- 分支：
  - master分支，主要是功能的实现，使用需要通过命令行的形式启动程序。
  - gui分支，使用pyqt5实现了软件界面，更方便使用。



