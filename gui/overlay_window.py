from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QKeyEvent

class OverlayWindow(QWidget):
    # 添加信号
    overlay_closed = Signal()  # 遮罩层关闭信号

    def __init__(self, color, duration):
        super().__init__()
        self.duration = duration
        self.overlay_color = QColor(color[0], color[1], color[2], color[3])
        self.init_ui()
        self.start_countdown()

    def init_ui(self):
        """初始化UI"""
        # 设置窗口标志
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 置顶
            Qt.Tool  # 工具窗口
        )
        
        # 设置窗口属性
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # 显示时不激活
        
        # 设置窗口全屏
        screen = self.screen()
        if screen:
            self.setGeometry(screen.geometry())

        # 创建布局和标签，居中
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # 设置布局居中对齐
        
        self.time_label = QLabel("休息时间")
        self.time_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 0.7);
                border-radius: 10px;
                padding: 20px;
                font-size: 36px;
            }
        """)
        self.time_label.setAlignment(Qt.AlignCenter)  # 设置标签文字居中对齐
        layout.addWidget(self.time_label)
        self.setLayout(layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.overlay_color)

    def start_countdown(self):
        """开始倒计时"""
        self.remaining_time = self.duration * 60
        self.update_display()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # 每秒更新一次

    def update_countdown(self):
        """更新倒计时"""
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.close()
        else:
            self.update_display()

    def update_display(self):
        """更新显示的时间"""
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_label.setText(f"休息时间: {minutes:02d}:{seconds:02d}\n按 ESC 键结束休息")

    def mousePressEvent(self, event):
        """鼠标按下事件，点击不关闭遮罩层"""
        event.ignore()

    def keyPressEvent(self, event: QKeyEvent):
        """键盘按下事件"""
        if event.key() == Qt.Key_Escape:
            self.timer.stop()
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """关闭窗口事件"""
        self.overlay_closed.emit()  # 发送遮罩层关闭信号
        super().closeEvent(event) 