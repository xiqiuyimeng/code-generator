# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat

from src.view.custom_widget.syntax_highlighter.abstract_syntax_highlighter import AbstractSyntaxHighLighter

_author_ = 'luwt'
_date_ = '2023/3/15 16:38'


class JsonSyntaxHighLighter(AbstractSyntaxHighLighter):

    def add_mappings(self):
        # json 保留字
        reserved_word_format = QTextCharFormat()
        reserved_word_format.setForeground(Qt.darkRed)
        reserved_word_pattern = r'(?<=:|,|\[)\s*(null|true|false),?'
        self.mappings[reserved_word_pattern] = reserved_word_format

        # json key
        key_format = QTextCharFormat()
        key_format.setForeground(Qt.darkRed)
        key_pattern = r'"[^"]*?"(?=\s*:)'
        self.mappings[key_pattern] = key_format

        # json value：数字
        num_value_format = QTextCharFormat()
        num_value_format.setForeground(Qt.darkGreen)
        num_value_pattern = r'(?<=:|,|\[)\s*(\d+),?'
        self.mappings[num_value_pattern] = num_value_format

        # json value: str
        str_value_format = QTextCharFormat()
        str_value_format.setForeground(Qt.blue)
        str_value_pattern = r'(?<=:|,|\[)\s*("[^:"]*")[^:],?'
        self.mappings[str_value_pattern] = str_value_format
