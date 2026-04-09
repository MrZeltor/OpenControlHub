# 📱 OpenControlHub

**Semantic Remote Control for Developers. Control your Host PC from your Mobile.**  
**Control Remoto Semántico para Desarrolladores. Controla tu Host PC desde tu móvil.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

OpenControlHub is a modular, open-source tool that allows you to control your computer's environment through a Mobile-First web interface. Specifically designed for development workflows, it lets you open projects, run terminal macros, and inject text (prompts) using real-time WebSockets.

OpenControlHub es una herramienta modular de código abierto que te permite controlar el entorno de tu computadora a través de una interfaz web Mobile-First. Diseñada específicamente para flujos de trabajo de desarrollo, permite abrir proyectos, ejecutar macros de terminal e inyectar texto (prompts) usando WebSockets en tiempo real.

---

## 🚀 Features / Características

-   **Mobile-First Dashboard:** Clean, responsive UI designed for quick access from any smartphone.
-   **VS Code Integration:** Open folders and inject code/prompts directly into your editor.
-   **Terminal Macros:** Execute common commands (Git, Build, Deploy) with a single tap.
-   **Modular Architecture:** Easily add your own modules (Spotify, System Volume, Home Automation).
-   **Real-time Connection:** Powered by WebSockets for ultra-low latency.
-   **Docker Ready:** Containerized for easy deployment (Headless).

---

## 🛠️ Tech Stack / Tecnologías

-   **Backend:** Python, FastAPI, WebSockets, PyAutoGUI.
-   **Frontend:** Modern Vanilla JS (ES6+), HTML5, CSS3 (Grid/Flexbox).
-   **Deployment:** Docker, Virtualenv.

---

## 📦 Instalación y Uso / Installation & Usage

### Opción A: Ejecutable (.exe) - Recomendado
1. Descarga la última versión desde [Releases](https://github.com/MrZeltor/OpenControlHub/releases).
2. Descomprime el archivo .zip.
3. Ejecuta `OpenControlHub.exe`.
4. El programa detectará tu IP automáticamente. Solo ábrela en tu celular.

### Opción B: Desarrolladores (Python)
#### Windows
```powershell
./scripts/run_host.bat
```

#### Linux / Mac
```bash
./scripts/run_host.sh
```

La interfaz estará disponible en `http://tu-ip-local:8000`.

---

## 🛠️ Cómo crear tu propio .exe
Si has hecho cambios y quieres generar un nuevo ejecutable:
```powershell
./scripts/build.bat
```
El resultado estará en la carpeta `dist/`.

---

## 🤝 Contributing / Contribuciones

Stars are welcome! ⭐ If you want to add a new module (e.g., Docker control, Spotify integration), please check our `modules/` directory and open a PR.

---
Made with ❤️ for the Developer community.
