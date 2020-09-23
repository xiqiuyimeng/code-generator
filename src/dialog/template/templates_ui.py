# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton, QMenu, QAction

from src.constant.constant import TEMPLATE_TABLE_HEADER_LABELS, COPY_ACTION, DEL_ACTION, TEMPLATE_LIST_HEADER, \
    ADD_TEMPLATE, BATCH_COPY_TEMPLATE, BATCH_DEL_TEMPLATE, TEMPLATE_QUIT, USE_TEMPLATE_CELL, CAT_TEMPLATE_CELL, \
    EDIT_TEMPLATE_CELL, COPY_TEMPLATE_CELL, DEL_TEMPLATE_CELL, QUIT_QUESTION
from src.dialog.draggable_dialog import DraggableDialog
from src.func.operate_template_thread import OperateTemplate
from src.little_widget.message_box import pop_question
from src.scrollable_widget.scrollable_widget import MyTableWidget
from src.sys.sys_info_storage.template_sqlite import TemplateSqlite
from src.table.table_header import CheckBoxHeader
from src.table.table_item import MyTableWidgetItem


class TemplatesDialog(DraggableDialog):

    def __init__(self, screen_rect):
        super().__init__()
        self.main_screen_rect = screen_rect
        # 二维，元素为元祖，（index、tp_name）
        self.selected_templates = list()
        # 初始化需要使用的icon
        self.icon = QIcon(":/icon/exec.png")
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        self.resize(self.main_screen_rect.width() * 0.6, self.main_screen_rect.height() * 0.6)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.table_frame = QtWidgets.QFrame(self)
        self.table_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.table_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.table_frame.setObjectName("template_table_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.table_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.table_header_label = QtWidgets.QLabel(self.table_frame)
        self.table_header_label.setObjectName("template_table_header_label")
        self.verticalLayout.addWidget(self.table_header_label)
        # 添加表格
        self.tableWidget = MyTableWidget(self.table_frame)
        # 取消水平滑块
        self.tableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName("tableWidget")
        # 表头
        self.make_header()
        # 填充表格数据
        self.fill_table(TemplateSqlite().get_templates())
        # 交替行颜色
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.verticalLayout.addWidget(self.tableWidget)
        # 按钮区域 添加模板 批量复制 批量删除 退出
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.add_template = QtWidgets.QPushButton(self.table_frame)
        self.add_template.setObjectName("add_template")
        self.gridLayout.addWidget(self.add_template, 0, 0, 1, 1)
        self.batch_copy = QtWidgets.QPushButton(self.table_frame)
        self.batch_copy.setObjectName("batch_copy")
        self.gridLayout.addWidget(self.batch_copy, 0, 1, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.table_frame)
        self.gridLayout.addWidget(self.button_blank, 0, 2, 1, 1)
        self.batch_delete = QtWidgets.QPushButton(self.table_frame)
        self.batch_delete.setObjectName("batch_delete")
        self.gridLayout.addWidget(self.batch_delete, 0, 3, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.table_frame)
        self.quit_button.setObjectName("quit_button")
        self.gridLayout.addWidget(self.quit_button, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.main_layout.addWidget(self.table_frame)

        # 事件
        self.batch_copy.clicked.connect(self.batch_copy_templates)
        self.batch_delete.clicked.connect(self.batch_delete_templates)
        self.quit_button.clicked.connect(self.quit)

        self.tableWidget.item_checkbox_clicked.connect(lambda checked, field, row:
                                                       self.on_checkbox_changed(checked, field, row))

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.table_header_label.setText(TEMPLATE_LIST_HEADER)
        self.add_template.setText(ADD_TEMPLATE)
        self.batch_copy.setText(BATCH_COPY_TEMPLATE)
        self.batch_delete.setText(BATCH_DEL_TEMPLATE)
        self.quit_button.setText(TEMPLATE_QUIT)

    def make_header(self):
        self.tableWidget.setColumnCount(8)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader()
        self.table_header.setObjectName("table_header")
        self.tableWidget.setHorizontalHeader(self.table_header)
        self.tableWidget.setHorizontalHeaderLabels(TEMPLATE_TABLE_HEADER_LABELS)
        # 设置表头列宽度
        self.tableWidget.horizontalHeader().resizeSection(0, 60)
        self.tableWidget.horizontalHeader().resizeSection(2, 60)
        self.tableWidget.horizontalHeader().resizeSection(3, 60)
        self.tableWidget.horizontalHeader().resizeSection(4, 60)
        # 最后拉伸到最大
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 隐藏默认的行号
        self.tableWidget.verticalHeader().setHidden(True)
        self.table_header.select_all_clicked.connect(self.all_clicked)

    def fill_table(self, templates, start_row=0):
        for i, template in enumerate(templates):
            if start_row:
                i += start_row
            self.tableWidget.insertRow(i)
            table_check_item = MyTableWidgetItem(self.tableWidget)
            table_check_item.setCheckState(Qt.Unchecked)
            table_check_item.setText(i + 1)
            self.tableWidget.setItem(i, 0, table_check_item)
            self.table_header.all_header_combobox.append(table_check_item)
            n = 1
            for field in template:
                # 模板中的每一个字段
                if field is not None:
                    tp_item = MyTableWidgetItem(self.tableWidget)
                    tp_item.setText(field)
                    self.tableWidget.setItem(i, n, tp_item)
                    n += 1
            # 最后添加按钮，在序号为7的列
            self.tableWidget.setCellWidget(i, 7, self.make_tools(i, template.tp_name, template.is_using))
        self.tableWidget.resizeRowsToContents()

    def all_clicked(self, clicked):
        self.selected_templates.clear()
        [self.selected_templates.append(
            (checkbox.row(), self.tableWidget.item(checkbox.row(), checkbox.column() + 1).text())
        ) for checkbox in self.table_header.all_header_combobox]
        self.table_header.change_state(clicked)

    def on_checkbox_changed(self, checked, tp_name, row):
        """点击复选框"""
        header_checked = False
        if checked and (row, tp_name) not in self.selected_templates:
            self.selected_templates.append((row, tp_name))
            # 与表头联动
            if len(self.selected_templates) == len(self.table_header.all_header_combobox):
                header_checked = True
        elif not checked and (row, tp_name) in self.selected_templates:
            self.selected_templates.remove((row, tp_name))
        self.table_header.set_header_checked(header_checked)

    def batch_copy_templates(self, selected_templates=None):
        """批量复制"""
        already_selected = selected_templates if selected_templates else self.selected_templates
        if already_selected:
            OperateTemplate(self, COPY_ACTION, already_selected)

    def batch_delete_templates(self, selected_templates=None):
        """批量删除"""
        already_selected = selected_templates if selected_templates else self.selected_templates
        if already_selected:
            OperateTemplate(self, DEL_ACTION, already_selected)

    def make_tools(self, row, tp_name, is_used):
        """
        添加操作按钮
        :param row: 当前行
        :param tp_name: 模板名称
        :param is_used: 是否在使用，如果不在使用，需要展示使用按钮
        """
        tool_button = QToolButton(self)
        tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tool_button.setStatusTip('对模板的操作')
        tool_button.setPopupMode(QToolButton.InstantPopup)
        tool_button.setText('操作')
        tool_button.setIcon(self.icon)
        tool_button.setAutoRaise(True)
        menu = QMenu(self)
        # 没有使用的模板才需要这个按钮
        if is_used == '否':
            use_act = QAction(self.icon, USE_TEMPLATE_CELL, self)
            use_act.triggered.connect(lambda: self.use_action(row, tp_name))
            menu.addAction(use_act)
        cat_act = QAction(self.icon, CAT_TEMPLATE_CELL, self)
        cat_act.triggered.connect(lambda: self.cat_action(row, tp_name))
        menu.addAction(cat_act)
        edit_act = QAction(self.icon, EDIT_TEMPLATE_CELL, self)
        edit_act.triggered.connect(lambda: self.edit_action(row, tp_name))
        menu.addAction(edit_act)
        copy_act = QAction(self.icon, COPY_TEMPLATE_CELL, self)
        copy_act.triggered.connect(lambda: self.copy_action(row, tp_name))
        menu.addAction(copy_act)
        del_act = QAction(self.icon, DEL_TEMPLATE_CELL, self)
        del_act.triggered.connect(lambda: self.del_action(row, tp_name))
        menu.addAction(del_act)
        tool_button.setMenu(menu)
        return tool_button

    def use_action(self, row, tp_name):
        """设为使用中"""
        TemplateSqlite().change_using_template(tp_name)
        # 当前使用中的模板所在行
        old_row = -1
        # 渲染表格
        for i in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(i, 4)
            if item.text() == '是':
                item.setText('否')
                old_row = i
        self.tableWidget.item(row, 4).setText('是')
        # 处理操作菜单
        self.tableWidget.setCellWidget(row, 7, self.make_tools(
            row, self.tableWidget.item(row, 1).text(), '是'
        ))
        # 如果之前使用的存在，重新构建下操作菜单
        if old_row >= 0:
            self.tableWidget.setCellWidget(old_row, 7, self.make_tools(
                old_row, self.tableWidget.item(old_row, 1).text(), '否'
            ))

    def cat_action(self, row, tp_name):
        print(row, CAT_TEMPLATE_CELL)

    def edit_action(self, row, tp_name):
        print(row, EDIT_TEMPLATE_CELL)

    def copy_action(self, row, tp_name):
        """复制模板，具体实现为批量复制方法"""
        self.batch_copy_templates(((row, tp_name),))

    def del_action(self, row, tp_name):
        """删除模板，具体实现为批量删除方法"""
        self.batch_delete_templates(((row, tp_name),))

    def keyPressEvent(self, event):
        """在按esc时，执行自定义的quit方法"""
        if event.key() == Qt.Key_Escape:
            self.quit()
        else:
            super().keyPressEvent(event)

    def quit(self):
        """关闭前判断下是否存在使用中的模板，若不存在，弹窗提示"""
        if not TemplateSqlite().get_using_template():
            if pop_question('警告', QUIT_QUESTION):
                self.close()
        else:
            self.close()
