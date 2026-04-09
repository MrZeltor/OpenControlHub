const keyboard = {
    init: () => {
        const input = document.getElementById('hiddenKeyboard');
        if (!input) return;

        input.addEventListener('input', (e) => {
            const char = e.data;
            if (char) {
                sendCommand('keyboard', 'type', char);
                // Clear input but keep focus
                input.value = '';
            }
        });

        input.addEventListener('keydown', (e) => {
            const specialKeys = ['Enter', 'Backspace', 'Escape', 'Tab'];
            if (specialKeys.includes(e.key)) {
                keyboard.pressKey(e.key.toLowerCase());
                if (e.key === 'Enter') input.value = '';
            }
        });
    },

    pressKey: (key) => {
        sendCommand('keyboard', 'press', key);
    },

    toggle: () => {
        const input = document.getElementById('hiddenKeyboard');
        input.focus();
        showToast('Teclado Activo');
    }
};

window.addEventListener('load', () => keyboard.init());
