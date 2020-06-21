# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conn_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog
from sys_info_storage.sqlite import *
from db_info import DBExecutor


class Ui_Dialog(QDialog):

    _signal = QtCore.pyqtSignal(Connection)

    def __init__(self, connection, dialog_title):
        super().__init__()
        self.dialog = self
        self.dialog_title = dialog_title
        self.connection = connection
        self._translate = QtCore.QCoreApplication.translate
        self.setupUi()

    def setupUi(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(387, 332)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.dialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(self.dialog)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.conn_name = QtWidgets.QLabel(self.dialog)
        self.conn_name.setObjectName("conn_name")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.conn_name)
        self.conn_name_text = QtWidgets.QLineEdit(self.dialog)
        self.conn_name_text.setObjectName("conn_name_text")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.conn_name_text)
        self.verticalLayout_2.addLayout(self.formLayout_2)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.host = QtWidgets.QLabel(self.dialog)
        self.host.setObjectName("host")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.host)
        self.host_text = QtWidgets.QLineEdit(self.dialog)
        self.host_text.setObjectName("host_text")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.host_text)
        self.port = QtWidgets.QLabel(self.dialog)
        self.port.setObjectName("port")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.port)
        self.port_text = QtWidgets.QLineEdit(self.dialog)
        self.port_text.setObjectName("port_text")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.port_text)
        self.user = QtWidgets.QLabel(self.dialog)
        self.user.setObjectName("user")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.user)
        self.user_text = QtWidgets.QLineEdit(self.dialog)
        self.user_text.setObjectName("user_text")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.user_text)
        self.pwd = QtWidgets.QLabel(self.dialog)
        self.pwd.setObjectName("pwd")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.pwd)
        self.pwd_text = QtWidgets.QLineEdit(self.dialog)
        self.pwd_text.setObjectName("pwd_text")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.pwd_text)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.blank = QtWidgets.QLabel(self.dialog)
        self.blank.setText("")
        self.blank.setObjectName("blank")
        self.verticalLayout_2.addWidget(self.blank)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.test_conn = QtWidgets.QPushButton(self.dialog)
        self.test_conn.setObjectName("test_conn")
        self.horizontalLayout.addWidget(self.test_conn)
        self.label = QtWidgets.QLabel(self.dialog)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.ok = QtWidgets.QPushButton(self.dialog)
        self.ok.setObjectName("ok")
        # todo 确定按钮默认不可用，只有当输入框都有值才可用
        self.ok.setDisabled(False)
        self.horizontalLayout.addWidget(self.ok)
        self.cancel = QtWidgets.QPushButton(self.dialog)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        # 测试连接按钮：点击触发测试mysql连接功能
        self.test_conn.clicked.connect(self.test_connection)
        # 确定按钮：点击触发添加连接记录到系统库中，并增加到展示界面
        self.ok.clicked.connect(self.add_conn)
        # 取消按钮：点击则关闭对话框
        self.cancel.clicked.connect(self.dialog.close)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate("Dialog", self.dialog_title))
        self.title.setText(self._translate("Dialog", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">mysql连接</span></p></body></html>"))
        self.conn_name.setText(self._translate("Dialog", "连接名："))
        self.host.setText(self._translate("Dialog", "主机："))
        self.port.setText(self._translate("Dialog", "端口号："))
        self.user.setText(self._translate("Dialog", "用户名："))
        self.pwd.setText(self._translate("Dialog", "密码："))
        self.test_conn.setText(self._translate("Dialog", "测试连接"))
        self.ok.setText(self._translate("Dialog", "确定"))
        self.cancel.setText(self._translate("Dialog", "取消"))
        # 回显
        if self.connection.id:
            self.conn_name_text.setText(self._translate("Dialog", self.connection.name))
            self.host_text.setText(self._translate("Dialog", self.connection.host))
            port = str(self.connection.port) if self.connection.port else None
            self.port_text.setText(self._translate("Dialog", port))
            self.user_text.setText(self._translate("Dialog", self.connection.user))
            self.pwd_text.setText(self._translate("Dialog", self.connection.pwd))
        else:
            self.host_text.setText(self._translate("Dialog", "localhost"))
            self.port_text.setText(self._translate("Dialog", "3306"))
            self.user_text.setText(self._translate("Dialog", "root"))

    def check_text(self, foc):
        print(foc)

    def get_input(self):
        conn_name = self.conn_name_text.text()
        host = self.host_text.text()
        port = int(self.port_text.text())
        user = self.user_text.text()
        pwd = self.pwd_text.text()
        return Connection(self.connection.id, conn_name, host, port, user, pwd)

    def test_connection(self):
        """测试连接"""
        self.dialog.setDisabled(True)
        new_conn = self.get_input()
        try:
            with DBExecutor(
                    new_conn.host,
                    new_conn.port,
                    new_conn.user,
                    new_conn.pwd
            ) as cur:
                cur.test_conn()
            self.pop_msg('连接成功\t')
        except Exception as e:
            self.pop_msg(f'连接失败\t\n{e.args[0]} - {e.args[1]}')
            print(e)
        finally:
            self.dialog.setDisabled(False)

    def add_conn(self):
        """添加新的连接记录到系统库中"""
        new_conn = self.get_input()
        if self.dialog_title == '编辑连接':
            update_conn(new_conn)
        elif self.dialog_title == '添加连接':
            add_conn(new_conn)
            new_conn = get_new_conn()
        self.pop_msg('保存成功\t')
        self.dialog.close()
        self._signal.emit(new_conn)

    def pop_msg(self, msg):
        QMessageBox.information(QMessageBox(), 'mysql', msg, QMessageBox.Ok)


# if __name__ == '__main__':
#     import sys
#
#     app = QtWidgets.QApplication(sys.argv)
#     conn = Connection(None, 'centos121', 'centos121', 3306, 'root', 'admin')
#     ui = Ui_Dialog(conn)
#     ui.show()
#     sys.exit(app.exec_())