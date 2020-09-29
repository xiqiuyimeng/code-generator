# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

from src.constant.constant import JAVA_TP_DESC, MAPPER_TP_DESC, XML_TP_DESC, SERVICE_TP_DESC, SERVICE_IMPL_TP_DESC, \
    CONTROLLER_TP_DESC, QUIT, TP_HELP, TP_INTRODUCE, TP_INFO, TP_ENGINE, TP_ENGINE_INFO, TP_KEY_DESC
from src.dialog.draggable_dialog import DraggableDialog
from src.dialog.template.tab_bar_style import TabWidget
from src.scrollable_widget.scrollable_widget import MyTextBrowser

_author_ = 'luwt'
_date_ = '2020/9/27 14:59'


class TemplateHelpDialog(DraggableDialog):

    close_signal = pyqtSignal()

    def __init__(self, screen_rect, current_index, tab_names):
        super().__init__()
        self.title = '模板帮助信息'
        self.main_screen_rect = screen_rect
        self.current_index = current_index
        self.tab_names = tab_names
        self.tp_desc = [JAVA_TP_DESC, MAPPER_TP_DESC, XML_TP_DESC, SERVICE_TP_DESC,
                        SERVICE_IMPL_TP_DESC, CONTROLLER_TP_DESC]
        self.content = dict(zip(self.tab_names, self.tp_desc))
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(self.main_screen_rect.width() * 0.8, self.main_screen_rect.height() * 0.8)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.template_help_frame = QtWidgets.QFrame(self)
        self.template_help_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.template_help_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.template_help_frame.setObjectName("template_help_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.template_help_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.template_help_title = QtWidgets.QLabel(self.template_help_frame)
        self.template_help_title.setObjectName("template_help_title")
        self.verticalLayout_2.addWidget(self.template_help_title)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.template_help_label = QtWidgets.QLabel(self.template_help_frame)
        self.template_help_label.setObjectName("template_help_label")
        self.gridLayout.addWidget(self.template_help_label, 0, 0, 1, 1)
        self.template_help_info = QtWidgets.QLabel(self.template_help_frame)
        self.template_help_info.setObjectName("template_help_info")
        self.template_help_info.setWordWrap(True)
        self.gridLayout.addWidget(self.template_help_info, 0, 1, 1, 1)
        self.template_engine_label = QtWidgets.QLabel(self.template_help_frame)
        self.template_engine_label.setObjectName("template_engine_label")
        self.gridLayout.addWidget(self.template_engine_label, 1, 0, 1, 1)
        self.template_engine = QtWidgets.QLabel(self.template_help_frame)
        self.template_engine.setObjectName("template_engine")
        self.gridLayout.addWidget(self.template_engine, 1, 1, 1, 1)
        self.template_desc = QtWidgets.QLabel(self.template_help_frame)
        self.template_desc.setObjectName("template_desc")
        self.gridLayout.addWidget(self.template_desc, 2, 0, 1, 1)

        # 构建tab页
        self.template_help_tab_widget = TabWidget(self.template_help_frame)
        self.template_help_tab_widget.setObjectName("template_help_tab_widget")
        for tab_name in self.tab_names:
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"{tab_name}")
            setattr(self, f"self.{tab_name}", tab)
            self.set_up_tab(tab, self.content.get(tab_name))
            self.template_help_tab_widget.addTab(tab, tab_name[:-3])
        self.gridLayout.addWidget(self.template_help_tab_widget, 3, 0, 1, 2)
        self.verticalLayout_2.addLayout(self.gridLayout)

        self.button_gridLayout = QtWidgets.QGridLayout()
        self.button_gridLayout.setObjectName("button_gridLayout")
        for i in range(3):
            blank = QtWidgets.QLabel(self.template_help_frame)
            self.button_gridLayout.addWidget(blank, 0, i, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.template_help_frame)
        self.quit_button.setObjectName("quit_button")
        self.button_gridLayout.addWidget(self.quit_button, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.button_gridLayout)
        self.verticalLayout.addWidget(self.template_help_frame)

        self.quit_button.clicked.connect(self.quit)
        self.template_help_tab_widget.setCurrentIndex(self.current_index)
        self.retranslate_ui()

    def retranslate_ui(self):
        self.setWindowTitle(QtCore.QCoreApplication.translate("Dialog", self.title))
        self.template_help_title.setText(TP_HELP)
        self.template_help_label.setText(TP_INTRODUCE)
        self.template_help_info.setText(TP_INFO)
        self.template_engine_label.setText(TP_ENGINE)
        self.template_engine.setText(TP_ENGINE_INFO)
        self.template_desc.setText(TP_KEY_DESC)
        self.quit_button.setText(QUIT)

    def set_up_tab(self, tab, content):
        self.verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        self.verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        self.help_text_browser = MyTextBrowser(tab)
        self.help_text_browser.setObjectName("help_text_browser")
        # 以纯文本形式显示
        self.help_text_browser.setPlainText(content)
        self.verticalLayout_scroll.addWidget(self.help_text_browser)

    def switch_tab(self, index):
        self.activateWindow()
        self.template_help_tab_widget.setCurrentIndex(index)

    def quit(self):
        self.close_signal.emit()
        self.close()

