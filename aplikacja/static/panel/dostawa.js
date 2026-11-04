(() => {
	const wiersze = document.querySelectorAll('#tabela-dostawy tbody tr');
	const liczba = (tekst) => Number.parseFloat(String(tekst).replace(/\s/g, '').replace(',', '.'));
	const format = (n) => n.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2, signDisplay: 'exceptZero' });

	wiersze.forEach((wiersz) => {
		const pole = wiersz.querySelector('input');
		const przelicz = () => {
			const dostarczono = liczba(pole.value);
			const wpisano = !Number.isNaN(dostarczono);
			wiersz.querySelector('.roznica').textContent = wpisano ? format(dostarczono - liczba(wiersz.dataset.plan)) : '';
			wiersz.classList.toggle('za-malo', wpisano && dostarczono < liczba(wiersz.dataset.rezerwacje));
		};
		pole.addEventListener('input', przelicz);
		przelicz();
	});
})();
