import subprocess
import pyautogui
import logging
from app.modules.base import BaseModule

logger = logging.getLogger("OpenControlHub.VSCode")

class VSCodeModule(BaseModule):
    def handle_command(self, action: str, data: any):
        if action == "open_path":
            self.open_path(data)
        elif action == "type_prompt":
            self.type_prompt(data)
        elif action == "macro":
            self.run_macro(data)
        else:
            logger.warning(f"Unknown action for VSCode: {action}")

    def open_path(self, path: str):
        """Opens a specific path in VS Code."""
        try:
            # Using shell=True for windows to recognize 'code' command if in PATH
            # On Linux/Mac, shell=False is preferred
            subprocess.Popen(['code', path], shell=True)
            logger.info(f"Opening VS Code at: {path}")
        except Exception as e:
            logger.error(f"Failed to open VS Code: {str(e)}")

    def type_prompt(self, prompt: str):
        """Types a prompt into the active window using PyAutoGUI."""
        try:
            pyautogui.write(prompt, interval=0.01)
            # Press enter to submit if needed, or leave it to the user
            # pyautogui.press('enter')
            logger.info(f"Typed prompt: {prompt[:20]}...")
        except Exception as e:
            logger.error(f"Failed to type prompt: {str(e)}")

    def run_macro(self, macro_name: str):
        """Runs pre-defined macros (Terminal commands, etc)."""
        # Mapping simple macros to keyboard shortcuts or system commands
        macros = {
            "git_status": "git status",
            "git_push": "git push",
            "npm_start": "npm start",
            "terminal_new": ["ctrl", "shift", "`"]
        }
        
        cmd = macros.get(macro_name)
        if isinstance(cmd, list):
            pyautogui.hotkey(*cmd)
        elif isinstance(cmd, str):
            pyautogui.write(cmd)
            pyautogui.press('enter')
        
        logger.info(f"Executed macro: {macro_name}")
