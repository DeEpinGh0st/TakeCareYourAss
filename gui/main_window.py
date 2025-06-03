from PySide6.QtWidgets import QMainWindow, QSystemTrayIcon, QMenu, QWidget, QMessageBox
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from .timer_window import TimerWindow
from .settings_window import SettingsWindow
from core.config_manager import ConfigManager
import os
from PySide6.QtWidgets import QApplication
import sys

# 资源路径兼容PyInstaller打包和源码运行
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化配置
        self.config = {
            'work_duration': 60,
            'break_duration': 5,
            'timer_width': 160,
            'timer_height': 80,
            'timer_font_size': 24,
            'overlay_color': [0, 0, 0, 128],  # 修改为RGBA数组格式
            'timer_position': {'x': 0, 'y': 0}
        }
        
        # 加载配置
        self.config_manager = ConfigManager()
        saved_config = self.config_manager.load_config()
        if saved_config:
            self.config.update(saved_config)
        
        self.init_ui()
        
        # 启动计时器
        self.start_timer()

    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle('久坐提醒')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # 创建系统托盘图标
        icon_path = resource_path('favicon.ico')
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.setToolTip("Take Care Your Ass")
        self.tray_icon.show()
        self.setWindowIcon(QIcon(icon_path))
        
        # 创建托盘菜单
        tray_menu = QMenu()
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self.close)
        
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        
        # 创建计时器窗口
        self.timer_window = TimerWindow()
        self.timer_window.set_config(self.config)
        
        # 创建设置窗口，传入timer_window
        self.settings_window = SettingsWindow(self.config, self.timer_window)
        self.settings_window.settings_saved.connect(self.on_settings_saved)
        
        # 设置窗口位置
        if self.config['timer_position']['x'] != 0 or self.config['timer_position']['y'] != 0:
            self.timer_window.move(
                self.config['timer_position']['x'],
                self.config['timer_position']['y']
            )
        else:
            # 如果位置未设置，移动到右下角
            self.timer_window.move_to_corner()
            
        # 隐藏主窗口
        self.hide()

    def start_timer(self):
        """启动计时器"""
        self.timer_window.start_timer()

    def show_settings(self):
        """显示设置窗口"""
        self.settings_window.show()

    def on_settings_saved(self, new_config):
        """设置保存时的处理"""
        self.config = new_config
        self.config_manager.save_config(self.config)
        # 只更新计时器窗口的配置，不重新开始计时
        self.timer_window.set_config(self.config)

    def closeEvent(self, event):
        """关闭窗口事件"""
        reply = QMessageBox(self)
        reply.setWindowTitle("确认")
        reply.setText("确定要退出程序吗？")
        reply.setIcon(QMessageBox.Question)
        reply.setStyleSheet("""
            QMessageBox {
                background-color: #f5f5f5;
            }
            QMessageBox QWidget {
                background-color: #f5f5f5;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background-color: #f5f5f5;
            }
            QMessageBox QPushButton {
                padding: 8px 20px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #1976D2;
            }
            QMessageBox QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        reply.setWindowFlags(reply.windowFlags() | Qt.WindowStaysOnTopHint)
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.setDefaultButton(QMessageBox.No)
        
        if reply.exec() == QMessageBox.Yes:
            # 保存计时器窗口位置
            if hasattr(self, 'timer_window'):
                self.config['timer_position'] = {
                    'x': self.timer_window.pos().x(),
                    'y': self.timer_window.pos().y()
                }
                self.config_manager.save_config(self.config)
            
            # 停止计时器
            if hasattr(self, 'timer_window'):
                self.timer_window.stop_timer()
            
            # 关闭所有窗口
            if hasattr(self, 'timer_window'):
                self.timer_window.close()
            if hasattr(self, 'settings_window'):
                self.settings_window.close()
            
            # 退出应用
            QApplication.quit()
        else:
            event.ignore() 