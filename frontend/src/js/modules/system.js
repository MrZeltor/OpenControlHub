const system = {
    openExplorer: (path = "") => {
        sendCommand('system', 'open_explorer', path);
        showToast(`Abriendo Explorador: ${path || 'Inicio'}`);
    },
    
    execute: (command, label) => {
        sendCommand('system', 'open_app', command);
        showToast(`Iniciando: ${label || command}`);
    },

    mediaControl: (key) => {
        sendCommand('system', 'media_key', key);
        // Translation for toasts
        const labels = {
            'volumeup': 'Subir Volumen',
            'volumedown': 'Bajar Volumen',
            'volumemute': 'Silencio',
            'playpause': 'Reproducir/Pausar',
            'nexttrack': 'Siguiente',
            'prevtrack': 'Anterior'
        };
        showToast(labels[key] || key);
    }
};
