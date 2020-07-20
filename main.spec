# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = [
    'main.py',
    './table/table_header.py',
    './sys_info_storage/sqlite.py',
    './settings/font.py',
    './main_window/generator_gui.py',
    './little_widget/menu.py',
    './little_widget/menu_bar_func.py',
    './little_widget/message_box.py',
    './little_widget/tool_bar.py',
    './generator/mybatis_generator.py',
    './generator/spring_generator.py',
    './func/connection_function.py',
    './func/do_generate.py',
    './func/gui_function.py',
    './func/selected_data.py',
    './func/table_func.py',
    './func/tree_function.py',
    './func/tree_strategy.py',
    './dialog/confirm_select_dialog.py',
    './dialog/conn_dialog.py',
    './dialog/generate_result_dialog.py',
    './dialog/select_generator_ui.py',
    './db/cursor_proxy.py',
    './db/get_cursor.py',
    './constant/constant.py',
    './constant/mysql_type.py'
]


a = Analysis(py_files,
             pathex=['D:\\python_workspaces\\python_tools\\mysql_generator'],
             binaries=[],
             datas=[
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\bg_jpg\\*.jpg', './bg_jpg'),
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\icon\\*.jpg', './icon'),
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\template\\*.txt', './template')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='generator')
