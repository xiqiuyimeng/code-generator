# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

from src.dialog.draggable_dialog import DraggableDialog
from src.dialog.template.tab_bar_style import TabWidget
from src.little_widget.message_box import pop_fail
from src.scrollable_widget.scrollable_widget import MyTextBrowser, MyTextEdit
from src.sys.sys_info_storage.template_sqlite import Template, TemplateSqlite


class TemplateDialog(DraggableDialog):

    result = pyqtSignal(str)

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
            # 保存
            self.save_button.clicked.connect(self.save_func)
            self.button_gridLayout.addWidget(self.save_button, 0, 2, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.template_frame)
        self.quit_button.setObjectName("quit_button")
        # 关闭
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
        verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        tab.text_edit = MyTextEdit(tab)
        tab.text_edit.setObjectName("text_edit")
        # 以纯文本形式显示
        tab.text_edit.setPlainText(eval(f'self.template.{tab_name}'))
        verticalLayout_scroll.addWidget(tab.text_edit)

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

    def save_func(self):
        if not self.template_name.text():
            pop_fail(self.title, "请填写模板名称")
        else:
            if self.title == "新建":
                pass
            elif self.title == "编辑":
                changed_text = dict()
                if self.template.tp_name != self.template_name.text():
                    changed_text['tp_name'] = self.template_name.text()
                for i in range(self.template_tab_widget.count()):
                    text = self.template_tab_widget.widget(i).text_edit.toPlainText()
                    original_text = eval(f'self.template.{self.tab_names[i]}')
                    if text != original_text:
                        changed_text[self.tab_names[i]] = text
                if changed_text:
                    try:
                        self.edit_template(self.template_name.text(), changed_text)
                    except Exception as e:
                        pop_fail(self.title, e.args)

    def add_new_template(self):
        """新建模板"""
        pass

    def edit_template(self, tp_name, changed_text):
        """编辑模板"""
        new_template_dict = dict(zip(Template._fields, (None,) * (len(Template._fields))))
        new_template_dict['id'] = self.template.id
        new_template_dict.update(changed_text)
        TemplateSqlite().update_selective(new_template_dict)
        self.result.emit(tp_name)
        self.close()


