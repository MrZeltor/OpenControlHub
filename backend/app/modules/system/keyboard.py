import pyautogui
import pyperclip
import logging
from app.modules.base import BaseModule

logger = logging.getLogger("OpenControlHub.Keyboard")

class KeyboardModule(BaseModule):
    def handle_command(self, action: str, data: any):
        if action == "type":
            self.type_text(data)
        elif action == "press":
            self.press_key(data)
        else:
            logger.warning(f"Unknown action for Keyboard: {action}")

    def type_text(self, text: str):
        """Types a string of text. Uses clipboard for special characters like 'ñ'."""
        try:
            # Check if text is a single character and non-ASCII (e.g., 'ñ', 'á', emojis)
            # Or if it contains non-ASCII characters
            if not text.isascii():
                # For non-ASCII, copying and pasting is much more reliable
                pyperclip.copy(text)
                pyautogui.hotkey('ctrl', 'v')
                logger.info(f"Pasted special text: {text}")
            else:
                pyautogui.write(text, interval=0.01)
        except Exception as e:
            logger.error(f"Failed to type text: {str(e)}")

    def press_key(self, key: str):
        """Presses a specific key (e.g., 'enter', 'backspace')."""
        try:
            pyautogui.press(key)
        except Exception as e:
            logger.error(f"Failed to press key {key}: {str(e)}")
