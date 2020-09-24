# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets

from src.dialog.draggable_dialog import DraggableDialog
from src.dialog.template.tab_bar_style import TabWidget
from src.scrollable_widget.scrollable_widget import MyTextBrowser, MyTextEdit


class TemplateDialog(DraggableDialog):

    def __init__(self, title, screen_rect, template=None):
        super().__init__()
        self.title = title
        self.main_screen_rect = screen_rect
        self.template = template
        self.tab_names = tuple(filter(lambda k: k.endswith("_tp"), self.template._fields))
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.resize(self.main_screen_rect.width() * 0.8, self.main_screen_rect.height() * 0.8)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.template_frame = QtWidgets.QFrame(self)
        self.template_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.template_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.template_frame.setObjectName("template_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.template_frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.template_title = QtWidgets.QLabel(self.template_frame)
        self.template_title.setObjectName("template_title")
        self.verticalLayout_2.addWidget(self.template_title)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.template_name_label = QtWidgets.QLabel(self.template_frame)
        self.template_name_label.setObjectName("template_name_label")
        self.gridLayout.addWidget(self.template_name_label, 0, 0, 1, 1)
        if self.title == '查看':
            self.template_name = QtWidgets.QLabel(self.template_frame)
        else:
            self.template_name = QtWidgets.QLineEdit(self.template_frame)
        self.template_name.setObjectName("template_name")
        self.gridLayout.addWidget(self.template_name, 0, 1, 1, 1)
        self.template_content_label = QtWidgets.QLabel(self.template_frame)
        self.template_content_label.setObjectName("template_content_label")
        self.gridLayout.addWidget(self.template_content_label, 1, 0, 1, 1)
        self.template_tab_widget = TabWidget(self.template_frame)
        self.template_tab_widget.setObjectName("template_tab_widget")
        for tab_name in self.tab_names:
            exec(f'self.{tab_name} = QtWidgets.QWidget()')
            exec(f'self.{tab_name}.setObjectName("{tab_name}")')
            if self.title == '查看':
                exec(f'self.set_up_show_tab(self.{tab_name}, "{tab_name}")')
            else:
                exec(f'self.set_up_edit_tab(self.{tab_name}, "{tab_name}")')
            exec(f'self.template_tab_widget.addTab(self.{tab_name}, "{tab_name[:-3]}")')
        self.gridLayout.addWidget(self.template_tab_widget, 2, 0, 1, 2)

        self.verticalLayout_2.addLayout(self.gridLayout)
        # 按钮区
        self.button_gridLayout = QtWidgets.QGridLayout()
        self.button_gridLayout.setObjectName("button_gridLayout")
        self.support_button = QtWidgets.QPushButton(self.template_frame)
        self.support_button.setObjectName("support_button")
        self.button_gridLayout.addWidget(self.support_button, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.template_frame)
        self.button_gridLayout.addWidget(self.button_blank, 0, 1, 1, 1)
        if self.title == '查看':
            self.button_blank2 = QtWidgets.QLabel(self.template_frame)
            self.button_gridLayout.addWidget(self.button_blank2, 0, 2, 1, 1)
        else:
            self.save_button = QtWidgets.QPushButton(self.template_frame)
            self.save_button.setObjectName("save_button")
            self.button_gridLayout.addWidget(self.save_button, 0, 2, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.template_frame)
        self.quit_button.setObjectName("quit_button")
        self.quit_button.clicked.connect(self.close)
        self.button_gridLayout.addWidget(self.quit_button, 0, 3, 1, 1)

        self.verticalLayout_2.addLayout(self.button_gridLayout)
        self.verticalLayout.addWidget(self.template_frame)
        self.retranslateUi()
        self.template_tab_widget.setCurrentIndex(0)

    def set_up_show_tab(self, tab, tab_name):
        self.verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        self.verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        self.text_browser = MyTextBrowser(tab)
        self.text_browser.setLineWrapMode(MyTextBrowser.NoWrap)
        self.text_browser.setObjectName("text_browser")
        # 以纯文本形式显示
        self.text_browser.setPlainText(eval(f'self.template.{tab_name}'))
        self.verticalLayout_scroll.addWidget(self.text_browser)

    def set_up_edit_tab(self, tab, tab_name):
        self.verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        self.verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        self.text_edit = MyTextEdit(tab)
        self.text_edit.setObjectName("text_edit")
        # 以纯文本形式显示
        self.text_edit.setPlainText(eval(f'self.template.{tab_name}'))
        self.verticalLayout_scroll.addWidget(self.text_edit)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.template_title.setText(self.title)
        self.template_name_label.setText(_translate("Dialog", "模板名称"))
        self.template_name.setText(_translate("Dialog", self.template.tp_name))
        self.template_content_label.setText(_translate("Dialog", "模板内容"))
        self.support_button.setText("帮助信息")
        if self.title != '查看':
            self.save_button.setText("保存")
        self.quit_button.setText("退出")


