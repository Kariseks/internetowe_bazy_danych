// Zapamiętaj wybór na tym urządzeniu dla obu paneli.
(() => {
    const toggle = document.querySelector('.kontrast');
    if (!toggle) return;
    function ustaw(wlaczony) {
        document.documentElement.classList.toggle('wysoki-kontrast', wlaczony);
        toggle.setAttribute('aria-pressed', String(wlaczony));
    }
    let preferencja;
    try { preferencja = localStorage.getItem('wysoki-kontrast'); } catch { /* Prywatna sesja. */ }
    ustaw(preferencja === null || preferencja === undefined
        ? matchMedia('(prefers-contrast: more)').matches : preferencja === '1');
    toggle.hidden = false;
    toggle.addEventListener('click', () => {
        const wlaczony = toggle.getAttribute('aria-pressed') !== 'true';
        ustaw(wlaczony);
        try { localStorage.setItem('wysoki-kontrast', wlaczony ? '1' : '0'); } catch { /* Tylko bieżąca strona. */ }
    });
})();
