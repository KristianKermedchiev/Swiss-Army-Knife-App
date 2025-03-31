# cli.spec
block_cipher = None

a = Analysis(['cli.py'],
             pathex=['C:\\Users\\kkerm\\Documents\\GitHub\\Swiss-Army-Knife-App\\src'],
             binaries=[],
             datas=[
                 ('commands', 'src/commands'),
                 ('services', 'src/services'),
                 ('utils', 'src/utils'),
                 ('db', 'src/db')
             ],
             hiddenimports=[
                 'src.commands.bills',
                 'pandas',
                 'numpy',
                 'pytz',
                 'src.commands.expenses',
                 'src.services.expenses_service',
                 'src.utils.file_utils',
                 'src.db.db_interface'
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
          name='cli_app',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)