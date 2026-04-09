const apps = {
    launch: (command, label) => {
        sendCommand('system', 'open_app', command);
        showToast(`Iniciando: ${label}`);
    },
    
    sendPrompt: () => {
        const input = document.getElementById('promptInput');
        const text = input.value.trim();
        if (text) {
            sendCommand('keyboard', 'type', text);
            showToast('Texto enviado al PC');
            input.value = ''; 
        }
    }
};
