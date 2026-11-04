(() => {
	const form = document.getElementById('form-sprzedaz');
	const pozycje = document.getElementById('pozycje');
	const wzor = document.getElementById('wzor-pozycji');
	const suma = document.getElementById('suma');
	const pusto = document.getElementById('pusto');
	const zatwierdz = document.getElementById('zatwierdz');
	const filtr = document.getElementById('filtr');
	const licznik = form.querySelector('[name="form-TOTAL_FORMS"]');
	const skrzynki = [...form.querySelectorAll('.skrzynka')];

	const liczba = (tekst) => Number.parseFloat(String(tekst).replace(/\s/g, '').replace(',', '.')) || 0;
	const zl = (n) => `${n.toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} zł`;
	const skrzynka = (id) => skrzynki.find((s) => s.dataset.id === String(id));
	const poleProduktu = (wiersz) => wiersz.querySelector('input[name$="-produkt"]');
	const poleMasy = (wiersz) => wiersz.querySelector('input[name$="-masa_kg"]');

	function przelicz() {
		let razem = 0;
		for (const wiersz of pozycje.rows) {
			const wartosc = Math.max(0, liczba(poleMasy(wiersz).value)) * liczba(wiersz.dataset.cena);
			wiersz.querySelector('.pozycja-wartosc').textContent = zl(wartosc);
			razem += wartosc;
		}
		suma.textContent = zl(razem);
		pusto.hidden = pozycje.rows.length > 0;
		zatwierdz.disabled = pozycje.rows.length === 0;
	}

	function opisz(wiersz) {
		const s = skrzynka(poleProduktu(wiersz).value);
		if (!s) return;
		wiersz.dataset.cena = s.dataset.cena;
		wiersz.querySelector('.pozycja-nazwa').textContent = s.dataset.nazwa;
		wiersz.querySelector('.pozycja-cena').textContent = `${zl(liczba(s.dataset.cena))} za kg`;
	}

	function ponumeruj() {
		[...pozycje.rows].forEach((wiersz, i) => {
			wiersz.querySelectorAll('[name], [id], [for]').forEach((el) => {
				for (const atrybut of ['name', 'id', 'for']) {
					const wartosc = el.getAttribute(atrybut);
					if (wartosc) el.setAttribute(atrybut, wartosc.replace(/form-\d+-/, `form-${i}-`));
				}
			});
		});
		licznik.value = pozycje.rows.length;
	}

	function dodaj(s) {
		const obecny = [...pozycje.rows].find((w) => poleProduktu(w).value === s.dataset.id);
		if (obecny) {
			poleMasy(obecny).select();
			return;
		}
		const szablon = document.createElement('template');
		szablon.innerHTML = wzor.innerHTML.replaceAll('__prefix__', pozycje.rows.length);
		const wiersz = szablon.content.firstElementChild;
		poleProduktu(wiersz).value = s.dataset.id;
		pozycje.append(wiersz);
		opisz(wiersz);
		ponumeruj();
		przelicz();
		poleMasy(wiersz).focus();
	}

	skrzynki.forEach((s) => s.addEventListener('click', () => dodaj(s)));

	pozycje.addEventListener('input', przelicz);
	pozycje.addEventListener('click', (zdarzenie) => {
		if (!zdarzenie.target.matches('.usun')) return;
		zdarzenie.target.closest('tr').remove();
		ponumeruj();
		przelicz();
		filtr.focus();
	});
	pozycje.addEventListener('keydown', (zdarzenie) => {
		if (zdarzenie.key !== 'Enter') return;
		zdarzenie.preventDefault();
		filtr.value = '';
		filtr.dispatchEvent(new Event('input'));
		filtr.focus();
	});

	const widoczne = () => skrzynki.filter((s) => !s.hidden && !s.disabled);
	filtr.addEventListener('input', () => {
		const fraza = filtr.value.trim().toLowerCase();
		skrzynki.forEach((s) => { s.hidden = !s.dataset.nazwa.toLowerCase().includes(fraza); });
	});
	filtr.addEventListener('keydown', (zdarzenie) => {
		if (zdarzenie.key !== 'Enter') return;
		zdarzenie.preventDefault();
		const pierwsza = widoczne()[0];
		if (filtr.value.trim() && pierwsza) dodaj(pierwsza);
	});

	[...pozycje.rows].forEach(opisz);
	przelicz();
})();
