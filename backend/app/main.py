import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.connection import manager
from app.modules.vscode.handler import VSCodeModule

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

@app.websocket("/ws/control")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message = json.loads(data)
                module_name = message.get("module")
                action = message.get("action")
                payload = message.get("data")

                logger.info(f"Command received: {module_name} -> {action}")

                if module_name == "vscode":
                    vscode_module.handle_command(action, payload)
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
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
