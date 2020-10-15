# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap

from src.constant.constant import TP_NAME_AVAILABLE, TP_NAME_EXISTS, CAT_TEMPLATE_TITLE, ADD_TEMPLATE_TITLE, \
    EDIT_TEMPLATE_TITLE, NO_TP_NAME, HELP_BUTTON, SAVE, QUIT, TP_NAME, TP_CONTENT
from src.dialog.draggable_dialog import DraggableDialog
from src.dialog.template.tab_bar_style import TabWidget
from src.dialog.template.template_help_ui import TemplateHelpDialog
from src.little_widget.message_box import pop_fail
from src.read_qrc.read_file import read_qss
from src.scrollable_widget.scrollable_widget import MyTextBrowser, MyTextEdit
from src.sys.sys_info_storage.template_sqlite import Template, TemplateSqlite


class TemplateDialog(DraggableDialog):

    result = pyqtSignal(str)
    # 关闭信号，关闭时发送当前窗口dialog_id
    close_signal = pyqtSignal(str)

    def __init__(self, gui, dialog_id, title, screen_rect, template=None):
        super().__init__()
        self.gui = gui
        self.dialog_id = dialog_id
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
        if self.title == CAT_TEMPLATE_TITLE:
            self.template_name = QtWidgets.QLabel(self.template_frame)
        else:
            self.template_name = QtWidgets.QLineEdit(self.template_frame)
            self.template_name.textEdited.connect(self.check_name_available)
            self.template_name.setMaxLength(50)
        self.template_name.setObjectName("template_name")
        self.gridLayout.addWidget(self.template_name, 0, 1, 1, 1)
        self.name_check_blank = QtWidgets.QLabel(self.template_frame)
        self.gridLayout.addWidget(self.name_check_blank, 1, 0, 1, 1)
        self.name_check_splitter = QtWidgets.QSplitter(self.template_frame)
        self.name_check_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.name_check_splitter.setObjectName("name_check_splitter")
        self.name_check_splitter.setHandleWidth(0)
        self.gridLayout.addWidget(self.name_check_splitter, 1, 1, 1, 1)
        self.name_check_pic = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_pic.setObjectName("name_check_pic")
        self.name_check_prompt = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_prompt.setObjectName("name_check_prompt")

        self.template_content_label = QtWidgets.QLabel(self.template_frame)
        self.template_content_label.setObjectName("template_content_label")
        self.gridLayout.addWidget(self.template_content_label, 2, 0, 1, 1)
        self.template_tab_widget = TabWidget(self.template_frame)
        self.template_tab_widget.setObjectName("template_tab_widget")
        for tab_name in self.tab_names:
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"{tab_name}")
            setattr(self, f"self.{tab_name}", tab)
            if self.title == CAT_TEMPLATE_TITLE:
                self.set_up_show_tab(tab, tab_name)
            else:
                self.set_up_edit_tab(tab, tab_name)
            self.template_tab_widget.addTab(tab, tab_name[:-3])
        self.gridLayout.addWidget(self.template_tab_widget, 3, 0, 1, 2)

        self.verticalLayout_2.addLayout(self.gridLayout)
        # 按钮区
        self.button_gridLayout = QtWidgets.QGridLayout()
        self.button_gridLayout.setObjectName("button_gridLayout")
        self.support_button = QtWidgets.QPushButton(self.template_frame)
        self.support_button.setObjectName("support_button")
        self.button_gridLayout.addWidget(self.support_button, 0, 0, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.template_frame)
        self.button_gridLayout.addWidget(self.button_blank, 0, 1, 1, 1)
        if self.title == CAT_TEMPLATE_TITLE:
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
        self.button_gridLayout.addWidget(self.quit_button, 0, 3, 1, 1)
        self.quit_button.clicked.connect(self.dialog_close)
        self.support_button.clicked.connect(self.open_help)

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
        self.setWindowTitle(_translate("Dialog", self.title))
        self.template_title.setText(self.title)
        self.template_name_label.setText(_translate("Dialog", TP_NAME))
        self.template_name.setText(_translate("Dialog", self.template.tp_name))
        self.template_content_label.setText(_translate("Dialog", TP_CONTENT))
        self.support_button.setText(HELP_BUTTON)
        if self.title != CAT_TEMPLATE_TITLE:
            self.save_button.setText(SAVE)
        self.quit_button.setText(QUIT)

    def save_func(self):
        try:
            if not self.template_name.text():
                pop_fail(self.title, NO_TP_NAME)
            else:
                if self.title == ADD_TEMPLATE_TITLE:
                    self.add_new_template()
                elif self.title == EDIT_TEMPLATE_TITLE:
                    changed_text = dict()
                    if self.template.tp_name != self.template_name.text():
                        changed_text['tp_name'] = self.template_name.text()
                    for i in range(self.template_tab_widget.count()):
                        text = self.template_tab_widget.widget(i).text_edit.toPlainText()
                        original_text = eval(f'self.template.{self.tab_names[i]}')
                        if text != original_text:
                            changed_text[self.tab_names[i]] = text
                    if changed_text:
                        self.edit_template(self.template_name.text(), changed_text)
                    else:
                        self.dialog_close()
        except Exception as e:
            pop_fail(self.title, f'{e}')

    def add_new_template(self):
        """新建模板"""
        template_dict = self.template._asdict()
        template_dict['tp_name'] = self.template_name.text()
        for i in range(self.template_tab_widget.count()):
            template_dict[self.tab_names[i]] = self.template_tab_widget.widget(i).text_edit.toPlainText()
        TemplateSqlite().insert(template_dict)
        self.result.emit(template_dict.get('tp_name'))
        self.dialog_close()

    def edit_template(self, tp_name, changed_text):
        """编辑模板"""
        new_template_dict = dict(zip(Template._fields, (None,) * (len(Template._fields))))
        new_template_dict['id'] = self.template.id
        new_template_dict.update(changed_text)
        TemplateSqlite().update_selective(new_template_dict)
        self.result.emit(tp_name)
        self.dialog_close()

    def check_name_available(self, tp_name):
        """检查名称是否可用"""
        label_height = self.template_name.geometry().height()
        self.name_check_pic.setFixedWidth(label_height)
        if tp_name:
            name_available = TemplateSqlite().check_tp_name_available(tp_name, self.template.id)
            if name_available:
                prompt = TP_NAME_AVAILABLE.format(tp_name)
                style = "color:green"
                # 重载样式表
                self.template_name.setStyleSheet(read_qss())
                pm = QPixmap(":/icon/right.png").scaled(label_height * 0.6,
                                                        label_height * 0.6,
                                                        QtCore.Qt.IgnoreAspectRatio,
                                                        QtCore.Qt.SmoothTransformation)
            else:
                prompt = TP_NAME_EXISTS.format(tp_name)
                style = "color:red"
                self.template_name.setStyleSheet("#template_name{border-color:red;color:red}")
                pm = QPixmap(":/icon/wrong.png").scaled(label_height * 0.6,
                                                        label_height * 0.6,
                                                        QtCore.Qt.IgnoreAspectRatio,
                                                        QtCore.Qt.SmoothTransformation)
            self.name_check_pic.setPixmap(pm)
            self.name_check_prompt.setStyleSheet(style)
            self.name_check_prompt.setText(prompt)

    def open_help(self):
        if hasattr(self.gui, 'help'):
            self.gui.help.switch_tab(self.template_tab_widget.currentIndex())
        else:
            self.gui.help = TemplateHelpDialog(self.main_screen_rect,
                                               self.template_tab_widget.currentIndex(),
                                               self.tab_names)
            self.gui.help.show()
            self.gui.opened_window.append(self.gui.help)
            self.gui.help.close_signal.connect(self.remove_help_ui)

    def remove_help_ui(self):
        self.gui.opened_window.remove(self.gui.help)
        delattr(self.gui, 'help')

    def keyPressEvent(self, event):
        """在按esc时，执行自定义的关闭方法"""
        if event.key() == QtCore.Qt.Key_Escape:
            self.dialog_close()
        else:
            super().keyPressEvent(event)

    def dialog_close(self):
        self.close_signal.emit(self.dialog_id)
        self.close()


