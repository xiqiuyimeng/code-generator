# -*- coding: utf-8 -*-
import re

from PyQt6.QtGui import QSyntaxHighlighter

_author_ = 'luwt'
_date_ = '2023/3/15 15:25'


class SyntaxHighLighterABC(QSyntaxHighlighter):

    def __init__(self, parent=None):
        super().__init__(parent)

        # 保存匹配规则与展示样式
        self.mappings = dict()
        self.add_mappings()

    def add_mappings(self):
        ...

    def highlightBlock(self, text):
        for pattern, text_format in self.mappings.items():
            for match in re.finditer(pattern, text):
                start, end = match.span()
                self.setFormat(start, end - start, text_format)
