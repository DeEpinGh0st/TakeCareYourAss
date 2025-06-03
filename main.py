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
    
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 