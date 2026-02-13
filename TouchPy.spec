# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for TouchPy - Touch Typing Trainer
This file configures how the application is built into an executable.
"""

from PyInstaller.utils.hooks import collect_data_files
import os

# Collect data files (exercises)
exercises_path = os.path.join('typing_trainer', 'exercises')
datas = [(exercises_path, 'typing_trainer/exercises')]

# Collect Textual and Rich data files if needed
datas += collect_data_files('textual')
datas += collect_data_files('rich')

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'textual',
        'rich',
        'typing_trainer',
        'typing_trainer.app',
        'typing_trainer.models',
        'typing_trainer.services.loader',
        'typing_trainer.services.metrics',
        'typing_trainer.views.menu_view',
        'typing_trainer.views.typing_view',
        'typing_trainer.views.summary_view',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TouchPy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Keep console for better compatibility
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # You can add an .ico file here later
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TouchPy',
)
