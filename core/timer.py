from PySide6.QtCore import QTimer, QObject, Signal
from typing import Callable

class Timer(QObject):
    time_updated = Signal(int)  # 发送剩余时间（秒）
    timer_finished = Signal()   # 计时结束信号

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_time)
        self.remaining_seconds = 0
        self.is_running = False

    def start(self, minutes: int) -> None:
        """开始计时"""
        self.remaining_seconds = minutes * 60
        self.is_running = True
        self.timer.start(1000)  # 每秒更新一次

    def stop(self) -> None:
        """停止计时"""
        self.timer.stop()
        self.is_running = False

    def pause(self) -> None:
        """暂停计时"""
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def resume(self) -> None:
        """恢复计时"""
        if not self.is_running and self.remaining_seconds > 0:
            self.timer.start(1000)
            self.is_running = True

    def _update_time(self) -> None:
        """更新剩余时间"""
        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.time_updated.emit(self.remaining_seconds)
        else:
            self.stop()
            self.timer_finished.emit()

    def get_remaining_time(self) -> tuple[int, int]:
        """获取剩余时间（分钟和秒）"""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        return minutes, seconds 