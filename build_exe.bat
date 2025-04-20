@echo off
REM PyInstallerでimage_resizer_gui.pyをexe化するバッチファイル
REM 必要に応じてpip install pyinstaller してください

pyinstaller --noconfirm --onefile --windowed image_resizer_gui.py

pause
