const remote = {
    isStreaming: false,
    zoomLevel: 1,
    _pendingFrame: false,

    toggleStream: () => {
        remote.isStreaming = !remote.isStreaming;
        const btn = document.getElementById('toggleStreamBtn');
        if (remote.isStreaming) {
            btn.innerHTML = '<i class="fa-solid fa-pause"></i> Parar';
            btn.classList.add('btn-active');
            remote._pendingFrame = false;
            remote.requestFrame();
            showToast('Transmisión Iniciada');
        } else {
            btn.innerHTML = '<i class="fa-solid fa-play"></i> Iniciar';
            btn.classList.remove('btn-active');
            showToast('Transmisión Parada');
        }
    },

    setMonitor: (index) => {
        sendCommand('system', 'set_monitor', index);
        showToast(`Monitor ${index === '0' ? 'Completo' : index} seleccionado`);
    },

    adjustZoom: (delta) => {
        remote.zoomLevel = Math.min(Math.max(1, remote.zoomLevel + delta), 3);
        const img = document.getElementById('screenStream');
        img.style.transform = `scale(${remote.zoomLevel})`;
        img.style.transformOrigin = 'top left';
        showToast(`Zoom: ${remote.zoomLevel.toFixed(1)}x`);
    },

    forceReload: () => {
        if (!remote.isStreaming) {
            remote.isStreaming = true;
            const btn = document.getElementById('toggleStreamBtn');
            btn.innerHTML = '<i class="fa-solid fa-pause"></i> Parar';
            btn.classList.add('btn-active');
        }
        remote._pendingFrame = false;
        remote.requestFrame();
        showToast('Cuadro recargado');
    },

    requestFrame: () => {
        if (remote.isStreaming && !remote._pendingFrame) {
            remote._pendingFrame = true;
            sendCommand('system', 'request_frame', null);
        }
    },

    handleFrame: (base64Data) => {
        const img = document.getElementById('screenStream');
        img.src = `data:image/jpeg;base64,${base64Data}`;
        remote._pendingFrame = false;

        if (remote.isStreaming && !document.hidden) {
            requestAnimationFrame(() => remote.requestFrame());
        }
    }
};

// Reanudar stream automáticamente al volver de minimizar/cambiar de tab
document.addEventListener('visibilitychange', () => {
    if (!document.hidden && remote.isStreaming) {
        remote._pendingFrame = false;
        remote.requestFrame();
    }
});
