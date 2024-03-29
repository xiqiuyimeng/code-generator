# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCharFormat

from src.view.custom_widget.syntax_highlighter.syntax_highlighter_abc import SyntaxHighLighterABC

_author_ = 'luwt'
_date_ = '2023/3/15 16:38'


class JsonSyntaxHighLighter(SyntaxHighLighterABC):

    def add_mappings(self):
        # json 保留字
        reserved_word_format = QTextCharFormat()
        reserved_word_format.setForeground(Qt.GlobalColor.darkRed)
        reserved_word_pattern = r'(?<=:|,|\[)\s*(null|true|false),?'
        self.mappings[reserved_word_pattern] = reserved_word_format

        # json key
        key_format = QTextCharFormat()
        key_format.setForeground(Qt.GlobalColor.darkRed)
        key_pattern = r'"[^"]*?"(?=\s*:)'
        self.mappings[key_pattern] = key_format

        # json value：数字
        num_value_format = QTextCharFormat()
        num_value_format.setForeground(Qt.GlobalColor.darkGreen)
        num_value_pattern = r'(?<=:|,|\[)\s*(\d+),?'
        self.mappings[num_value_pattern] = num_value_format

        # json value: str
        str_value_format = QTextCharFormat()
        str_value_format.setForeground(Qt.GlobalColor.blue)
        str_value_pattern = r'(?<=:|,|\[)\s*("[^:"]*")[^:],?'
        self.mappings[str_value_pattern] = str_value_format
