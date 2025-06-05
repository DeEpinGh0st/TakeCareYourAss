@echo off
setlocal enabledelayedexpansion

echo === TakeCareYourAss Windows打包脚本 ===
echo 正在检查环境...

REM 检查Python是否安装
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 检查PyInstaller是否安装
python -c "import PyInstaller" >nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到PyInstaller，请先安装:
    echo pip install pyinstaller
    pause
    exit /b 1
)

REM 检查必要文件
if not exist main.py (
    echo 错误: 未找到main.py
    pause
    exit /b 1
)

if not exist favicon.ico (
    echo 警告: 未找到favicon.ico，将使用默认图标
)

echo 清理旧的构建文件...
if exist build rmdir /s /q build
if exist __pycache__ rmdir /s /q __pycache__
if exist main.spec del /q main.spec
if exist dist rmdir /s /q dist

echo 开始打包...

REM 构建命令
if exist favicon.ico (
    pyinstaller --noconfirm --clean --onefile --windowed ^
        --icon=favicon.ico ^
        --add-data "favicon.ico;." ^
        -n TakeCareYourAss main.py
) else (
    pyinstaller --noconfirm --clean --onefile --windowed ^
        -n TakeCareYourAss main.py
)

if %errorlevel% equ 0 (
    echo.
    echo === 打包成功！===
    echo 可执行文件位置: %cd%\dist\TakeCareYourAss.exe
) else (
    echo.
    echo 打包失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo 您可以直接运行 dist\TakeCareYourAss.exe 来启动程序
pause
