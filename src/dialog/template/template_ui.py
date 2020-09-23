# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'template.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QRect

from src.dialog.template.tab_bar_style import TabWidget
from src.scrollable_widget.scrollable_widget import MyTextBrowser, MyTextEdit
from src.sys.sys_info_storage.template_sqlite import TemplateSqlite, Template


class TemplateDialog(QtWidgets.QDialog):

    def __init__(self, title, screen_rect, template=None):
        super().__init__()
        self.title = title
        self.main_screen_rect = screen_rect
        self.template = template
        self.tab_names = tuple(filter(lambda k: k.endswith("_tp"), self.template._fields))
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
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
        self.verticalLayout.addWidget(self.template_frame)
        self.retranslateUi()
        self.template_tab_widget.setCurrentIndex(0)
        self.setStyleSheet("""#template_title{
            font-size:20px;
            font-family:楷体;
            font-weight:500;
            /*文字居中*/
            qproperty-alignment:AlignHCenter;
        }""")

    def set_up_show_tab(self, tab, tab_name):
        self.verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        self.verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        self.text_browser = MyTextBrowser(tab)
        self.text_browser.setLineWrapMode(MyTextBrowser.NoWrap)
        self.text_browser.setObjectName("text_browser")
        # 以纯文本形式显示
        self.text_browser.setPlainText(eval(f'self.template.{tab_name}'))
        self.verticalLayout_scroll.addWidget(self.set_up_line_number(tab, self.text_browser.document().lineCount()))
        self.verticalLayout_scroll.addWidget(self.text_browser)

    def set_up_edit_tab(self, tab, tab_name):
        self.verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        self.verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        self.text_edit = MyTextEdit(tab)
        self.text_edit.setObjectName("text_edit")
        # 以纯文本形式显示
        self.text_edit.setPlainText(eval(f'self.template.{tab_name}'))
        self.verticalLayout_scroll.addWidget(self.set_up_line_number(tab, self.text_edit.document().lineCount()))
        self.verticalLayout_scroll.addWidget(self.text_edit)

    def set_up_line_number(self, parent, line_count):
        # 限制标签的大小
        num_cut = QtWidgets.QLabel(parent)
        num_cut.setFixedWidth(30)
        num_cut.setStyleSheet('background-color:royalblue')
        num = QtWidgets.QLabel(num_cut)
        # 生成行号序列
        line_nums = '\n'.join([str(i) for i in range(1, line_count + 1)])
        num.setText(line_nums)
        num.adjustSize()
        return num_cut

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.template_title.setText(self.title)
        self.template_name_label.setText(_translate("Dialog", "模板名称"))
        self.template_name.setText(_translate("Dialog", self.template.tp_name))
        self.template_content_label.setText(_translate("Dialog", "模板内容"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    t = TemplateSqlite().get_using_template()
    r = QRect(0, 0, 1152, 810)
    new_t = Template()
    ui = TemplateDialog("新建", r, t)
    ui.show()
    sys.exit(app.exec_())
