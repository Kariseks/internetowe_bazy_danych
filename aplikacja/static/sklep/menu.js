// Menu boczne na telefonie. Bez JavaScriptu odnośniki zostają w nagłówku (sklep.css).
(() => {
	const przycisk = document.querySelector('.burger');
	const menu = document.getElementById('menu');
	const zaslona = document.querySelector('.zaslona');
	if (!przycisk || !menu || !zaslona) return;

	const telefon = window.matchMedia('(max-width: 40rem)');
	// Klasę menu-js dodaje skrypt w <head>, przed pierwszym rysowaniem; animacje dopiero po nim.
	requestAnimationFrame(() => requestAnimationFrame(() => document.documentElement.classList.add('menu-animacje')));

	function ustaw(otwarte) {
		document.documentElement.classList.toggle('menu-otwarte', otwarte);
		przycisk.setAttribute('aria-expanded', String(otwarte));
		if (otwarte) {
			menu.querySelector('a, button').focus();
		}
	}

	function zamknij() {
		if (przycisk.getAttribute('aria-expanded') !== 'true') return;
		ustaw(false);
		przycisk.focus();
	}

	przycisk.addEventListener('click', () => {
		if (przycisk.getAttribute('aria-expanded') === 'true') zamknij();
		else ustaw(true);
	});
	zaslona.addEventListener('click', zamknij);
	document.addEventListener('keydown', (e) => { if (e.key === 'Escape') zamknij(); });
	telefon.addEventListener('change', () => ustaw(false));
})();
