from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QKeyEvent, QFont

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
        
        # 获取所有屏幕
        screens = QApplication.screens()
        if screens:
            # 计算所有屏幕的总区域
            total_geometry = screens[0].geometry()
            for screen in screens[1:]:
                total_geometry = total_geometry.united(screen.geometry())
            # 设置窗口大小为所有屏幕的总区域
            self.setGeometry(total_geometry)
        # 记录1号屏幕的geometry
        self.first_screen_geometry = screens[0].geometry() if screens else None
        self.display_text = "休息时间"
        self.remaining_time = self.duration * 60

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), self.overlay_color)
        if self.first_screen_geometry:
            # 在1号屏幕中央绘制文字
            font = QFont()
            font.setPointSize(36)
            painter.setFont(font)
            painter.setPen(Qt.white)
            # 文字内容
            text = self.display_text
            # 计算文字大小
            metrics = painter.fontMetrics()
            text_width = metrics.horizontalAdvance(text)
            text_height = metrics.height()
            # 计算1号屏幕中心
            center_x = self.first_screen_geometry.x() + self.first_screen_geometry.width() // 2
            center_y = self.first_screen_geometry.y() + self.first_screen_geometry.height() // 2
            # 让文字居中
            painter.setBrush(QColor(0,0,0,180))
            rect_x = center_x - text_width // 2 - 30
            rect_y = center_y - text_height // 2 - 20
            rect_w = text_width + 60
            rect_h = text_height + 40
            painter.setRenderHint(QPainter.Antialiasing)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 16, 16)
            painter.setPen(Qt.white)
            painter.drawText(center_x - text_width // 2, center_y + text_height // 4, text)

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
        self.display_text = f"休息时间: {minutes:02d}:{seconds:02d},按 ESC 键结束休息"
        self.update()

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