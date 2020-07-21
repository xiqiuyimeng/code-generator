# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

py_files = [
    'main.py',
]


a = Analysis(py_files,
             pathex=['D:\\python_workspaces\\python_tools\\mysql_generator'],
             binaries=[],
             datas=[
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\static\\bg_jpg\\*.jpg', './static/bg_jpg'),
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\static\\icon\\*.jpg', './static/icon'),
             ('D:\\python_workspaces\\python_tools\\mysql_generator\\static\\template\\*.txt', './static/template')],
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
