@echo off
REM Windows下打包，设置输出名为TakeCareYourAss，图标为favicon.ico
pyinstaller --noconfirm --clean --onefile --windowed --icon=favicon.ico --add-data "favicon.ico;." -n TakeCareYourAss main.py

REM 清理PyInstaller生成的临时文件和目录
rmdir /s /q build
rmdir /s /q __pycache__
del /q main.spec

echo.
echo 打包完成，dist目录下生成 TakeCareYourAss.exe 文件。
pause
