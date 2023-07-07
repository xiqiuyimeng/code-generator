# -*- coding: utf-8 -*-
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics, QTextDocument
from PyQt6.QtWidgets import QFrame, QLabel, QFormLayout

from src.constant.help.help_constant import TEXT_BROWSER_STYLE, MULTI_LINE_LABEL_STYLE
from src.view.custom_widget.scrollable_widget import ScrollArea, ScrollableTextBrowser

_author_ = 'luwt'
_date_ = '2023/6/14 16:03'


class HelpWidgetABC(ScrollArea):

    def __init__(self):
        super().__init__()
        self.canvas_content_frame: QFrame = ...
        self.canvas_content_layout: QFormLayout = ...
        self.setup_ui()

    def setup_ui(self):
        # 画布，用来承载控件
        self.canvas_content_frame = QFrame()
        self.canvas_content_frame.setObjectName('help_canvas_content_frame')
        # 设置画布控件
        self.set_canvas_widget(self.canvas_content_frame)
        # 画布布局
        self.canvas_content_layout = QFormLayout(self.canvas_content_frame)

        # 添加内容
        self.add_content()

        self.canvas_content_layout.addWidget(QLabel())

    def add_content(self):
        ...

    def add_label(self, label_text):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 拼接上样式
        label.setText(f'{MULTI_LINE_LABEL_STYLE}<p>{label_text}</p>')
        # 自动换行
        label.setWordWrap(True)

        # 计算高度
        # 创建QTextDocument对象并设置字体和文本
        doc = QTextDocument()
        doc.setDefaultFont(label.font())
        doc.setHtml(label.text())

        # 获取文本所需的最小矩形大小
        # 将行宽设置为label的宽度
        doc.setTextWidth(label.width())
        size = doc.documentLayout().documentSize()

        # 计算框架的高度（文本加上行间距）
        font_metrics = QFontMetrics(label.font())
        height = size.height() + (font_metrics.leading() if size.height() > font_metrics.height() else 0)

        # 高度固定
        label.setFixedHeight(height)
        self.canvas_content_layout.addRow(label)

    def add_row_label(self, label_text, help_label_text):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setObjectName('form_label')
        label.setText(label_text)
        help_label = QLabel()
        help_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        help_label.setText(f'{MULTI_LINE_LABEL_STYLE}<p>{help_label_text}</p>')
        # 自动换行
        help_label.setWordWrap(True)
        # 高度固定
        help_label.setFixedHeight(help_label.sizeHint().height())
        self.canvas_content_layout.addRow(label, help_label)

    def add_row_text_browser(self, label_text, browser_text):
        label = QLabel()
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        label.setObjectName('form_label')
        label.setText(label_text)
        content_browser = ScrollableTextBrowser()
        # 自动换行
        content_browser.setLineWrapMode(content_browser.LineWrapMode.WidgetWidth)

        # 使用 QTextDocument 设置文本，可以获取文本实际高度
        doc = QTextDocument()
        doc.setDefaultFont(content_browser.currentFont())
        # 设置样式，拼接富文本
        html_text = f'{TEXT_BROWSER_STYLE}<div>{browser_text}</div>'
        # 使用html来展示富文本，可以设置更多样式
        doc.setHtml(html_text)
        content_browser.setDocument(doc)

        font_metrics = QFontMetrics(content_browser.currentFont())
        line_height = font_metrics.height()
        # 为了美观，高度增加两行
        content_browser.setFixedHeight(doc.size().height() + (line_height << 1))
        self.canvas_content_layout.addRow(label, content_browser)
