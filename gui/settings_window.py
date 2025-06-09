from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QColorDialog,
    QMessageBox, QFrame, QCheckBox, QApplication, QToolTip,
    QSlider, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QColor, QPalette, QIntValidator, QIcon, QFont
import os
from utils.autostart import AutoStartManager
from gui.overlay_window import OverlayWindow

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
        self.autostart_manager = AutoStartManager()
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
        frame_layout.setSpacing(24)  # 增加垂直间距

        label_style = """
            QLabel {
                color: #222;
                font-size: 15px;
                font-weight: 500;
                min-height: 24px;  /* 确保标签有足够的高度 */
            }
        """
        input_style = """
            QLineEdit {
                padding: 6px 10px;  /* 减小内边距 */
                border: 1.5px solid #d0d0d0;
                border-radius: 5px;
                background: #fafbfc;
                font-size: 15px;
                color: #222;
                selection-background-color: #cce4ff;
                min-height: 20px;  /* 减小最小高度 */
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
                min-height: 32px;  /* 增加按钮高度 */
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
                min-height: 24px;  /* 确保复选框有足够的高度 */
                padding: 2px 0;  /* 添加上下内边距 */
            }
            QCheckBox::indicator {
                width: 20px;  /* 增加指示器大小 */
                height: 20px;
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
        work_layout.setSpacing(12)  # 增加水平间距
        work_label = QLabel("工作时间(分钟):")
        work_label.setStyleSheet(label_style)
        work_label.setFixedWidth(120)
        self.work_duration_input = QLineEdit()
        self.work_duration_input.setValidator(QIntValidator(1, 999999))
        self.work_duration_input.setStyleSheet(input_style)
        work_layout.addWidget(work_label)
        work_layout.addStretch()
        work_layout.addWidget(self.work_duration_input)
        frame_layout.addLayout(work_layout)

        # 休息时间设置
        break_layout = QHBoxLayout()
        break_layout.setSpacing(12)
        break_label = QLabel("休息时间(分钟):")
        break_label.setStyleSheet(label_style)
        break_label.setFixedWidth(120)
        self.break_duration_input = QLineEdit()
        self.break_duration_input.setValidator(QIntValidator(1, 999999))
        self.break_duration_input.setStyleSheet(input_style)
        break_layout.addWidget(break_label)
        break_layout.addStretch()
        break_layout.addWidget(self.break_duration_input)
        frame_layout.addLayout(break_layout)

        # 计时框宽度设置
        width_layout = QHBoxLayout()
        width_layout.setSpacing(12)  # 增加水平间距
        width_label = QLabel("计时框宽度(像素):")
        width_label.setStyleSheet(label_style)
        width_label.setFixedWidth(120)
        self.timer_width_input = QLineEdit()
        self.timer_width_input.setValidator(QIntValidator(100, 500))
        self.timer_width_input.setStyleSheet(input_style)
        width_layout.addWidget(width_label)
        width_layout.addStretch()
        width_layout.addWidget(self.timer_width_input)
        frame_layout.addLayout(width_layout)

        # 计时框高度设置
        height_layout = QHBoxLayout()
        height_layout.setSpacing(12)  # 增加水平间距
        height_label = QLabel("计时框高度(像素):")
        height_label.setStyleSheet(label_style)
        height_label.setFixedWidth(120)
        self.timer_height_input = QLineEdit()
        self.timer_height_input.setValidator(QIntValidator(100, 500))
        self.timer_height_input.setStyleSheet(input_style)
        height_layout.addWidget(height_label)
        height_layout.addStretch()
        height_layout.addWidget(self.timer_height_input)
        frame_layout.addLayout(height_layout)

        # 文字大小设置
        font_layout = QHBoxLayout()
        font_layout.setSpacing(12)  # 增加水平间距
        font_label = QLabel("文字大小(像素):")
        font_label.setStyleSheet(label_style)
        font_label.setFixedWidth(120)
        self.font_size_input = QLineEdit()
        self.font_size_input.setValidator(QIntValidator(12, 72))
        self.font_size_input.setStyleSheet(input_style)
        font_layout.addWidget(font_label)
        font_layout.addStretch()
        font_layout.addWidget(self.font_size_input)
        frame_layout.addLayout(font_layout)

        # 遮罩颜色设置
        color_layout = QHBoxLayout()
        color_layout.setSpacing(12)  # 增加水平间距
        color_label = QLabel("屏幕遮罩层颜色:")
        color_label.setStyleSheet(label_style)
        color_label.setFixedWidth(130)
        self.color_button = QPushButton()
        self.color_button.setMinimumWidth(160)
        self.color_button.setMaximumWidth(160)
        self.color_button.setFixedHeight(32)
        self.color_button.setProperty("colorBtn", True)
        self.color_button.setStyleSheet(color_btn_style)
        self.color_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.color_button.clicked.connect(self.choose_color)
        color_layout.addWidget(color_label)
        color_layout.addWidget(self.color_button)
        
        preview_btn_style = """
            QPushButton {
                min-width: 36px;
                max-width: 36px;
                min-height: 20px;
                max-height: 20px;
                background-color: #4a90e2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 500;
                padding: 0 6px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2d6da3;
            }
        """
        # 预览按钮
        preview_button = QPushButton("预览")
        preview_button.setFixedSize(44, 20)  # 适当加宽
        preview_button.setStyleSheet(preview_btn_style)
        preview_button.clicked.connect(self.preview_overlay)
        color_layout.addWidget(preview_button)
        frame_layout.addLayout(color_layout)

        # 遮罩透明度设置
        opacity_layout = QHBoxLayout()
        opacity_layout.setSpacing(12)
        opacity_label = QLabel("遮罩层透明度:")
        opacity_label.setStyleSheet(label_style)
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(50)  # 默认值
        self.opacity_slider.setMinimumWidth(160)  # 增加滑块宽度
        self.opacity_slider.setStyleSheet("""
            QSlider {
                height: 16px;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 2px;
                background: #f3f3f3;
                margin: 0px 0;
                border-radius: 2px;
            }
            QSlider::sub-page:horizontal {
                background: #90caff;
                border-radius: 2px;
            }
            QSlider::add-page:horizontal {
                background: #f3f3f3;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 2px solid #90caff;
                width: 12px;
                height: 12px;
                margin: -6px 0;
                border-radius: 6px;
            }
            QSlider::handle:horizontal:hover {
                border: 2px solid #4a90e2;
                background: #f8faff;
            }
            QSlider::handle:horizontal:pressed {
                border: 2px solid #357abd;
                background: #e6f2ff;
            }
        """)
        self.opacity_value_label = QLabel("50%")
        self.opacity_value_label.setStyleSheet("""
            QLabel {
                color: #222;
                font-size: 15px;
                font-weight: 500;
                min-width: 45px;
                text-align: right;
            }
        """)
        self.opacity_slider.valueChanged.connect(self.update_opacity_label)
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addStretch()
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addSpacing(32)
        self.opacity_value_label.setContentsMargins(8, 0, 0, 0)
        opacity_layout.addWidget(self.opacity_value_label)
        frame_layout.addLayout(opacity_layout)

        # 隐藏计时框设置
        hide_timer_layout = QHBoxLayout()
        hide_timer_layout.setSpacing(12)  # 增加水平间距
        hide_timer_label = QLabel("隐藏计时框（立即生效）:")
        hide_timer_label.setStyleSheet(label_style)
        
        # 创建问号图标标签
        help_label = HelpLabel("?")
        help_label.setFixedSize(20, 20)  # 增加图标大小
        help_label.setAlignment(Qt.AlignCenter)
        help_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #4a90e2;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                padding: 0;
                margin: 0 4px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
            }
            QLabel:hover {
                background-color: #357abd;
            }
        """)
        help_label.setToolTipText("倒计时一分钟时显示")
        help_label.setCursor(Qt.PointingHandCursor)
        
        self.hide_timer_checkbox = QCheckBox()
        self.hide_timer_checkbox.setStyleSheet(checkbox_style)
        hide_timer_layout.addWidget(hide_timer_label)
        hide_timer_layout.addWidget(help_label)
        hide_timer_layout.addStretch()
        hide_timer_layout.addWidget(self.hide_timer_checkbox)
        frame_layout.addLayout(hide_timer_layout)

        # 开机自启设置
        autostart_layout = QHBoxLayout()
        autostart_layout.setSpacing(12)  # 增加水平间距
        autostart_label = QLabel("开机自启动:")
        autostart_label.setStyleSheet(label_style)
        self.autostart_checkbox = QCheckBox()
        self.autostart_checkbox.setStyleSheet(checkbox_style)
        autostart_layout.addWidget(autostart_label)
        autostart_layout.addStretch()
        autostart_layout.addWidget(self.autostart_checkbox)
        frame_layout.addLayout(autostart_layout)

        # 保存按钮
        save_button = QPushButton("保存")
        save_button.setStyleSheet(button_style)
        save_button.setMinimumHeight(36)  # 增加按钮高度
        save_button.clicked.connect(self.save_settings)
        frame_layout.addWidget(save_button)

        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet(cancel_btn_style)
        cancel_button.setMinimumHeight(36)  # 增加按钮高度
        cancel_button.clicked.connect(self.close)
        frame_layout.addWidget(cancel_button)

        main_layout.addWidget(frame)
        main_layout.addStretch(1)

        # 软件信息
        info_label = QLabel("Take Care Your Ass v1.2.0  by S0cke3t")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #888; font-size: 12px; margin-top: 18px;")
        main_layout.addWidget(info_label)

        # 调整窗口高度以适应所有控件
        self.setFixedSize(400, 600)  # 增加窗口高度

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

    def update_opacity_label(self, value):
        """更新透明度标签显示"""
        self.opacity_value_label.setText(f"{value}%")

    def preview_overlay(self):
        """预览当前遮罩层设置，显示3秒"""
        # 获取当前颜色和透明度
        color = [
            int(self.config['overlay_color'][0]),
            int(self.config['overlay_color'][1]),
            int(self.config['overlay_color'][2]),
            255  # alpha 先设为不透明，实际用opacity
        ]
        opacity = self.opacity_slider.value()
        # 创建遮罩层窗口，持续3秒
        self._preview_overlay = OverlayWindow(color, 0, opacity)  # duration=0, 不显示倒计时
        self._preview_overlay.display_text = "遮罩效果预览"
        self._preview_overlay.shortcut_text = ""
        self._preview_overlay.show()
        QTimer.singleShot(3000, self._preview_overlay.close)

    def load_settings(self):
        self.work_duration_input.setText(str(self.config.get('work_duration', 60)))
        self.break_duration_input.setText(str(self.config.get('break_duration', 5)))
        self.timer_width_input.setText(str(self.config.get('timer_width', 200)))
        self.timer_height_input.setText(str(self.config.get('timer_height', 200)))
        self.font_size_input.setText(str(self.config.get('timer_font_size', 24)))
        self.hide_timer_checkbox.setChecked(self.config.get('hide_timer', False))
        self.autostart_checkbox.setChecked(self.config.get('autostart', False))
        self.opacity_slider.setValue(self.config.get('overlay_opacity', 50))
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
            autostart = self.autostart_checkbox.isChecked()
            overlay_opacity = self.opacity_slider.value()
            
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
            
            # 设置开机自启
            if autostart != self.autostart_manager.is_autostart_enabled():
                if not self.autostart_manager.set_autostart(autostart):
                    QMessageBox.warning(self, "设置失败", "设置开机自启失败，请检查程序权限")
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
                'overlay_opacity': overlay_opacity,  # 保存遮罩层透明度
                'timer_position': timer_position,  # 保存计时器位置
                'hide_timer': hide_timer,  # 保存隐藏计时框设置
                'autostart': autostart  # 保存开机自启设置
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