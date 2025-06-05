import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import os

def main():
    # 隐藏控制台窗口
    if os.name == 'nt':  # Windows系统
        import ctypes
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )
    # 注意：在Linux系统上，建议在打包时使用以下命令来创建无控制台窗口的应用程序：
    # pyinstaller --noconsole main.py
    # 或
    # pyinstaller -w main.py
    
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 