#!/bin/bash
# Linux下打包，设置输出名为TakeCareYourAss，图标为favicon.ico（仅部分桌面环境支持ico，推荐用png）

# 检查是否安装了必要的工具
check_dependencies() {
    if ! command -v pyinstaller &> /dev/null; then
        echo "错误: 未找到 PyInstaller，请先安装:"
        echo "pip install pyinstaller"
        exit 1
    fi
}

# 检查文件是否存在
check_files() {
    if [ ! -f "main.py" ]; then
        echo "错误: 未找到 main.py"
        exit 1
    fi
    if [ ! -f "favicon.ico" ]; then
        echo "警告: 未找到 favicon.ico，将使用默认图标"
    fi
}

# 清理旧的构建文件
cleanup() {
    echo "清理旧的构建文件..."
    rm -rf build
    rm -rf __pycache__
    rm -f main.spec
    rm -rf dist
}

# 主打包函数
build() {
    echo "开始打包..."
    
    # 构建命令
    if [ -f "favicon.ico" ]; then
        pyinstaller --noconfirm --clean --onefile --windowed \
            --icon=favicon.ico \
            --add-data "favicon.ico:." \
            -n TakeCareYourAss main.py
    else
        pyinstaller --noconfirm --clean --onefile --windowed \
            -n TakeCareYourAss main.py
    fi
    
    # 检查打包是否成功
    if [ $? -eq 0 ]; then
        echo "打包成功！"
        echo "可执行文件位置: $(pwd)/dist/TakeCareYourAss"
    else
        echo "打包失败，请检查错误信息"
        exit 1
    fi
}

# 主程序
echo "=== TakeCareYourAss 打包脚本 ==="
echo "正在检查环境..."

check_dependencies
check_files
cleanup
build

echo
echo "=== 打包完成 ==="
echo "可执行文件已生成在 dist 目录下"
echo "您可以通过以下命令运行程序："
echo "./dist/TakeCareYourAss"
