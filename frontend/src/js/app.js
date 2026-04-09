let socket;
const statusEl = document.getElementById('status');

function connect() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Use window.location.host to automatically detect IP/Port
    const wsUrl = `${protocol}//${window.location.host}/ws/control`;
    
    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        statusEl.textContent = 'Connected';
        statusEl.className = 'status-connected';
        console.log('Connected to OpenControlHub Host');
    };

    socket.onclose = () => {
        statusEl.textContent = 'Disconnected';
        statusEl.className = 'status-disconnected';
        console.log('Disconnected. Retrying in 3s...');
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
        alert('Not connected to Host PC');
    }
}

// Initial connection
connect();
