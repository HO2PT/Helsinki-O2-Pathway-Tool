# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['O2PathwayTool.py'],
    pathex=[],
    binaries=[],
    datas=[('Img', 'Img'), ('userInstructions.pdf', '.')],
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

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='O2PathwayTool',
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
    icon='Img/ho2pt.ico',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='O2PathwayTool',
)
app = BUNDLE(
    coll,
    name='O2PathwayTool.app',
    icon='Img/ho2pt.ico',
    bundle_identifier=None,
)
