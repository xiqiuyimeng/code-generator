# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'static/ui/about.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt

from src.constant.constant import ABOUT_TITLE, GENERATOR_TITLE, ABOUT_MYBATIS_TITLE, ABOUT_MYBATIS_INFO, \
    ABOUT_SPRING_TITLE, ABOUT_SPRING_INFO, ABOUT_PATH_TITLE, APPOINT_PATH, APPOINT_PATH_INFO, APPOINT_PROJECT, \
    APPOINT_PROJECT_INFO
from src.scrollable_widget.scrollable_widget import MyScrollArea


class AboutUI(QtWidgets.QDialog):

    def __init__(self, screen_rect):
        super().__init__()
        self.main_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("about_dialog")
        self.setFixedSize(self.main_screen_rect.width() * 0.8, self.main_screen_rect.height() * 0.8)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.about_frame = QtWidgets.QFrame(self)
        self.about_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.about_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.about_frame.setObjectName("about_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.about_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.about_scrollArea = MyScrollArea(self.about_frame)
        self.about_scrollArea.setWidgetResizable(True)
        self.about_scrollArea.setObjectName("about_scrollArea")
        self.about_scroll_widget = QtWidgets.QWidget()
        self.about_scroll_widget.setObjectName("about_scroll_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.about_scroll_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.about_title = QtWidgets.QLabel(self.about_scroll_widget)
        self.about_title.setObjectName("about_title")
        self.gridLayout.addWidget(self.about_title, 0, 0, 1, 4)
        self.generator_title = QtWidgets.QLabel(self.about_scroll_widget)
        self.generator_title.setObjectName("generator_title")
        self.gridLayout.addWidget(self.generator_title, 1, 0, 1, 1)
        self.mybatis_generator_title = QtWidgets.QLabel(self.about_scroll_widget)
        self.mybatis_generator_title.setObjectName("mybatis_generator_title")
        self.gridLayout.addWidget(self.mybatis_generator_title, 2, 0, 1, 1)
        self.about_mybatis = QtWidgets.QLabel(self.about_scroll_widget)
        self.about_mybatis.setObjectName("about_mybatis")
        self.gridLayout.addWidget(self.about_mybatis, 2, 1, 1, 3)
        self.spring_generator_title = QtWidgets.QLabel(self.about_scroll_widget)
        self.spring_generator_title.setObjectName("spring_generator_title")
        self.gridLayout.addWidget(self.spring_generator_title, 3, 0, 1, 1)
        self.about_spring = QtWidgets.QLabel(self.about_scroll_widget)
        self.about_spring.setObjectName("about_spring")
        self.gridLayout.addWidget(self.about_spring, 3, 1, 1, 3)
        self.path_title = QtWidgets.QLabel(self.about_scroll_widget)
        self.path_title.setObjectName("path_title")
        self.gridLayout.addWidget(self.path_title, 4, 0, 1, 1)
        self.appoint_path = QtWidgets.QLabel(self.about_scroll_widget)
        self.appoint_path.setObjectName("appoint_path")
        self.gridLayout.addWidget(self.appoint_path, 5, 0, 1, 1)
        self.appoint_path_info = QtWidgets.QLabel(self.about_scroll_widget)
        self.appoint_path_info.setObjectName("appoint_path_info")
        self.gridLayout.addWidget(self.appoint_path_info, 5, 1, 1, 3)
        self.appoint_project = QtWidgets.QLabel(self.about_scroll_widget)
        self.appoint_project.setObjectName("appoint_project")
        self.gridLayout.addWidget(self.appoint_project, 6, 0, 1, 1)
        self.appoint_project_info = QtWidgets.QLabel(self.about_scroll_widget)
        self.appoint_project_info.setObjectName("appoint_project_info")
        self.gridLayout.addWidget(self.appoint_project_info, 6, 1, 1, 3)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.about_scrollArea.setWidget(self.about_scroll_widget)
        self.verticalLayout.addWidget(self.about_scrollArea)
        self.verticalLayout_frame.addWidget(self.about_frame)

        self.about_title.setText(ABOUT_TITLE)
        self.generator_title.setText(GENERATOR_TITLE)
        self.mybatis_generator_title.setText(ABOUT_MYBATIS_TITLE)
        self.about_mybatis.setText(ABOUT_MYBATIS_INFO)
        self.spring_generator_title.setText(ABOUT_SPRING_TITLE)
        self.about_spring.setText(ABOUT_SPRING_INFO)
        self.path_title.setText(ABOUT_PATH_TITLE)
        self.appoint_path.setText(APPOINT_PATH)
        self.appoint_path_info.setText(APPOINT_PATH_INFO)
        self.appoint_project.setText(APPOINT_PROJECT)
        self.appoint_project_info.setText(APPOINT_PROJECT_INFO)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.ActivationChange and not self.isHidden():
            self.close()
