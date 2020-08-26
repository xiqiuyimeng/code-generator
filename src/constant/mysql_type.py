# -*- coding: utf-8 -*-
from enum import Enum
_author_ = 'luwt'
_date_ = '2019/1/23 11:27'


class MysqlType(Enum):
    tinyint = ('TINYINT', 'Integer')
    int = ('INTEGER', 'Integer')
    text = ('VARCHAR', 'String')
    float = ('FLOAT', 'Float')
    double = ('DOUBLE', 'Double')
    decimal = ('DECIMAL', 'BigDecimal')
    date = ('DATE', 'Date')
    datetime = ('TIMESTAMP', 'Date')
    timestamp = ('TIMESTAMP', 'Date')
    time = ('TIME', 'Date')
    char = ('CHAR', 'String')
    varchar = ('VARCHAR', 'String')
    longtext = ('VARCHAR', 'String')
    bigint = ('LONG', 'Long')


# 需要import的类型和对应语句
import_type = {
    'Date': 'import java.util.Date;'
}
