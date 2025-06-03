#!/bin/bash
# Linux下打包，设置输出名为TakeCareYourAss，图标为favicon.ico（仅部分桌面环境支持ico，推荐用png）
pyinstaller --noconfirm --clean --onefile --windowed --icon=favicon.ico --add-data "favicon.ico:." -n TakeCareYourAss main.py

# 清理PyInstaller生成的临时文件和目录
rm -rf build
rm -rf __pycache__
rm -f main.spec

echo
echo "打包完成，dist目录下生成 TakeCareYourAss 可执行文件。"
