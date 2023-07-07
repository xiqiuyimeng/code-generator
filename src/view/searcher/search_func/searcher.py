# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt

from src.view.searcher.dock.dock_widget import SearcherDockWidget
from src.view.searcher.search_func.matcher_func import SmartMatcher
from src.view.searcher.style_item_delegate.searcher_style_delegate import SearchStyledItemDelegate

_author_ = 'luwt'
_date_ = '2022/5/9 19:02'


class Searcher:
    """
    搜索功能，在树或者列表中搜索
    :param target 要搜索的目标，比如树，或者列表
    :param main_widget 主部件，用于停留dock窗口
    """

    def __init__(self, target, main_widget):
        self.target = target
        # dock 窗口
        self.dock_widget = SearcherDockWidget(main_widget)
        self.dock_widget.hide()
        # 存储以第一次匹配得到的元素字典，{id(item): [[(0,0)], [(0,1)]]}，key为item的id，value为list，存储每次匹配到的索引段列表，
        # 可以作为当前元素的搜索历史记录
        self.search_item_dict = dict()
        # 存储匹配到的元素列表记录，[[item0, item1], [item0]]，列表的最后永远是最新的元素匹配记录
        self.match_item_records = list()
        # 上一次匹配的文本长度
        self.last_search_text_len = 0
        # 给target设置视图代理对象
        self.target.setItemDelegate(SearchStyledItemDelegate(self.target, self.search_item_dict,
                                                             self.match_item_records))
        self.connect_signal()

    def connect_signal(self):
        # 连接搜索信号
        self.dock_widget.line_edit.search_text_signal.connect(self.search)
        # 回退搜索信号
        self.dock_widget.line_edit.back_select_signal.connect(self.backspace_search)
        # 清空搜索信号
        self.dock_widget.line_edit.clear_search_signal.connect(self.clear_search_data)
        # 上下选择箭头信号
        self.dock_widget.line_edit.up_down_select_signal.connect(self.up_down_select_item)

    def show_search(self):
        self.dock_widget.line_edit.start_search(self.target)

    def continue_search(self):
        # 如果搜索控件未隐藏，那么将焦点设回到搜索框
        if not self.dock_widget.isHidden():
            self.dock_widget.line_edit.setFocus()

    def clear_search_data(self):
        # 容器清空
        self.search_item_dict.clear()
        self.match_item_records.clear()
        self.clear_row_index()
        self.last_search_text_len = 0

    def search(self, text):
        # 转化为每次输入都是一个字符的形式匹配，这样才能匹配回退搜索，每次删除一个字符
        # 例如利用输入法，一次性输入 abc，那么匹配时将进行 a，ab，abc 三次匹配
        match_result_len = 0
        # 每次处理时，应该在上次搜索的基础上进行搜索
        for i in range(self.last_search_text_len, len(text)):
            # 构造当前搜索字符串
            search_text = text[: i + 1]
            match_items = list()
            # 如果搜索过，在当前的小范围内搜索
            if self.match_item_records:
                self.smart_match_text(search_text, match_items)
            else:
                # 如果还没搜索过，用迭代器，在所有节点中搜寻
                self.iterate_search(search_text, match_items)
            self.match_item_records.append(match_items)
            match_result_len = len(match_items)
        # 记录已经匹配的长度
        self.last_search_text_len = len(text)
        # 如果匹配不到，把输入框文本变为错误颜色
        if not match_result_len:
            self.dock_widget.line_edit.paint_wrong_color()
        # 设置焦点
        self.set_selected_focus()
        # 在设置完搜索控件的焦点后，应将焦点设置回搜索框，否则无法继续输入搜索
        self.dock_widget.line_edit.setFocus()
        # 给子类一个处理特有逻辑的机会
        self.search_post_process()

    def backspace_search(self):
        if self.match_item_records:
            # 每次回退，都需要将上次匹配文本长度减1
            self.last_search_text_len -= 1
            # 退格弹出容器最后一个元素
            pop_items = self.match_item_records.pop()
            # 弹出匹配到的元素索引
            for k, v in self.search_item_dict.items():
                for item in pop_items:
                    if k == id(item):
                        v.pop()
            # 如果已经删除了所有字符，或者能匹配到，将输入框文本变为正常颜色
            if not self.match_item_records or self.match_item_records[-1]:
                self.dock_widget.line_edit.paint_right_color()
            # 渲染，触发界面绘制刷新
            self.target.viewport().update()
            # 给子类一个处理特有逻辑的机会
            self.search_post_process()

    def up_down_select_item(self, key):
        if not self.match_item_records:
            return
        item_records = self.match_item_records[-1]
        # 如果当前节点在搜索列表中，按索引查找
        if self.target.currentItem() in item_records:
            index = item_records.index(self.target.currentItem())
            if key == Qt.Key.Key_Up:
                next_item = item_records[index - 1]
            else:
                next_item = item_records[index + 1 if index < len(item_records) - 1 else 0]
        else:
            # 如果当前节点不在搜索列表中，找出离当前元素最近的搜索节点，也就是选中元素并非搜索高亮节点
            up_item, next_item = self.get_up_down_next(item_records, self.target.currentItem())
            if key == Qt.Key.Key_Up:
                # 找出离当前元素最近的上一个元素
                next_item = up_item
            else:
                # 找出离当前元素最近的下一个元素
                next_item = next_item
        self.target.set_selected_focus(next_item)
        # 在设置完搜索控件的焦点后，应将焦点设置回搜索框，否则无法继续输入搜索
        self.dock_widget.line_edit.setFocus()

    def get_up_down_next(self, item_list, item):
        # 如果查找元素小于第一个元素或大于最后一个元素，则返回(-1，0)
        if self.get_row_index(item) < self.get_row_index(item_list[0]) \
                or self.get_row_index(item) > self.get_row_index(item_list[-1]):
            return item_list[-1], item_list[0]
        # 最终查找到只有两个元素，且查找在元素在其范围之内，返回
        if len(item_list) == 2 \
                and self.get_row_index(item_list[0]) < self.get_row_index(item) < self.get_row_index(item_list[1]):
            return item_list[0], item_list[1]
        # 获取中间索引
        mid_idx = len(item_list) >> 1
        # 如果中间数大于查找元素，查找左边元素，否则查找右边
        if self.get_row_index(item_list[mid_idx]) - self.get_row_index(item) > 0:
            return self.get_up_down_next(item_list[0: mid_idx + 1], item)
        else:
            return self.get_up_down_next(item_list[mid_idx:], item)

    def simple_match_text(self, text, item, match_items):
        smart_matcher = SmartMatcher(text)
        result = smart_matcher.match(self.get_item_text(item))
        if result:
            # 将匹配成功的信息放入列表
            match_items.append(item)
            self.search_item_dict[id(item)] = [result]

    def smart_match_text(self, text, match_items):
        last_match_items = self.match_item_records[-1]
        # 构建搜索器
        smart_matcher = SmartMatcher(text)
        for item in last_match_items:
            match_result = smart_matcher.match(self.get_item_text(item))
            if match_result:
                # 匹配成功，添加匹配成功的元素
                match_items.append(item)
                self.search_item_dict.get(id(item)).append(match_result)

    def set_selected_focus(self):
        if self.match_item_records and self.match_item_records[-1]:
            self.target.set_selected_focus(self.match_item_records[-1][0])

    def get_item_text(self, item) -> str:
        ...

    def search_post_process(self):
        ...

    def clear_row_index(self):
        ...

    def iterate_search(self, text, match_items):
        ...

    def get_row_index(self, item) -> int:
        ...
