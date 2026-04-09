const vscode = {
    openProject: (path) => {
        sendCommand('vscode', 'open_path', path);
    },
    
    runMacro: (macroName) => {
        sendCommand('vscode', 'macro', macroName);
    },
    
    sendPrompt: () => {
        const input = document.getElementById('promptInput');
        const text = input.value.trim();
        if (text) {
            sendCommand('vscode', 'type_prompt', text);
            input.value = ''; // Clear after sending
        }
    }
};
