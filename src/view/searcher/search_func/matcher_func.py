# -*- coding: utf-8 -*-
"""
智能搜索算法：
    1、首先整词搜索，若能匹配到，则返回结果
    2、整词不存在，则尝试搜索字符，尽量以连续字符，也就是单词搜索匹配
        1、初步匹配，获取到搜索字符，在目标文本中的位置，例如搜索 enet 在 目标文本 code generator 中的位置，按顺序匹配可得索引位置：3,7,8,11
            若在按顺序匹配过程中，有字符无法匹配到，则视为失败
        2、尝试合并索引段，找出其中连续的索引，合并为段，以前例结果，合并为：(3, 3), (7, 8), (11, 11)
        3、根据合并后的索引段，取出对应字符，以前例结果，取出字符为 e, ne, t
        4、最后根据合并后的字符段，进行递归搜索，当字符个数小于等于2，则没有必要进行这一步，因为其等价于前面的全词匹配。
            匹配方式：遍历第一个字符段 char0，合并下一个字符段 char1，生成新的字符段进行匹配，如果匹配不到，则以 char1 为 char0，继续匹配，
            目的为了找到更连续的字符，实现类似单词匹配的模式。以前例结果，搜索匹配过程：合并字符段，得到 ene，搜索匹配成功，再次合并 t，
            得到 enet，匹配失败，所以最终匹配结果为，code g`ene`ra`t`or
"""

_author_ = 'luwt'
_date_ = '2022/5/9 19:02'


class SmartMatcher:

    def __init__(self, search_text):
        self.search_text = search_text.lower()
        self.target_text: str = ...
        self.consecutive_idx_segments: list = ...
        self.idx_match_list: list = ...

    def match(self, target_text):
        """匹配搜索词在目标词中的位置"""
        self.target_text = target_text.lower()
        # 首先进行简单匹配，将整词进行匹配
        simple_match_result = self.simple_match()
        if simple_match_result:
            # 返回统一格式
            return [simple_match_result, ]
        else:
            return self.smart_match()

    def smart_match(self):
        """智能匹配，匹配搜索词在目标词中的位置，尽量以单词（连续字符）的形式匹配"""
        self.consecutive_idx_segments = list()
        # 首先初步匹配，获取到text中每个字符在target text中的位置（按text中的字符顺序排列）
        each_char_idx_list = self.first_match()
        if not each_char_idx_list:
            return
        # 遍历上一步得到的列表，尝试合并其中的连续索引，变成连续索引段列表
        self.merge_consecutive_idx(each_char_idx_list)
        # 找出合并索引段后的文本段列表
        merge_str_list = self.get_str_list()
        # 尝试将邻近索引段表示的文本合并，构成新文本，再进行匹配，目的：优先组合单词匹配
        self.recursive_match(merge_str_list)
        return self.idx_match_list

    def simple_match(self):
        """简单匹配，直接进行全词匹配，返回匹配成功的索引值"""
        if self.search_text in self.target_text:
            start = self.target_text.index(self.search_text)
            end = start + len(self.search_text) - 1
            return start, end

    def first_match(self):
        """
        初步匹配，匹配search_text中每个字符按顺序在target中的位置，
        如果存在不在target中的字符，则匹配失败，否则返回匹配后的索引列表
        """
        i = -1
        idx_list = list()
        for text in self.search_text:
            if text in self.target_text[i + 1:]:
                i = self.target_text.index(text, i + 1)
                idx_list.append(i)
            else:
                return
        return idx_list

    def merge_consecutive_idx(self, idx_list):
        """
        合并索引段，找出索引列表中连续的索引，合并为段
        eg: [1, 2, 3, 4, 6, 7, 8, 10] ->
        [(1,4), (6, 8), (10, 10)]
        """
        start = idx_list[0]
        for j, idx in enumerate(idx_list):
            if j == len(idx_list) - 1:
                self.consecutive_idx_segments.append((start, idx))
            else:
                next_ = idx_list[j + 1]
                if idx + 1 != next_:
                    end = idx
                    self.consecutive_idx_segments.append((start, end))
                    start = next_
        self.idx_match_list = self.consecutive_idx_segments

    def get_str_list(self):
        """按合并后的索引段找出对应的文本列表"""
        str_list = list()
        for i in self.consecutive_idx_segments:
            str_list.append(self.target_text[i[0]: i[1] + 1])
        return str_list

    def recursive_match(self, str_list):
        """递归匹配字符列表，合并相邻文本段进行匹配，以达到精准匹配已存在单词的目的"""
        # 如果元素个数等于1，退出即可，因为简单匹配中会匹配到完全匹配的情况；
        # 元素个数等于2，再次合并即等于完全匹配，没有必要继续
        if isinstance(str_list, list) and len(str_list) <= 2:
            return
        for i, str_seg in enumerate(str_list):
            if i < len(str_list) - 1:
                # 下一个文本段
                next_str_seg = str_list[i + 1]
                # 当前文本段 + 下一个文本段，合并为新的文本
                merge_str_seg = str_seg + next_str_seg
                # 构造合并文本后的新列表
                merge_str_list = [*str_list[:i], merge_str_seg, *str_list[i + 2:]]
                # 进行匹配
                match_result = self.match_sequence(merge_str_list)
                if match_result:
                    # 匹配成功，将当前结果赋值给最终结果
                    self.idx_match_list = match_result
                    # 以新文本列表替换原str list，递归合并匹配，如果匹配失败，继续下一个元素
                    self.recursive_match(merge_str_list)
                    break

    def match_sequence(self, str_list):
        """匹配文本列表中每一个元素是否在target text中，且需按顺序匹配"""
        start = 0
        idx_list = list()
        for text in str_list:
            if text in self.target_text[start:]:
                start = self.target_text.index(text, start)
                end = start + len(text) - 1
                idx_list.append((start, end))
                start = end + 1
            else:
                return
        return idx_list
