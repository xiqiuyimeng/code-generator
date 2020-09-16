# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from static import style_rc
from static import template_rc


_author_ = 'luwt'
_date_ = '2020/8/17 10:27'


template_names = ['java_tp', 'mapper_tp', 'xml_tp', 'service_tp', 'service_impl_tp', 'controller_tp']
templates = [':/template/java.txt', ':/template/mapper.txt', ':/template/xml.txt',
             ':/template/service.txt', ':/template/service_impl.txt', ':/template/controller.txt']


def read_file(file_path):
    file = QFile(file_path)
    file.open(QIODevice.ReadOnly)
    content = QTextStream(file).readAll()
    file.close()
    return content


def read_qss():
    return read_file(":/style.qss")


def read_template():
    template_contents = list()
    [template_contents.append(read_file(template)) for template in templates]
    return dict(zip(template_names, template_contents))
