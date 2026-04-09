@echo off
echo [OpenControlHub] Iniciando proceso de empaquetado...

:: Activar entorno virtual
if exist "venv" (
    call venv\Scripts\activate
) else (
    echo [Error] Entorno virtual no encontrado. Ejecuta scripts\run_host.bat primero.
    exit /b 1
)

:: Instalar PyInstaller si no existe
pip install pyinstaller

:: Ejecutar PyInstaller
echo [OpenControlHub] Creando ejecutable .exe (esto puede tardar unos minutos)...
:: --add-data "origen;destino" (en Windows usa ;)
:: Incluimos la carpeta frontend y la estructura de backend
pyinstaller --noconfirm --onedir --console --name "OpenControlHub" ^
    --add-data "frontend;frontend" ^
    --add-data "backend;backend" ^
    --hidden-import "uvicorn.logging" ^
    --hidden-import "uvicorn.loops" ^
    --hidden-import "uvicorn.loops.auto" ^
    --hidden-import "uvicorn.protocols" ^
    --hidden-import "uvicorn.protocols.http" ^
    --hidden-import "uvicorn.protocols.http.auto" ^
    --hidden-import "uvicorn.protocols.websockets" ^
    --hidden-import "uvicorn.protocols.websockets.auto" ^
    --hidden-import "uvicorn.lifespan" ^
    --hidden-import "uvicorn.lifespan.on" ^
    "run.py"

echo.
echo [OpenControlHub] ¡Proceso completado!
echo [OpenControlHub] El ejecutable se encuentra en: dist\OpenControlHub\OpenControlHub.exe
echo [OpenControlHub] Puedes comprimir la carpeta 'dist\OpenControlHub' para distribuirla.
pause
