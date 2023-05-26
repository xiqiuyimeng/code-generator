# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton, QFileDialog, QComboBox, QGridLayout

from src.constant.template_dialog_constant import CONFIG_DESC_TEXT, CONFIG_INPUT_WIDGET_TYPE_DICT, \
    OPEN_FILE_DIALOG_BUTTON_TXT, SELECT_DIRECTORY_TITLE
from src.service.system_storage.template_config_sqlite import TemplateConfig
from src.view.custom_widget.text_editor import TextEditor

_author_ = 'luwt'
_date_ = '2023/4/7 9:14'


def get_config_value_widget(template_config: TemplateConfig):
    config_widget_class = CONFIG_INPUT_WIDGET_TYPE_DICT.get(template_config.config_value_widget)
    return globals()[config_widget_class](template_config)


class ConfigValueWidgetABC(QWidget):
    """配置项输入控件抽象类"""

    def __init__(self, config: TemplateConfig):
        super().__init__()
        # 配置项数据
        self.config = config
        # 主布局
        self._layout: QGridLayout = ...
        # 必填
        self.required_label: QLabel = ...
        self.required_label_palette: QPalette = ...
        # 配置项名称label
        self.config_name_label: QLabel = ...
        # 配置项控件布局
        self.config_layout: QHBoxLayout = ...
        # 配置项说明label
        self.config_desc_label: QLabel = ...
        # 配置项说明值label
        self.config_desc_value_label: QLabel = ...

        self.setup_ui()
        self.set_text()
        self.connect_signal()

    def setup_ui(self):
        self._layout = QGridLayout(self)
        self.required_label = QLabel()
        self.required_label.setAlignment(Qt.AlignTop)
        self._layout.addWidget(self.required_label, 0, 0, 1, 1)
        self.config_name_label = QLabel()
        self.config_name_label.setAlignment(Qt.AlignTop)
        self._layout.addWidget(self.config_name_label, 0, 1, 1, 1)
        self.config_layout = QHBoxLayout()
        self.setup_config_widget_ui()
        self._layout.addLayout(self.config_layout, 0, 2, 1, 1)
        self.config_desc_label = QLabel()
        self.config_desc_label.setAlignment(Qt.AlignTop)
        self._layout.addWidget(self.config_desc_label, 1, 1, 1, 1)
        self.config_desc_value_label = QLabel()
        self._layout.addWidget(self.config_desc_value_label, 1, 2, 1, 1)
        self._layout.setColumnStretch(0, 1)
        self._layout.setColumnStretch(1, 10)
        self._layout.setColumnStretch(2, 70)

    def setup_config_widget_ui(self):
        ...

    def set_text(self):
        if self.config.is_required:
            # 必填项文本为 *，红色文本
            if self.required_label_palette is Ellipsis:
                self.required_label_palette = QPalette()
                self.required_label_palette.setColor(QPalette.WindowText, Qt.red)
            self.required_label.setText('*')
            self.required_label.setPalette(self.required_label_palette)
        # 配置项名称
        self.config_name_label.setText(self.config.config_name)
        # 配置项说明label文本
        self.config_desc_label.setText(CONFIG_DESC_TEXT)
        # 配置项说明
        self.config_desc_value_label.setText(self.config.config_desc)
        self.set_other_text()

    def set_other_text(self):
        ...

    def connect_signal(self):
        ...

    def collect_data(self):
        ...


class LineEditConfigValueWidget(ConfigValueWidgetABC):
    """文本输入框控件"""

    def __init__(self, *args):
        self.line_edit: QLineEdit = ...
        super().__init__(*args)

    def setup_config_widget_ui(self):
        self.line_edit = QLineEdit()
        self.config_layout.addWidget(self.line_edit)

    def set_other_text(self):
        # 占位文本
        self.line_edit.setPlaceholderText(self.config.placeholder_text)
        # 默认值
        self.line_edit.setText(self.config.default_value)

    def collect_data(self):
        return self.line_edit.text()


class FileDialogConfigValueWidgetABC(ConfigValueWidgetABC):
    """文件夹对话框控件抽象类"""

    def __init__(self, *args):
        self.open_file_dialog_button: QPushButton = ...
        super().__init__(*args)

    def setup_config_widget_ui(self):
        self.open_file_dialog_button = QPushButton()
        self.config_layout.addWidget(self.open_file_dialog_button)

    def set_other_text(self):
        self.open_file_dialog_button.setText(OPEN_FILE_DIALOG_BUTTON_TXT)

    def connect_signal(self):
        self.open_file_dialog_button.clicked.connect(self.open_dir_dialog)

    def open_dir_dialog(self):
        exists_dir = QFileDialog.getExistingDirectory(self, SELECT_DIRECTORY_TITLE, '', QFileDialog.ShowDirsOnly)
        if exists_dir:
            self.set_dir(exists_dir)

    def set_dir(self, exists_dir):
        ...


class FileDialogConfigValueWidget(FileDialogConfigValueWidgetABC):
    """文件夹对话框控件"""

    def __init__(self, *args):
        self.dir_label: QLabel = ...
        super().__init__(*args)

    def setup_config_widget_ui(self):
        self.dir_label = QLabel()
        self.config_layout.addWidget(self.dir_label)
        super().setup_config_widget_ui()

    def set_dir(self, exists_dir):
        self.dir_label.setText(exists_dir)

    def collect_data(self):
        return self.dir_label.text()


class LineEditFileDialogConfigValueWidget(LineEditConfigValueWidget, FileDialogConfigValueWidgetABC):
    """文本输入框 + 文件夹对话框 控件"""

    def __init__(self, *args):
        super().__init__(*args)
        FileDialogConfigValueWidgetABC.__init__(self, *args)

    def setup_config_widget_ui(self):
        super().setup_config_widget_ui()
        FileDialogConfigValueWidgetABC.setup_config_widget_ui(self)

    def set_other_text(self):
        super().set_other_text()
        FileDialogConfigValueWidgetABC.set_other_text(self)

    def set_dir(self, exists_dir):
        self.line_edit.setText(exists_dir)


class TextEditorConfigValueWidget(ConfigValueWidgetABC):
    """文本编辑区控件"""

    def __init__(self, *args):
        self.text_editor: TextEditor = ...
        super().__init__(*args)

    def setup_config_widget_ui(self):
        self.text_editor = TextEditor()
        self.config_layout.addWidget(self.text_editor)

    def set_other_text(self):
        self.text_editor.setPlainText(self.config.default_value)

    def collect_data(self):
        return self.text_editor.toPlainText()


class ComboBoxConfigValueWidget(ConfigValueWidgetABC):
    """下拉框列表控件"""

    def __init__(self, *args):
        self.combo_box: QComboBox = ...
        super().__init__(*args)

    def setup_config_widget_ui(self):
        self.combo_box = QComboBox()
        self.config_layout.addWidget(self.combo_box)

    def set_other_text(self):
        self.combo_box.addItems(self.config.range_values.split(","))
        self.combo_box.setCurrentText(self.config.default_value)

    def collect_data(self):
        return self.combo_box.currentText()
