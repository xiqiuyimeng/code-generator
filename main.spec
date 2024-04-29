# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['E:\\python_workspace\\code-generator'],
    binaries=[],
    datas=[
        ('E:\\python_workspace\\code-generator\\static\\bg_jpg', 'static/bg_jpg'),
        ('E:\\python_workspace\\code-generator\\static\\boot', 'static/boot'),
        ('E:\\python_workspace\\code-generator\\static\\gif', 'static/gif'),
        ('E:\\python_workspace\\code-generator\\static\\icon', 'static/icon'),
        ('E:\\python_workspace\\code-generator\\static\\qss', 'static/qss'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
splash = Splash(
    'static/boot/boot.jpg',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=False,
)

exe = EXE(
    pyz,
    a.scripts,
    splash,
    [],
    exclude_binaries=True,
    name='代码生成器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/icon/exec.png',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash.binaries,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='code-generator',
)
