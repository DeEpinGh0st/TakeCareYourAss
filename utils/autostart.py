import os
import sys
import platform
from pathlib import Path

class AutoStartManager:
    def __init__(self):
        self.app_name = "TakeCareAss"
        self.is_windows = platform.system().lower() == "windows"
        self.is_linux = platform.system().lower() == "linux"
        if self.is_windows:
            import winreg
            import win32com.client
            self.winreg = winreg
            self.win32com = win32com
            self.startup_folder = self._get_startup_folder()
            self.shortcut_path = os.path.join(self.startup_folder, f"{self.app_name}.lnk")
        elif self.is_linux:
            self.autostart_dir = os.path.expanduser("~/.config/autostart")
            self.desktop_file = os.path.join(self.autostart_dir, f"{self.app_name}.desktop")

    def _get_startup_folder(self):
        """获取Windows启动文件夹路径"""
        try:
            with self.winreg.OpenKey(self.winreg.HKEY_CURRENT_USER, 
                              r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders") as key:
                return self.winreg.QueryValueEx(key, "Startup")[0]
        except Exception:
            # 如果注册表读取失败，使用默认路径
            return os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup")

    def create_shortcut(self):
        """创建开机自启快捷方式（Windows）"""
        try:
            # 获取当前程序的完整路径
            if getattr(sys, 'frozen', False):
                app_path = sys.executable
            else:
                app_path = os.path.abspath(sys.argv[0])
            # 创建快捷方式
            shell = self.win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(self.shortcut_path)
            shortcut.Targetpath = app_path
            shortcut.WorkingDirectory = os.path.dirname(app_path)
            shortcut.save()
            return True
        except Exception as e:
            print(f"创建快捷方式失败: {str(e)}")
            return False

    def remove_shortcut(self):
        """删除开机自启快捷方式（Windows）"""
        try:
            if os.path.exists(self.shortcut_path):
                os.remove(self.shortcut_path)
            return True
        except Exception as e:
            print(f"删除快捷方式失败: {str(e)}")
            return False

    def create_desktop_file(self):
        """创建Linux自启动.desktop文件"""
        try:
            if getattr(sys, 'frozen', False):
                app_path = sys.executable
            else:
                app_path = os.path.abspath(sys.argv[0])
            os.makedirs(self.autostart_dir, exist_ok=True)
            content = f"""[Desktop Entry]\nType=Application\nExec={app_path}\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName={self.app_name}\n"""
            with open(self.desktop_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"创建.desktop文件失败: {str(e)}")
            return False

    def remove_desktop_file(self):
        """删除Linux自启动.desktop文件"""
        try:
            if os.path.exists(self.desktop_file):
                os.remove(self.desktop_file)
            return True
        except Exception as e:
            print(f"删除.desktop文件失败: {str(e)}")
            return False

    def is_autostart_enabled(self):
        if self.is_windows:
            return os.path.exists(self.shortcut_path)
        elif self.is_linux:
            return os.path.exists(self.desktop_file)
        return False

    def set_autostart(self, enable):
        if self.is_windows:
            if enable:
                return self.create_shortcut()
            else:
                return self.remove_shortcut()
        elif self.is_linux:
            if enable:
                return self.create_desktop_file()
            else:
                return self.remove_desktop_file()
        return False 