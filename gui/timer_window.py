from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QColor, QPalette
from core.timer import Timer
from .overlay_window import OverlayWindow

class TimerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 初始化配置
        self.config = {
            'timer_width': 140,
            'timer_height': 70,
            'timer_font_size': 25
        }
        
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 置顶
            Qt.Tool  # 工具窗口，不在任务栏显示
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # 创建布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # 移除边距
        layout.setSpacing(0)  # 移除间距
        
        # 创建容器widget来居中显示时间标签
        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        self.time_label = QLabel("60:00")
        self.time_label.setAlignment(Qt.AlignCenter)  # 文字居中
        self.time_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                padding: 10px;
                font-size: {self.config['timer_font_size']}px;
            }}
        """)
        container_layout.addWidget(self.time_label)
        
        # 添加暂停和加减时间按钮
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(0)
        btn_height = 28

        # - 按钮
        self.minus_button = QPushButton("-")
        self.minus_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.minus_button.setFixedHeight(btn_height)
        self.minus_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border: none;
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
                border-top-right-radius: 0px;
                border-bottom-right-radius: 0px;
                font-size: 18px;
                margin: 0px;
                padding: 0px;
                border-right: 1px #fff;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.9);
            }
        """)
        self.minus_button.clicked.connect(self.decrease_time)
        btn_layout.addWidget(self.minus_button)

        # 暂停按钮
        self.pause_button = QPushButton("暂停")
        self.pause_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.pause_button.setFixedHeight(btn_height)
        self.pause_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border: none;
                border-radius: 0px;
                font-size: 16px;
                margin: 0px;
                padding: 0px;
                border-right: 1px  #fff;
                border-left: 1px  #fff;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.9);
            }
        """)
        self.pause_button.clicked.connect(self.toggle_pause)
        btn_layout.addWidget(self.pause_button)

        # + 按钮
        self.plus_button = QPushButton("+")
        self.plus_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.plus_button.setFixedHeight(btn_height)
        self.plus_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border: none;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                font-size: 18px;
                margin: 0px;
                padding: 0px;
                border-left: 1px  #fff;
            }
            QPushButton:focus { outline: none; }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.8);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.9);
            }
        """)
        self.plus_button.clicked.connect(self.increase_time)
        btn_layout.addWidget(self.plus_button)

        container_layout.addLayout(btn_layout)
        
        container.setLayout(container_layout)
        layout.addWidget(container)
        self.setLayout(layout)
        
        # 设置窗口大小
        self.setFixedSize(self.config['timer_width'], self.config['timer_height'])

        # 设置初始位置（右下角）
        self.move_to_corner()

        # 初始化计时器
        self.timer = Timer()
        self.timer.time_updated.connect(self.update_display)
        self.timer.timer_finished.connect(self.on_timer_finished)

        # 用于拖动窗口
        self.dragging = False
        self.drag_position = QPoint()
        
        # 暂停状态
        self.is_paused = False

    def move_to_corner(self):
        """将窗口移动到屏幕右下角"""
        screen = self.screen()
        if screen:
            screen_geometry = screen.geometry()
            # 确保窗口完全显示在屏幕内
            x = screen_geometry.width() - self.width() - 20
            y = screen_geometry.height() - self.height() - 40
            # 确保坐标不为负
            x = max(0, x)
            y = max(0, y)
            self.move(x, y)

    def showEvent(self, event):
        """显示窗口事件"""
        super().showEvent(event)
        # 只有在没有保存位置时才移动到角落
        if not (self.config and 'timer_position' in self.config and 
                self.config['timer_position']['x'] != 0 and 
                self.config['timer_position']['y'] != 0):
            self.move_to_corner()

    def update_display(self, seconds: int):
        """更新显示的时间"""
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        self.time_label.setText(f"{minutes:02d}:{remaining_seconds:02d}")
        
        # 如果启用了隐藏计时框功能
        if self.config.get('hide_timer', False):
            # 当剩余时间大于1分钟时隐藏窗口
            if seconds > 60:
                self.hide()
            # 当剩余时间小于等于1分钟时显示窗口
            else:
                self.show()

    def on_timer_finished(self):
        """计时结束时的处理"""
        self.hide()
        if self.config:
            # 显示休息提醒
            self.overlay = OverlayWindow(
                self.config['overlay_color'],
                self.config['break_duration']
            )
            # 连接遮罩层关闭信号
            self.overlay.overlay_closed.connect(self.start_timer)
            self.overlay.show()

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if self.dragging and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.dragging = False
            event.accept()

    def start_timer(self, minutes: int = None):
        """开始计时"""
        if minutes is None and self.config:
            minutes = self.config['work_duration']
        self.show()
        self.timer.start(minutes)

    def stop_timer(self):
        """停止计时"""
        self.timer.stop()
        self.hide()

    def set_config(self, config):
        """设置配置"""
        self.config = config
        # 更新窗口大小
        self.setFixedSize(self.config['timer_width'], self.config['timer_height'])
        # 更新字体大小
        self.time_label.setStyleSheet(f"""
            QLabel {{
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                padding: 10px;
                font-size: {self.config['timer_font_size']}px;
            }}
        """)
        # 应用保存的位置
        if 'timer_position' in self.config:
            self.move(self.config['timer_position']['x'], self.config['timer_position']['y'])
        
        # 如果启用了隐藏计时框功能，且剩余时间大于1分钟，则隐藏窗口
        if self.config.get('hide_timer', False):
            minutes, seconds = self.timer.get_remaining_time()
            if minutes > 0 or seconds > 60:
                self.hide()

    def closeEvent(self, event):
        """关闭窗口事件"""
        # 保存位置到配置
        if hasattr(self, 'config'):
            self.config['timer_position'] = {
                'x': self.pos().x(),
                'y': self.pos().y()
            }
        event.accept()

    def toggle_pause(self):
        """切换暂停/继续状态"""
        if self.is_paused:
            self.timer.resume()
            self.pause_button.setText("暂停")
            self.is_paused = False
        else:
            self.timer.pause()
            self.pause_button.setText("继续")
            self.is_paused = True

    def decrease_time(self):
        """减少10分钟"""
        if self.timer.remaining_seconds > 0:
            self.timer.remaining_seconds = max(0, self.timer.remaining_seconds - 600)
            self.update_display(self.timer.remaining_seconds)

    def increase_time(self):
        """增加10分钟"""
        self.timer.remaining_seconds += 600
        self.update_display(self.timer.remaining_seconds) 