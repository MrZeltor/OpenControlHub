import mss
import mss.tools
import base64
import io
import pyautogui
from PIL import Image, ImageDraw
import logging

logger = logging.getLogger("OpenControlHub.Screen")

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()
        self.active_monitor_index = 0
        self.monitor = self.sct.monitors[self.active_monitor_index] 

    def get_monitors_count(self):
        """Returns the number of detected monitors."""
        return len(self.sct.monitors)

    def set_monitor(self, index: int):
        """Switches the active monitor to capture."""
        if 0 <= index < len(self.sct.monitors):
            self.active_monitor_index = index
            self.monitor = self.sct.monitors[index]
            logger.info(f"Switched to monitor {index}")
            return True
        return False

    def get_frame(self, quality=60, max_width=1280):
        """Captures a frame, draws the cursor, compresses it, and returns base64."""
        try:
            # Capture monitor
            sct_img = self.sct.grab(self.monitor)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # --- Draw Mouse Cursor ---
            try:
                mx, my = pyautogui.position()
                # Adjust mouse position relative to the captured monitor
                rx = mx - self.monitor["left"]
                ry = my - self.monitor["top"]
                
                # Check if mouse is within this monitor's bounds
                if 0 <= rx < self.monitor["width"] and 0 <= ry < self.monitor["height"]:
                    draw = ImageDraw.Draw(img)
                    radius = 8
                    # Draw a red circle with an outline for visibility
                    draw.ellipse([rx - radius, ry - radius, rx + radius, ry + radius], fill="#ff0000", outline="white", width=2)
            except Exception as mouse_err:
                logger.debug(f"Failed to draw cursor: {mouse_err}")
            # -------------------------

            # Resize based on target width for better mobile experience
            if img.width > max_width:
                w_percent = (max_width / float(img.width))
                h_size = int((float(img.height) * float(w_percent)))
                img = img.resize((max_width, h_size), Image.Resampling.LANCZOS)
            
            # Save to buffer as JPEG
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            
            # Encode to base64
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return img_str
            
        except Exception as e:
            logger.error(f"Failed to capture frame: {str(e)}")
            return None

screen_capturer = ScreenCapture()
