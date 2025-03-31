# gui.spec
block_cipher = None

a = Analysis(['GUI_window.py'],
             pathex=['C:\\Users\\kkerm\\Documents\\GitHub\\Swiss-Army-Knife-App\\src'],
             binaries=[],
             datas=[
                 ('gui_tabs', 'src/gui_tabs'),
                 ('utils', 'src/utils'),
                 ('db', 'src/db'),
                 # Add other folders that GUI might need access to
                 ('services', 'src/services'),
                 ('commands', 'src/commands')
             ],
             hiddenimports=[
                 'pandas',
                 'numpy',
                 'pytz',
                 'src.gui_tabs.base_tab',
                 'src.utils.file_utils',
                 'src.db.db_interface',
                 'src.services.expenses_service',
                 'src.commands.expenses',
                 # Add any GUI-specific libraries
                 'tkinter',
                 'matplotlib',
                 'PIL',
                 'sys',
                 'os'
             ],
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
          name='gui_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)  # False for GUI apps