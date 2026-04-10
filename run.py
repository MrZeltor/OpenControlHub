import sys
import os
# Evitar crash de uvicorn en modo --noconsole (donde stdout es None)
if sys.stdout is None: sys.stdout = open(os.devnull, "w")
if sys.stderr is None: sys.stderr = open(os.devnull, "w")

import uvicorn
import socket
import ctypes
import threading
import pyperclip

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == "__main__":
    local_ip = get_ip()
    port = 8000
    
    link_completo = f"http://{local_ip}:{port}"
    
    # Copiamos automáticamente el enlace al portapapeles 
    try:
        pyperclip.copy(link_completo)
    except:
        pass

    # Resolve base directory (works both for script and PyInstaller bundle)
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Setup the popup function to be used by startup and by tray menu
    def show_popup():
        if os.name == 'nt':
            MB_OK = 0x0
            MB_ICONINFO = 0x40
            title = "OpenControlHub - Servidor Iniciado"
            spaces = " " * 30
            msg = f"¡Servidor activo!\n\nLink:\n{link_completo}\n\n(El link ha sido copiado a tu portapapeles. Solo pégalo y envíatelo al celular){spaces}"
            ctypes.windll.user32.MessageBoxW(0, msg, title, MB_OK | MB_ICONINFO)

    # Pystray logic
    try:
        import pystray
        from PIL import Image
        from pystray import MenuItem as item
        
        def on_show_ip(icon, item):
            try:
                pyperclip.copy(link_completo)
            except: pass
            threading.Thread(target=show_popup, daemon=True).start()
            
        def on_quit(icon, item):
            icon.stop()
            os._exit(0) # Force kill uvicorn
            
        icon_path = os.path.join(base_dir, "icon.ico")
        if os.path.exists(icon_path):
            image = Image.open(icon_path)
        else:
            image = Image.new('RGB', (64, 64), color = (73, 109, 137))
            
        menu = pystray.Menu(
            item('Copiar y Mostrar IP', on_show_ip),
            item('Salir de OpenControlHub', on_quit)
        )
        tray_icon = pystray.Icon("OpenControlHub", image, "OpenControlHub", menu)
        
        def setup_tray(icon):
            icon.visible = True
            threading.Thread(target=show_popup, daemon=True).start()
            
        def run_tray():
            tray_icon.run(setup_tray)
            
        threading.Thread(target=run_tray, daemon=True).start()
    except Exception as e:
        threading.Thread(target=show_popup, daemon=True).start()

    # Add backend to sys.path so uvicorn can find app.main
    backend_dir = os.path.join(base_dir, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    # Change working directory so relative paths in main.py work (e.g. "frontend")
    os.chdir(base_dir)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
