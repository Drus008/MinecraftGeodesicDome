# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['aplicacion.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/Programació/MinecraftGeodesicDome/doc/pack.mcmeta', 'doc'), ('D:/Programació/MinecraftGeodesicDome/doc/load.json', 'doc'), ('D:/Programació/MinecraftGeodesicDome/doc/iniciar.mcfunction', 'doc')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='aplicacion',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
