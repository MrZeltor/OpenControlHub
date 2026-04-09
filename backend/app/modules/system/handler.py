import subprocess
import os
import platform
import logging
import pyautogui
from app.modules.base import BaseModule

logger = logging.getLogger("OpenControlHub.System")

class SystemModule(BaseModule):
    def handle_command(self, action: str, data: any):
        if action == "open_explorer":
            self.open_explorer(data)
        elif action == "open_app":
            self.open_app(data)
        elif action == "media_key":
            self.media_control(data)
        else:
            logger.warning(f"Unknown action for System: {action}")

    def media_control(self, key: str):
        """Presses a media key (volumeup, volumedown, playpause, etc)."""
        try:
            # PyAutoGUI keys: volumeup, volumedown, volumemute, playpause, nexttrack, prevtrack
            pyautogui.press(key)
            logger.info(f"Media key pressed: {key}")
        except Exception as e:
            logger.error(f"Failed to press media key: {str(e)}")

    def open_explorer(self, path: str):
        """Opens the file explorer at a specific path (Cross-platform)."""
        try:
            # Expand common path shortcuts (e.g., Documents, Downloads)
            expanded_path = os.path.expanduser(path) if path.startswith("~") else path
            
            # Use specific system commands
            system = platform.system()
            if system == "Windows":
                # Normalize path for Windows
                clean_path = os.path.normpath(expanded_path)
                subprocess.Popen(['explorer', clean_path])
            elif system == "Darwin": # macOS
                subprocess.Popen(['open', expanded_path])
            else: # Linux
                subprocess.Popen(['xdg-open', expanded_path])
                
            logger.info(f"Opened explorer at: {expanded_path}")
        except Exception as e:
            logger.error(f"Failed to open explorer: {str(e)}")

    def open_app(self, app_path: str):
        """Opens a generic application, shortcut or run a system command."""
        try:
            if platform.system() == "Windows":
                # os.startfile is the most reliable way to "double click" anything in Windows
                # It handles .exe, .lnk, URI schemes (discord://), etc.
                os.startfile(app_path)
            else:
                subprocess.Popen(app_path, shell=True)
            logger.info(f"Executed app: {app_path}")
        except Exception as e:
            logger.error(f"Failed to execute app {app_path}: {str(e)}")
