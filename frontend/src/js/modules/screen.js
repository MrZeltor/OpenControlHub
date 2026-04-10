const remote = {
    isStreaming: false,
    zoomLevel: 1,
    
    toggleStream: () => {
        remote.isStreaming = !remote.isStreaming;
        const btn = document.getElementById('toggleStreamBtn');
        if (remote.isStreaming) {
            btn.textContent = '⏸ Parar';
            btn.classList.add('btn-active');
            remote.requestFrame();
            showToast('Transmisión Iniciada');
        } else {
            btn.textContent = '▶ Iniciar';
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
            btn.textContent = '⏸ Parar';
            btn.classList.add('btn-active');
        }
        remote.requestFrame();
        showToast('Cuadro recargado');
    },
    
    requestFrame: () => {
        if (remote.isStreaming) {
            sendCommand('system', 'request_frame', null);
        }
    },
    
    handleFrame: (base64Data) => {
        const img = document.getElementById('screenStream');
        img.src = `data:image/jpeg;base64,${base64Data}`;
        
        if (remote.isStreaming) {
            requestAnimationFrame(() => remote.requestFrame());
        }
    }
};
