import uvicorn
import socket
import os
import sys

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

    print("="*50)
    print("       OpenControlHub - Host Server")
    print("="*50)
    print(f"\n[*] SERVIDOR ACTIVO EN TU RED LOCAL")
    print(f"[*] Abre en tu celular: http://{local_ip}:{port}")
    print("\n[!] IMPORTANTE:")
    print("1. Mantén esta ventana abierta (o minimizada).")
    print("2. Tu celular debe estar en el mismo Wi-Fi que el PC.")
    print("-"*50)

    # Resolve base directory (works both for script and PyInstaller bundle)
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Add backend to sys.path so uvicorn can find app.main
    backend_dir = os.path.join(base_dir, "backend")
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)

    # Change working directory so relative paths in main.py work (e.g. "frontend")
    os.chdir(base_dir)

    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
