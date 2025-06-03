import os
import yaml
from typing import Dict, Any
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.yaml'
        # 动态获取屏幕右下角坐标
        app = QApplication.instance() or QApplication([])
        screen = app.primaryScreen()
        screen_geometry = screen.geometry()
        timer_width = 140
        timer_height = 70
        margin_x = 20
        margin_y = 40
        right_x = max(0, screen_geometry.width() - timer_width - margin_x)
        right_y = max(0, screen_geometry.height() - timer_height - margin_y)
        self.default_config = {
            'work_duration': 60,  # 工作时间（分钟）
            'break_duration': 10,  # 休息时间（分钟）
            'overlay_color': [144, 238, 144, 128],  # 淡黄绿色 [R, G, B, A]
            'timer_position': {'x': right_x, 'y': right_y},  # 计时器右下角
            'timer_width': timer_width,  # 计时器宽度
            'timer_height': timer_height,  # 计时器高度
            'timer_font_size': 25  # 计时器字体大小
        }
        self.config = self.load_config()

    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    if config is None:
                        print("配置文件为空，使用默认配置")
                        self.save_config(self.default_config)
                        return self.default_config.copy()
                    # 确保所有必要的配置项都存在
                    for key, value in self.default_config.items():
                        if key not in config:
                            print(f"配置项 {key} 不存在，使用默认值")
                            config[key] = value
                    # 确保颜色值是 RGBA 数组格式
                    if isinstance(config['overlay_color'], str):
                        try:
                            color = QColor(config['overlay_color'])
                            config['overlay_color'] = [
                                color.red(),
                                color.green(),
                                color.blue(),
                                128  # 设置50%透明度
                            ]
                        except Exception as e:
                            print(f"颜色转换错误：{str(e)}，使用默认颜色")
                            config['overlay_color'] = self.default_config['overlay_color']
                    elif not isinstance(config['overlay_color'], list) or len(config['overlay_color']) != 4:
                        print("颜色格式错误，使用默认颜色")
                        config['overlay_color'] = self.default_config['overlay_color']
                    return config
            else:
                print("配置文件不存在，使用默认配置并写入配置文件")
                self.save_config(self.default_config)
                return self.default_config.copy()
        except Exception as e:
            print(f"加载配置文件时出错：{str(e)}")
            return self.default_config.copy()

    def save_config(self, config):
        """保存配置到文件"""
        try:
            # 确保配置包含所有必要的项
            for key, value in self.default_config.items():
                if key not in config:
                    config[key] = value
            
            # 确保颜色值是 RGBA 数组格式
            if not isinstance(config['overlay_color'], list) or len(config['overlay_color']) != 4:
                config['overlay_color'] = self.default_config['overlay_color']
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, allow_unicode=True, default_flow_style=False)
            print("配置已保存")
        except Exception as e:
            print(f"保存配置时出错：{str(e)}")

    def get_config(self):
        """获取当前配置"""
        return self.config

    def update_config(self, new_config):
        """更新配置"""
        self.config = new_config
        self.save_config(self.config) 