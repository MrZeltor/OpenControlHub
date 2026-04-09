let socket;
const statusEl = document.getElementById('status');
const toastContainer = document.getElementById('toast-container');

// Tab Management
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    
    document.getElementById(tabId).classList.add('active');
    document.querySelector(`[onclick="showTab('${tabId}')"]`).classList.add('active');
}

let currentToastTimeout;

function showToast(message) {
    const container = document.getElementById('toast-container');
    
    // Remove existing toasts immediately
    container.innerHTML = '';
    if (currentToastTimeout) clearTimeout(currentToastTimeout);

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    container.appendChild(toast);
    
    currentToastTimeout = setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => toast.remove(), 300);
    }, 1500); // Faster disappearance
}

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/control`;
    
    console.log("Connecting to:", wsUrl);
    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        statusEl.textContent = 'Conectado';
        statusEl.className = 'status-connected';
        showToast('Conectado al PC');
    };

    socket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'frame') {
                if (typeof remote !== 'undefined') {
                    remote.handleFrame(message.data);
                }
            } else if (message.type === 'monitors_count') {
                updateMonitorSelector(message.data);
            }
        } catch (e) {
            console.error('Error parsing WS message:', e);
        }
    };

function updateMonitorSelector(count) {
    const selector = document.getElementById('monitorSelect');
    if (!selector) return;
    
    selector.innerHTML = '<option value="0">Toda la Pantalla</option>';
    for (let i = 1; i < count; i++) {
        selector.innerHTML += `<option value="${i}">Monitor ${i}</option>`;
    }
}

    socket.onclose = () => {
        statusEl.textContent = 'Desconectado';
        statusEl.className = 'status-disconnected';
        setTimeout(connect, 3000);
    };

    socket.onerror = (error) => {
        console.error('WebSocket Error:', error);
    };
}

function sendCommand(module, action, data) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        const payload = JSON.stringify({ module, action, data });
        socket.send(payload);
    } else {
        showToast('Error: Sin conexión al PC');
    }
}

// Initial connection
connect();
