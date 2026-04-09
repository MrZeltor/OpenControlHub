import json
import logging
import os
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.connection import manager
from app.modules.vscode.handler import VSCodeModule
from app.modules.system.handler import SystemModule
from app.modules.system.screen import screen_capturer
from app.modules.system.mouse import MouseModule
from app.modules.system.keyboard import KeyboardModule

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OpenControlHub")

app = FastAPI(title="OpenControlHub")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
vscode_module = VSCodeModule()
system_module = SystemModule()
mouse_module = MouseModule()
keyboard_module = KeyboardModule()

@app.websocket("/ws/control")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    # Send monitor count on connection
    await websocket.send_json({
        "type": "monitors_count",
        "data": screen_capturer.get_monitors_count()
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                module_name = message.get("module")
                action = message.get("action")
                payload = message.get("data")

                if module_name == "system" and action == "request_frame":
                    frame = screen_capturer.get_frame(quality=50) 
                    if frame:
                        await websocket.send_json({
                            "type": "frame",
                            "data": frame
                        })
                elif module_name == "system" and action == "set_monitor":
                    screen_capturer.set_monitor(int(payload))
                elif module_name == "vscode":
                    vscode_module.handle_command(action, payload)
                elif module_name == "system":
                    system_module.handle_command(action, payload)
                elif module_name == "mouse":
                    mouse_module.handle_command(action, payload)
                elif module_name == "keyboard":
                    keyboard_module.handle_command(action, payload)
                else:
                    logger.warning(f"Unknown module: {module_name}")

            except json.JSONDecodeError:
                logger.error("Failed to decode JSON message")
            except Exception as e:
                logger.error(f"Error handling command: {str(e)}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")

# Mount frontend static files
# Use absolute path so it works both in dev and PyInstaller bundle
_base_dir = getattr(sys, '_MEIPASS', None) or os.getcwd()
_frontend_dir = os.path.join(_base_dir, "frontend")
app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")
