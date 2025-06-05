from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QColorDialog,
    QMessageBox, QFrame, QCheckBox, QApplication, QToolTip
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPalette, QIntValidator, QIcon, QFont
import os

class HelpLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tooltip_text = ""
        self.tooltip_shown = False

    def setToolTipText(self, text):
        self.tooltip_text = text

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            QToolTip.showText(self.mapToGlobal(self.rect().bottomRight()), self.tooltip_text)
            self.tooltip_shown = True

    def leaveEvent(self, event):
        if self.tooltip_shown:
            QToolTip.hideText()
            self.tooltip_shown = False
        super().leaveEvent(event)

class SettingsWindow(QWidget):
    settings_saved = Signal(dict)

    def __init__(self, config, timer_window):
        super().__init__()
        self.config = config
        self.timer_window = timer_window
        # 设置窗口图标
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'favicon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('设置')
        self.setFixedSize(400, 500)
        # 只显示关闭按钮，禁用最小化和最大化
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.WindowCloseButtonHint
        )
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        # 主背景色
        self.setStyleSheet("")  # 先清空，后面统一设置
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(0)

        # 白色圆角设置区域
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(32, 32, 32, 32)
        frame_layout.setSpacing(18)

        label_style = """
            QLabel {
                color: #222;
                font-size: 15px;
                font-weight: 500;
            }
        """
        input_style = """
            QLineEdit {
                padding: 7px 10px;
                border: 1.5px solid #d0d0d0;
                border-radius: 5px;
                background: #fafbfc;
                font-size: 15px;
                color: #222;
                selection-background-color: #cce4ff;
            }
            QLineEdit:focus {
                border: 1.5px solid #4a90e2;
                background: #fff;
            }
        """
        color_btn_style = """
            QPushButton[colorBtn="true"] {
                border: 1.5px solid #d0d0d0;
                border-radius: 8px;
                background: #fafbfc;
                min-width: 50px;
                min-height: 25px;
            }
            QPushButton[colorBtn="true"]:hover {
                border: 1.5px solid #4a90e2;
                background: #f0f7ff;
            }
        """
        button_style = """
            QPushButton {
                padding: 6px 0px;
                min-height: 28px;
                margin-top: 8px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d6da3;
            }
        """
        cancel_btn_style = """
            QPushButton {
                padding: 6px 0px;
                min-height: 28px;
                margin-top: 8px;
                background-color: #e0e0e0;
                color: #333333;
                border: none;
                border-radius: 6px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """
        checkbox_style = """
            QCheckBox {
                color: #222;
                font-size: 15px;
                font-weight: 500;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 1.5px solid #d0d0d0;
                border-radius: 4px;
                background: #fafbfc;
            }
            QCheckBox::indicator:checked {
                background: #4a90e2;
                border: 1.5px solid #4a90e2;
            }
            QCheckBox::indicator:hover {
                border: 1.5px solid #4a90e2;
            }
        """

        # 工作时间设置
        work_layout = QHBoxLayout()
        work_label = QLabel("工作时间（分钟）:")
        work_label.setStyleSheet(label_style)
        self.work_duration_input = QLineEdit()
        self.work_duration_input.setValidator(QIntValidator(1, 999999))
        self.work_duration_input.setStyleSheet(input_style)
        work_layout.addWidget(work_label)
        work_layout.addWidget(self.work_duration_input)
        frame_layout.addLayout(work_layout)

        # 休息时间设置
        break_layout = QHBoxLayout()
        break_label = QLabel("休息时间（分钟）:")
        break_label.setStyleSheet(label_style)
        self.break_duration_input = QLineEdit()
        self.break_duration_input.setValidator(QIntValidator(1, 999999))
        self.break_duration_input.setStyleSheet(input_style)
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_duration_input)
        frame_layout.addLayout(break_layout)

        # 计时框宽度设置
        width_layout = QHBoxLayout()
        width_label = QLabel("计时框宽度（像素）:")
        width_label.setStyleSheet(label_style)
        self.timer_width_input = QLineEdit()
        self.timer_width_input.setValidator(QIntValidator(100, 500))
        self.timer_width_input.setStyleSheet(input_style)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.timer_width_input)
        frame_layout.addLayout(width_layout)

        # 计时框高度设置
        height_layout = QHBoxLayout()
        height_label = QLabel("计时框高度（像素）:")
        height_label.setStyleSheet(label_style)
        self.timer_height_input = QLineEdit()
        self.timer_height_input.setValidator(QIntValidator(100, 500))
        self.timer_height_input.setStyleSheet(input_style)
        height_layout.addWidget(height_label)
        height_layout.addWidget(self.timer_height_input)
        frame_layout.addLayout(height_layout)

        # 文字大小设置
        font_layout = QHBoxLayout()
        font_label = QLabel("文字大小（像素）:")
        font_label.setStyleSheet(label_style)
        self.font_size_input = QLineEdit()
        self.font_size_input.setValidator(QIntValidator(12, 72))
        self.font_size_input.setStyleSheet(input_style)
        font_layout.addWidget(font_label)
        font_layout.addWidget(self.font_size_input)
        frame_layout.addLayout(font_layout)

        # 遮罩颜色设置
        color_layout = QHBoxLayout()
        color_label = QLabel("屏幕遮罩层颜色:")
        color_label.setStyleSheet(label_style)
        self.color_button = QPushButton()
        self.color_button.setFixedSize(100, 25)
        self.color_button.setProperty("colorBtn", True)
        self.color_button.setStyleSheet(color_btn_style)
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        frame_layout.addLayout(color_layout)

        # 隐藏计时框设置
        hide_timer_layout = QHBoxLayout()
        hide_timer_label = QLabel("隐藏计时框（立即生效）:")
        hide_timer_label.setStyleSheet(label_style)
        
        # 创建问号图标标签
        help_label = HelpLabel("?")
        help_label.setFixedSize(16, 16)  # 固定大小
        help_label.setAlignment(Qt.AlignCenter)  # 文字居中
        help_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #4a90e2;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
                padding: 0;
                margin: 0 4px;
                min-width: 16px;
                max-width: 16px;
                min-height: 16px;
                max-height: 16px;
            }
            QLabel:hover {
                background-color: #357abd;
            }
        """)
        help_label.setToolTipText("倒计时一分钟时显示")
        help_label.setCursor(Qt.PointingHandCursor)  # 鼠标悬停时显示手型光标
        
        # 设置提示文本样式
        QApplication.instance().setStyleSheet("""
            QToolTip {
                color: white;
                background-color: #333333;
                border: none;
                padding: 4px;
                border-radius: 4px;
            }
        """)
        
        self.hide_timer_checkbox = QCheckBox()
        self.hide_timer_checkbox.setStyleSheet(checkbox_style)
        hide_timer_layout.addWidget(hide_timer_label)
        hide_timer_layout.addWidget(help_label)
        hide_timer_layout.addWidget(self.hide_timer_checkbox)
        hide_timer_layout.addStretch()  # 添加弹性空间，使复选框靠左对齐
        frame_layout.addLayout(hide_timer_layout)

        # 保存按钮
        save_button = QPushButton("保存")
        save_button.setStyleSheet(button_style)
        save_button.clicked.connect(self.save_settings)
        frame_layout.addWidget(save_button)

        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet(cancel_btn_style)
        cancel_button.clicked.connect(self.close)
        frame_layout.addWidget(cancel_button)

        main_layout.addWidget(frame)
        main_layout.addStretch(1)

        # 软件信息
        info_label = QLabel("Take Care Your Ass v1.1.0  by S0cke3t")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #888; font-size: 12px; margin-top: 18px;")
        main_layout.addWidget(info_label)

        # 调整窗口高度以适应所有控件
        self.setFixedSize(400, 550)  # 增加窗口高度

    def update_color_button(self):
        """更新颜色按钮的显示"""
        color = QColor(
            int(self.config['overlay_color'][0]),
            int(self.config['overlay_color'][1]),
            int(self.config['overlay_color'][2]),
            int(self.config['overlay_color'][3])
        )
        self.color_button.setStyleSheet(f"background-color: rgba({color.red()}, {color.green()}, {color.blue()}, 0.5);")

    def choose_color(self):
        """选择颜色"""
        current_color = QColor(
            int(self.config['overlay_color'][0]),
            int(self.config['overlay_color'][1]),
            int(self.config['overlay_color'][2]),
            int(self.config['overlay_color'][3])
        )
        color = QColorDialog.getColor(current_color, self, "选择颜色")
        if color.isValid():
            self.config['overlay_color'] = [
                int(color.red()),
                int(color.green()),
                int(color.blue()),
                128
            ]
            self.update_color_button()

    def load_settings(self):
        self.work_duration_input.setText(str(self.config.get('work_duration', 60)))
        self.break_duration_input.setText(str(self.config.get('break_duration', 5)))
        self.timer_width_input.setText(str(self.config.get('timer_width', 200)))
        self.timer_height_input.setText(str(self.config.get('timer_height', 200)))
        self.font_size_input.setText(str(self.config.get('timer_font_size', 24)))
        self.hide_timer_checkbox.setChecked(self.config.get('hide_timer', False))
        self.update_color_button()

    def save_settings(self):
        """保存设置"""
        try:
            # 获取输入值
            work_duration = int(self.work_duration_input.text())
            break_duration = int(self.break_duration_input.text())
            timer_width = int(self.timer_width_input.text())
            timer_height = int(self.timer_height_input.text())
            font_size = int(self.font_size_input.text())
            hide_timer = self.hide_timer_checkbox.isChecked()
            
            # 验证输入值
            if work_duration < 1:
                QMessageBox.warning(self, "输入错误", "工作时间必须大于1分钟")
                return
            if break_duration < 1:
                QMessageBox.warning(self, "输入错误", "休息时间必须大于1分钟")
                return
            if not (12 <= font_size <= 72):
                QMessageBox.warning(self, "输入错误", "文字大小必须在12-72像素之间")
                return
            
            # 获取计时器窗口的位置
            timer_position = {
                'x': self.timer_window.pos().x(),
                'y': self.timer_window.pos().y()
            }
            
            # 更新配置
            self.config.update({
                'work_duration': work_duration,
                'break_duration': break_duration,
                'timer_width': timer_width,
                'timer_height': timer_height,
                'timer_font_size': font_size,
                'overlay_color': self.config['overlay_color'],  # 使用已保存的颜色值
                'timer_position': timer_position,  # 保存计时器位置
                'hide_timer': hide_timer  # 保存隐藏计时框设置
            })
            
            # 保存配置
            self.settings_saved.emit(self.config)
            
            # 显示成功消息
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("保存成功")
            msg.setText("设置已保存")
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setStyleSheet("""
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
            msg.exec()
            
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置时出错：{str(e)}")

    def closeEvent(self, event):
        """关闭窗口事件"""
        # 隐藏窗口而不是关闭
        self.hide()
        event.ignore() 