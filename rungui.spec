# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['peer_reviewer_program/rungui.py'],
             pathex=['/Users/hamid/CanvasPeerReviewManager'],
             binaries=[],
             datas=[('peer_reviewer_program/davis_cs.jpg', './peer_reviewer_program')],
             hiddenimports=['pkg_resources.py2_warn'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rungui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='rungui.app',
             icon=None,
             bundle_identifier=None)