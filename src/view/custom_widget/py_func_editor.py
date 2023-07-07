# -*- coding: utf-8 -*-
import re

from PyQt6.QtCore import Qt

from src.view.custom_widget.text_editor import TextEditor

_author_ = 'luwt'
_date_ = '2023/3/28 15:14'


class PyFuncEditor(TextEditor):
    terminate_keyword_patterns = (r'\s+return\s*', r'\s+return\s+\S+', r'\s+pass\s*', r'\s+\.\.\.\s*')
    line_break_pattern = r'.*:\s*'
    left_blank_pattern = r'^\s*(?=\S+)'
    line_comment_pattern = r'#'
    func_name_pattern = r'^\s*def\s+(\S+)\s*\(\S*'

    def keyPressEvent(self, e):
        # 按下enter键，根据上一行结尾是否是冒号结尾，判断是否需要缩进
        if e.key() == Qt.Key.Key_Return:
            current_left_blank_len = 0
            tc = self.textCursor()
            # 获取当前行块
            current_block = tc.block()
            while current_block.blockNumber() >= 0:
                # 将当前行文本按 # 分隔，取出代码部分，暂时先不考虑文档注释
                # 如果代码文本中，只有空白，跳过
                code_text = self._get_code_text(current_block.text())
                if not code_text:
                    current_block = current_block.previous()
                    continue
                # 如果 current_left_blank_len 大于0，那么说明遇到终止关键字，
                # 搜索最近的一个以冒号结尾的行且缩进长度应小于当前行，与其缩进保持一致即可
                elif current_left_blank_len > 0:
                    if not re.fullmatch(self.line_break_pattern, code_text):
                        current_block = current_block.previous()
                        continue
                    blank_list = re.findall(self.left_blank_pattern, code_text)
                    if blank_list and len(blank_list[0]) < current_left_blank_len:
                        super().keyPressEvent(e)
                        self.smart_indent(code_text, False)
                        return
                    else:
                        current_block = current_block.previous()
                        continue
                else:
                    # 如果当前行是终止关键字，那么跳过，下一行的缩进应与上一个以冒号结尾的行一致
                    if self.match_terminate_keyword(code_text):
                        # 一定可以匹配到左侧空白
                        blank_list = re.findall(self.left_blank_pattern, code_text)
                        current_left_blank_len = len(blank_list[0])
                        current_block = current_block.previous()
                        continue
                    # 那么这里就认为，取到的都是正确的代码文本，对当前行进行智能缩进
                    else:
                        super().keyPressEvent(e)
                        self.smart_indent(code_text)
                        return
        super().keyPressEvent(e)

    def _get_code_text(self, line_text):
        # 将当前行文本按 # 分隔，取出代码部分，暂时先不考虑文档注释
        code_text = line_text.split(self.line_comment_pattern)[0]
        # 如果代码文本中，存在除空白外其他字符，返回结果
        if not re.fullmatch(self.blank_pattern, code_text):
            return code_text

    def match_terminate_keyword(self, code_text):
        return re.fullmatch(self.terminate_keyword_patterns[0], code_text) \
            or re.fullmatch(self.terminate_keyword_patterns[1], code_text) \
            or re.fullmatch(self.terminate_keyword_patterns[2], code_text) \
            or re.fullmatch(self.terminate_keyword_patterns[3], code_text)

    def smart_indent(self, code_text, indent=True):
        # 首先考虑上一行左侧空白，以此为基础进行处理
        blank_list = re.findall(self.left_blank_pattern, code_text)
        blank = ''
        if blank_list:
            blank += blank_list[0]
        # 如果是以冒号结尾的行下一行需要插入四个空格
        if indent and re.fullmatch(self.line_break_pattern, code_text):
            blank += '    '
        tc = self.textCursor()
        tc.insertText(blank)

    def parse_func_name(self) -> str:
        split_lines = self.toPlainText().splitlines()
        for line in split_lines:
            code_text = self._get_code_text(line)
            # 如果代码文本中，只有空白，跳过
            if not code_text:
                continue
            func_name_result = re.findall(self.func_name_pattern, code_text)
            if func_name_result:
                return func_name_result[0]
