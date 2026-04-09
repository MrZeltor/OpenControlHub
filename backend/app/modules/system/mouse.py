import pyautogui
import logging
from app.modules.base import BaseModule

logger = logging.getLogger("OpenControlHub.Mouse")

# Disable pyautogui fail-safe (use with caution, but better for remote control)
pyautogui.FAILSAFE = False

class MouseModule(BaseModule):
    def handle_command(self, action: str, data: any):
        if action == "move":
            self.move(data.get("dx", 0), data.get("dy", 0))
        elif action == "click":
            self.click(data)
        else:
            logger.warning(f"Unknown action for Mouse: {action}")

    def move(self, dx: float, dy: float):
        """Moves the mouse relative to its current position."""
        try:
            # Multiply by sensitivity factor if needed
            pyautogui.moveRel(dx, dy, _pause=False)
        except Exception as e:
            logger.error(f"Failed to move mouse: {str(e)}")

    def click(self, button: str):
        """Performs a mouse click (left, right, middle)."""
        try:
            pyautogui.click(button=button)
            logger.info(f"Mouse click: {button}")
        except Exception as e:
            logger.error(f"Failed to click mouse: {str(e)}")
