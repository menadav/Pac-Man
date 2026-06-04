# -*- mode: python ; coding: utf-8 -*-
"""Spec de PyInstaller. Build: ``pyinstaller pacman.spec``.

Produce un ejecutable autonomo en ``dist/`` listo para subir a itch.io
(zipear la carpeta) o a un depósito de Steam.
"""

from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# Incluye todos los submodulos y datos del paquete A-Maze-ing para que
# el generador recursivo funcione dentro del bundle.
hidden_imports = collect_submodules("mazegenerator") + [
    "pygame",
    "pydantic",
]

datas = collect_data_files("mazegenerator") + [
    ("config.json", "."),
]


a = Analysis(
    ["pac_man.py"],
    pathex=["."],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="pacman",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # app grafica: sin terminal en Windows
)
