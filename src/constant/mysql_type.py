# -*- coding: utf-8 -*-
from enum import Enum
_author_ = 'luwt'
_date_ = '2019/1/23 11:27'


class MysqlType(Enum):
    """第一个为jdbcType，第二个为javaType，根据mybatis映射关系取得"""
    bit = ('BIT', 'Boolean')

    tinyint = ('TINYINT', 'Byte')
    smallint = ('SMALLINT', 'Short')
    int = ('INTEGER', 'Integer')
    bigint = ('BIGINT', 'Long')

    float = ('FLOAT', 'Float')
    double = ('DOUBLE', 'Double')

    real = ('REAL', 'BigDecimal')
    decimal = ('DECIMAL', 'BigDecimal')
    numeric = ('NUMERIC', 'BigDecimal')

    char = ('CHAR', 'String')
    varchar = ('VARCHAR', 'String')

    tinytext = ('VARCHAR', 'String')
    text = ('VARCHAR', 'String')
    mediumtext = ('LONGVARCHAR', 'String')
    longtext = ('LONGVARCHAR', 'String')

    date = ('DATE', 'Date')
    datetime = ('TIMESTAMP', 'Date')
    timestamp = ('TIMESTAMP', 'Date')
    time = ('TIME', 'Date')


# 需要import的类型和对应语句
import_type = {
    'Date': 'import java.util.Date;',
    'BigDecimal': 'import java.math.BigDecimal;',
}
