(() => {
	const form = document.getElementById('form-rezerwacja');
	const masa = document.getElementById('masa');
	const wartosc = document.getElementById('wartosc');

	const liczba = (tekst) => Number.parseFloat(String(tekst).replace(/\s/g, '').replace(',', '.')) || 0;
	const format = (n, miejsca) => n.toLocaleString('pl-PL', { minimumFractionDigits: miejsca, maximumFractionDigits: miejsca });

	function przelicz() {
		let kg = 0;
		let zl = 0;
		for (const wiersz of form.querySelectorAll('tbody tr')) {
			const ilosc = Math.max(0, liczba(wiersz.querySelector('input').value));
			kg += ilosc;
			zl += ilosc * liczba(wiersz.dataset.cena);
		}
		masa.textContent = `${format(kg, 1)} kg`;
		wartosc.textContent = `${format(zl, 2)} zł`;
	}

	form.addEventListener('input', przelicz);
	przelicz();
})();
