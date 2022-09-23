# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'static/ui/about.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from src.constant_.constant import HELP_TITLE, HELP_MYSQL_CONN_TITLE, HELP_MYSQL_CONN_INFO, HELP_SELECT_COL_TITLE, \
    HELP_SELECT_COL_INFO, HELP_PATH_GENERATOR_TITLE, HELP_PATH_GENERATOR_INFO, HELP_PROJECT_GENERATOR_TITLE, \
    HELP_PROJECT_GENERATOR_INFO
from src.scrollable_widget.scrollable_widget import MyScrollArea


class HelpUI(QtWidgets.QDialog):

    def __init__(self, screen_rect):
        super().__init__()
        self.main_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("help_dialog")
        self.setFixedSize(self.main_screen_rect.width() * 0.8, self.main_screen_rect.height() * 0.8)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.help_frame = QtWidgets.QFrame(self)
        self.help_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.help_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.help_frame.setObjectName("help_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.help_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.help_scrollArea = MyScrollArea(self.help_frame)
        self.help_scrollArea.setWidgetResizable(True)
        self.help_scrollArea.setObjectName("help_scrollArea")
        self.help_scroll_widget = QtWidgets.QWidget()
        self.help_scroll_widget.setObjectName("help_scroll_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.help_scroll_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.help_title = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_title.setObjectName("help_title")
        self.gridLayout.addWidget(self.help_title, 0, 0, 1, 4)
        self.help_mysql_conn_title = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_mysql_conn_title.setObjectName("help_mysql_conn_title")
        self.gridLayout.addWidget(self.help_mysql_conn_title, 1, 0, 1, 1)
        self.help_mysql_conn_info = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_mysql_conn_info.setObjectName("help_mysql_conn_info")
        self.gridLayout.addWidget(self.help_mysql_conn_info, 1, 1, 1, 3)
        self.help_select_col_title = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_select_col_title.setObjectName("help_select_col_title")
        self.gridLayout.addWidget(self.help_select_col_title, 2, 0, 1, 1)
        self.help_select_col_info = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_select_col_info.setObjectName("help_select_col_info")
        self.gridLayout.addWidget(self.help_select_col_info, 2, 1, 1, 3)
        self.help_path_generator_title = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_path_generator_title.setObjectName("help_path_generator_title")
        self.gridLayout.addWidget(self.help_path_generator_title, 3, 0, 1, 1)
        self.help_path_generator_info = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_path_generator_info.setObjectName("help_path_generator_info")
        self.gridLayout.addWidget(self.help_path_generator_info, 3, 1, 1, 3)
        self.help_project_generator_title = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_project_generator_title.setObjectName("help_project_generator_title")
        self.gridLayout.addWidget(self.help_project_generator_title, 4, 0, 1, 1)
        self.help_project_generator_info = QtWidgets.QLabel(self.help_scroll_widget)
        self.help_project_generator_info.setObjectName("help_project_generator_info")
        self.gridLayout.addWidget(self.help_project_generator_info, 4, 1, 1, 3)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.help_scrollArea.setWidget(self.help_scroll_widget)
        self.verticalLayout.addWidget(self.help_scrollArea)
        self.verticalLayout_frame.addWidget(self.help_frame)

        self.help_title.setText(HELP_TITLE)
        self.help_mysql_conn_title.setText(HELP_MYSQL_CONN_TITLE)
        self.help_mysql_conn_info.setText(HELP_MYSQL_CONN_INFO)
        self.help_select_col_title.setText(HELP_SELECT_COL_TITLE)
        self.help_select_col_info.setText(HELP_SELECT_COL_INFO)
        self.help_path_generator_title.setText(HELP_PATH_GENERATOR_TITLE)
        self.help_path_generator_info.setText(HELP_PATH_GENERATOR_INFO)
        self.help_project_generator_title.setText(HELP_PROJECT_GENERATOR_TITLE)
        self.help_project_generator_info.setText(HELP_PROJECT_GENERATOR_INFO)

    def changeEvent(self, event):
        # 如果窗口不是当前活跃，那么就关闭
        if not self.isActiveWindow():
            self.close()
