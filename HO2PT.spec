# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['HO2PT.py'],
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
    name='HO2PT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Img/ho2pt.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='HO2PT',
)
app = BUNDLE(
    coll,
    name='HO2PT.app',
    icon='Img/ho2pt.ico',
    bundle_identifier='HO2PT',
)
