@echo off
echo [OpenControlHub] Initializing Host PC...

:: Check for virtual environment
if not exist "venv" (
    echo [OpenControlHub] Creating virtual environment...
    python -m venv venv
)

:: Activate venv and install dependencies
echo [OpenControlHub] Installing/Updating dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

:: Start the server
echo [OpenControlHub] Starting FastAPI Server on port 8000...
echo [OpenControlHub] Access from mobile using your PC IP (e.g., http://192.168.1.XX:8000)
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000 --reload
