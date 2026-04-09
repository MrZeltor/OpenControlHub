const mouse = {
    lastX: 0,
    lastY: 0,
    sensitivity: 1.5,
    
    init: () => {
        const trackpad = document.getElementById('trackpad');
        if (!trackpad) return;

        trackpad.addEventListener('touchstart', (e) => {
            const touch = e.touches[0];
            mouse.lastX = touch.clientX;
            mouse.lastY = touch.clientY;
            e.preventDefault();
        }, { passive: false });

        trackpad.addEventListener('touchmove', (e) => {
            const touch = e.touches[0];
            const dx = (touch.clientX - mouse.lastX) * mouse.sensitivity;
            const dy = (touch.clientY - mouse.lastY) * mouse.sensitivity;
            
            if (Math.abs(dx) > 0.1 || Math.abs(dy) > 0.1) {
                sendCommand('mouse', 'move', { dx, dy });
            }
            
            mouse.lastX = touch.clientX;
            mouse.lastY = touch.clientY;
            e.preventDefault();
        }, { passive: false });
    },
    
    click: (button) => {
        sendCommand('mouse', 'click', button);
    }
};

// Initialize trackpad after DOM load or when switching tabs
window.addEventListener('load', () => mouse.init());
