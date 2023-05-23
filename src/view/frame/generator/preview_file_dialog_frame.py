# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QSplitter, QFrame, QHBoxLayout, QVBoxLayout

from src.constant.generator_dialog_constant import SAVE_FILE_BTN_TEXT, PREVIEW_TREE_LOCATE_BTN_TEXT, \
    PREVIEW_RENAME_FILE_NAME_BTN_TEXT, NO_SELECTED_FILE_ITEM_PROMPT, PREVIEW_RENAME_FILE_NAME_TITLE
from src.view.box.message_box import pop_fail
from src.view.dialog.generator.save_file_dialog import SaveFileDialog
from src.view.dialog.simple_name_check_dialog import SimpleNameCheckDialog
from src.view.frame.dialog_frame_abc import DialogFrameABC
from src.view.tab.tab_widget.preview_generate_file_tab_widget import PreviewGenerateFileTabWidget
from src.view.tree.tree_widget.preview_generate_file_tree_widget import PreviewGenerateFileTreeWidget

_author_ = 'luwt'
_date_ = '2023/5/5 11:15'


class PreviewFileDialogFrame(DialogFrameABC):
    """预览生成，预览文件对话框框架"""

    def __init__(self, preview_data_dict, *args):
        # 存放的预览文件数据
        self.preview_data_dict: dict = preview_data_dict
        # 水平分割器
        self.horizontal_splitter: QSplitter = ...
        self.tree_frame: QFrame = ...
        self.tree_frame_layout: QVBoxLayout = ...
        self.tree_header_layout: QHBoxLayout = ...
        self.locate_button: QPushButton = ...
        self.rename_file_name_button: QPushButton = ...
        self.tree_widget: PreviewGenerateFileTreeWidget = ...
        self.tab_frame: QFrame = ...
        self.tab_frame_layout: QVBoxLayout = ...
        self.tab_widget: PreviewGenerateFileTabWidget = ...
        self.rename_file_name_dialog: SimpleNameCheckDialog = ...
        # 保存到文件按钮
        self.save_file_button: QPushButton = ...
        self.save_file_dialog: SaveFileDialog = ...
        super().__init__(*args, need_help_button=False)

    # ------------------------------ 创建ui界面 start ------------------------------ #
    def setup_content_ui(self):
        # 竖直方向的分割器
        self.horizontal_splitter = QSplitter(self)
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        # 设置拉伸时，不覆盖子控件，也就是不会隐藏控件
        self.horizontal_splitter.setChildrenCollapsible(False)
        self.frame_layout.addWidget(self.horizontal_splitter)
        # 将中间界面放大
        self.frame_layout.setStretch(1, 20)

        # 树结构
        self.tree_frame = QFrame(self)
        self.horizontal_splitter.addWidget(self.tree_frame)
        self.tree_frame_layout = QVBoxLayout(self.tree_frame)
        self.tree_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.setup_tree_header_layout()
        self.tree_widget = PreviewGenerateFileTreeWidget(self)
        self.tree_frame_layout.addWidget(self.tree_widget)

        # tab页
        self.tab_frame = QFrame(self)
        self.horizontal_splitter.addWidget(self.tab_frame)
        self.tab_frame_layout = QVBoxLayout(self.tab_frame)
        self.tab_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.tab_widget = PreviewGenerateFileTabWidget(self)
        self.tab_frame_layout.addWidget(self.tab_widget)

        self.horizontal_splitter.setStretchFactor(0, 1)
        self.horizontal_splitter.setStretchFactor(1, 3)

        # 填充树和tab页
        self.fill_tree_tab()
        # 将树节点都展开
        self.tree_widget.expandAll()

    def setup_tree_header_layout(self):
        self.tree_header_layout = QHBoxLayout(self.tree_frame)
        self.tree_header_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_frame_layout.addLayout(self.tree_header_layout)
        # 定位按钮
        self.locate_button = QPushButton(self.tree_frame)
        self.tree_header_layout.addWidget(self.locate_button)
        # 重命名文件按钮
        self.rename_file_name_button = QPushButton(self.tree_frame)
        self.tree_header_layout.addWidget(self.rename_file_name_button)

    def fill_tree_tab(self):
        for file_name, value in self.preview_data_dict.items():
            file_content, file_path = value
            # 创建树节点
            file_tree_item = self.tree_widget.make_tree_item(file_name, file_path)
            # 创建tab页
            file_tab_widget = self.tab_widget.make_tab(file_name, file_content)
            # preview_data_dict 添加页面属性
            self.preview_data_dict[file_name] = file_content, file_path, file_tree_item, file_tab_widget

    def get_blank_left_buttons(self) -> tuple:
        self.save_file_button = QPushButton(self)
        return self.save_file_button,

    def setup_other_label_text(self):
        self.locate_button.setText(PREVIEW_TREE_LOCATE_BTN_TEXT)
        self.rename_file_name_button.setText(PREVIEW_RENAME_FILE_NAME_BTN_TEXT)
        self.save_file_button.setText(SAVE_FILE_BTN_TEXT)

    # ------------------------------ 创建ui界面 end ------------------------------ #

    # ------------------------------ 信号槽处理 start ------------------------------ #

    def connect_other_signal(self):
        # 连接树双击事件，触发当前tab页切换
        self.tree_widget.doubleClicked.connect(self.change_current_tab)
        self.locate_button.clicked.connect(self.locate_tree_item)
        self.rename_file_name_button.clicked.connect(self.rename_file_name)
        self.save_file_button.clicked.connect(self.save_files)

    def change_current_tab(self, index):
        # 找到当前节点的文件名称，寻找对应的tab页节点，将其置为当前
        tree_item = self.tree_widget.itemFromIndex(index)
        # 只处理文件节点，也就是最底层的子节点
        if not tree_item.childCount():
            file_name = tree_item.text(0)
            file_value = self.preview_data_dict.get(file_name)
            file_tab_widget = file_value[3]
            self.tab_widget.setCurrentWidget(file_tab_widget)

    def locate_tree_item(self):
        """找到当前的tab页，获取文件名，根据文件名获取树节点，将其置为当前"""
        current_tab_index = self.tab_widget.currentIndex()
        file_name = self.tab_widget.tabText(current_tab_index)
        file_value = self.preview_data_dict.get(file_name)
        file_tree_item = file_value[2]
        self.tree_widget.set_selected_focus(file_tree_item)

    def rename_file_name(self):
        # 首先找到当前选中树节点
        current_item = self.tree_widget.currentItem()
        # 如果没有选中文件节点，则提示先选中一个节点再操作
        if not current_item or current_item.childCount():
            pop_fail(NO_SELECTED_FILE_ITEM_PROMPT, PREVIEW_RENAME_FILE_NAME_TITLE, self)
        else:
            # 收集不可重复的名称元祖
            exists_file_name_tuple = tuple(current_item.parent().child(child_idx).text(0)
                                           for child_idx in range(current_item.parent().childCount()))
            # 打开修改文件名对话框
            self.rename_file_name_dialog = SimpleNameCheckDialog(exists_file_name_tuple,
                                                                 PREVIEW_RENAME_FILE_NAME_TITLE,
                                                                 current_item.text(0))
            self.rename_file_name_dialog.edit_signal.connect(lambda new_file_name:
                                                             self.modify_file_name(current_item, new_file_name))
            self.rename_file_name_dialog.exec()

    def modify_file_name(self, tree_item, file_name):
        original_file_name = tree_item.text(0)
        # 修改树节点名称
        tree_item.setText(0, file_name)
        file_value = self.preview_data_dict.pop(original_file_name)
        file_tab_widget = file_value[3]
        # 修改tab页标题文件名称
        self.tab_widget.setTabText(self.tab_widget.indexOf(file_tab_widget), file_name)
        self.preview_data_dict[file_name] = file_value

    def save_files(self):
        # 收集数据
        save_file_dict = dict()
        for file_name, file_value in self.preview_data_dict.items():
            file_path, file_tab_widget = file_value[1], file_value[3]
            # 收集输出路径和当前的文件内容
            save_file_dict[file_name] = file_path, file_tab_widget.content_editor.toPlainText()
        # 打开保存进度对话框
        self.save_file_dialog = SaveFileDialog(save_file_dict)
        self.save_file_dialog.exec()

    # ------------------------------ 信号槽处理 end ------------------------------ #
