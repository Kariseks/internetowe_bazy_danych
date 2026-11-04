"""Dane przykładowe dla stubów z services.py. Do usunięcia, gdy stuby dostaną logikę."""
from datetime import datetime, time, timedelta
from decimal import Decimal as D
from types import SimpleNamespace as Atrapa

from django.contrib.auth.models import User
from django.utils import timezone


class Produkt(Atrapa):
    def __str__(self):
        return f'{self.nazwa} ({self.odmiana})' if self.odmiana else self.nazwa


_PRODUKTY = [
    # id, nazwa, odmiana, standardowa ilość, cena, stan
    (1, 'Ziemniaki', 'Irys', '120', '3.20', '84.50'),
    (2, 'Marchew', '', '60', '3.80', '41.20'),
    (3, 'Cebula', 'żółta', '50', '3.50', '37.00'),
    (4, 'Pomidory', 'malinowe', '30', '14.90', '12.40'),
    (5, 'Ogórki', 'gruntowe', '30', '8.90', '18.75'),
    (6, 'Kapusta', 'biała', '40', '3.00', '26.00'),
    (7, 'Buraki', '', '30', '3.40', '22.30'),
    (8, 'Jabłka', 'Ligol', '80', '4.50', '53.60'),
    (9, 'Gruszki', 'Konferencja', '25', '7.90', '0.00'),
]


def teraz():
    return timezone.localtime()


def _produkt(wiersz):
    return Produkt(id=wiersz[0], nazwa=wiersz[1], odmiana=wiersz[2], standardowa_ilosc_kg=D(wiersz[3]), w_ofercie=True)


def produkty():
    return [_produkt(w) for w in _PRODUKTY]


def produkt(produkt_id):
    return next(p for p in produkty() if p.id == produkt_id)


def cena(produkt_id):
    return D(next(w[4] for w in _PRODUKTY if w[0] == produkt_id))


def produkty_z_cenami():
    wiersze = [_produkt(w) for w in _PRODUKTY]
    for p in wiersze:
        p.cena_za_kg = cena(p.id)
    wycofany = Produkt(id=10, nazwa='Szparagi', odmiana='', standardowa_ilosc_kg=D('10'), w_ofercie=False, cena_za_kg=D('24.00'))
    return wiersze + [wycofany]


def produkt_z_historia_cen(produkt_id):
    p = next((p for p in produkty_z_cenami() if p.id == produkt_id), None)
    if p is None:
        return None
    dzis = timezone.localdate()
    p.ceny = [
        Atrapa(cena_za_kg=p.cena_za_kg, obowiazuje_od=dzis - timedelta(days=12)),
        Atrapa(cena_za_kg=(p.cena_za_kg - D('0.30')), obowiazuje_od=dzis - timedelta(days=60)),
    ]
    return p


def stan_produktow():
    return [Atrapa(produkt=_produkt(w), cena_za_kg=D(w[4]), stan_kg=D(w[5])) for w in _PRODUKTY]


def klienci():
    dane = [
        (11, 'Anna', 'Kowalska', 'kowalska', '501 200 300', '0.00'),
        (12, 'Piotr', 'Wiśniewski', 'wisniewski', '602 111 222', '12.40'),
        (13, 'Maria', 'Zielińska', 'zielinska', '703 444 555', '0.00'),
        (14, 'Tomasz', 'Lewandowski', 'lewandowski', '504 777 888', '118.60'),
        (15, 'Ewa', 'Kamińska', 'kaminska', '605 999 000', '36.20'),
    ]
    return [
        Atrapa(
            uzytkownik_id=i,
            uzytkownik=User(id=i, first_name=imie, last_name=nazwisko, email=f'{adres}@example.com'),
            telefon=telefon,
            identyfikator_karty=f'tok_{i}',
            zaleglosc=D(zaleglosc),
            zablokowany=D(zaleglosc) > 100,
        )
        for i, imie, nazwisko, adres, telefon, zaleglosc in dane
    ]


def klient(klient_id):
    return next((k for k in klienci() if k.uzytkownik_id == klient_id), None)


def _rezerwacja(rezerwacja_id, klient_id, dzien, stan, pozycje, odwazone=False):
    wiersze = [
        Atrapa(
            produkt=produkt(p),
            ilosc_kg=D(ilosc),
            masa_odwazona_kg=(D(ilosc) - D('0.05')) if odwazone else None,
        )
        for p, ilosc in pozycje
    ]
    return Atrapa(
        id=rezerwacja_id,
        klient=klient(klient_id),
        dzien_odbioru=dzien,
        stan=stan,
        zlozono=timezone.make_aware(datetime.combine(dzien - timedelta(days=1), time(15, 20))),
        pozycje=wiersze,
        laczna_masa=sum(w.ilosc_kg for w in wiersze),
    )


def rezerwacje(dzien):
    if dzien == timezone.localdate():
        return [
            _rezerwacja(101, 11, dzien, 'zlozona', [(1, '10.0'), (2, '3.5')]),
            _rezerwacja(102, 12, dzien, 'przygotowana', [(8, '12.0'), (6, '4.0')], odwazone=True),
            _rezerwacja(103, 13, dzien, 'zlozona', [(4, '2.5'), (5, '2.0'), (3, '1.5')]),
            _rezerwacja(104, 15, dzien, 'odebrana', [(1, '15.0')], odwazone=True),
        ]
    if dzien < timezone.localdate():
        return [
            _rezerwacja(201, 11, dzien, 'odebrana', [(1, '8.0')], odwazone=True),
            _rezerwacja(202, 14, dzien, 'nieodebrana', [(8, '20.0')]),
            _rezerwacja(203, 13, dzien, 'anulowana', [(5, '3.0')]),
        ]
    return [_rezerwacja(301, 13, dzien, 'zlozona', [(1, '6.0'), (7, '2.0')])]


def rezerwacja(rezerwacja_id):
    return next((r for r in rezerwacje(timezone.localdate()) if r.id == rezerwacja_id), None)


def wydanie(rezerwacja_id):
    r = rezerwacja(rezerwacja_id)
    if r is None:
        return None
    pozycje = [
        Atrapa(
            produkt=p.produkt,
            ilosc_kg=p.ilosc_kg,
            masa_kg=p.masa_odwazona_kg,
            cena_za_kg=cena(p.produkt.id),
            wartosc=(p.masa_odwazona_kg * cena(p.produkt.id)).quantize(D('0.01')),
        )
        for p in r.pozycje
    ]
    return Atrapa(rezerwacja=r, pozycje=pozycje, do_zaplaty=sum(p.wartosc for p in pozycje))


def _plan(produkt_wiersz, dzien):
    # Liczby zależne od dnia, żeby tabela nie wyglądała jak kopia jednego dnia.
    p = _produkt(produkt_wiersz)
    plan = p.standardowa_ilosc_kg + (10 if dzien.weekday() == 4 and p.id == 1 else 0)
    zarezerwowano = D((p.id * 3 + dzien.toordinal() % 7) % 19) if dzien.toordinal() % 7 < 5 else D(0)
    return plan, min(plan, zarezerwowano)


def plan_na_dzien(dzien):
    wiersze = []
    for w in _PRODUKTY:
        plan, zarezerwowano = _plan(w, dzien)
        wiersze.append(Atrapa(produkt=_produkt(w), plan_kg=plan, zarezerwowano_kg=zarezerwowano))
    return wiersze


def plan_tygodnia():
    dzis = timezone.localdate()
    dni = [dzis + timedelta(days=n) for n in range(1, 8)]
    zamkniety_jutro = teraz().hour >= 18
    dni_opis = [Atrapa(dzien=d, zamkniety=zamkniety_jutro and d == dni[0]) for d in dni]
    wiersze = []
    for w in _PRODUKTY:
        komorki = []
        for opis in dni_opis:
            plan, zarezerwowano = _plan(w, opis.dzien)
            komorki.append(Atrapa(
                dzien=opis.dzien,
                zamkniety=opis.zamkniety,
                plan_kg=plan,
                zarezerwowano_kg=zarezerwowano,
                dostepne_kg=plan - zarezerwowano,
                produkt=_produkt(w),
            ))
        wiersze.append(Atrapa(produkt=_produkt(w), komorki=komorki))
    return Atrapa(dni=dni_opis, wiersze=wiersze)


def dostawa(dzien):
    if dzien >= timezone.localdate():
        return None
    pozycje = []
    for w in plan_na_dzien(dzien):
        dostarczono = w.plan_kg - (5 if w.produkt.id == 9 else 0)
        if w.produkt.id == 4:
            w.zarezerwowano_kg = D('14')
            dostarczono = D('12')
        pozycje.append(Atrapa(
            produkt=w.produkt,
            plan_kg=w.plan_kg,
            zarezerwowano_kg=w.zarezerwowano_kg,
            dostarczono_kg=dostarczono,
            roznica_kg=dostarczono - w.plan_kg,
            za_malo=dostarczono < w.zarezerwowano_kg,
        ))
    return Atrapa(dzien=dzien, zarejestrowano=timezone.make_aware(datetime.combine(dzien, time(5, 40))), pozycje=pozycje)


def historia_sprzedazy(od, do):
    sprzedawca = User(id=2, first_name='Jan', last_name='Nowak')
    sprzedaze = []
    for numer, (godzina, pozycje, rezerwacja_id) in enumerate([
        (time(16, 42), [(1, '2.40'), (3, '0.85')], None),
        (time(15, 18), [(8, '1.20')], None),
        (time(11, 5), [(1, '14.95')], 104),
        (time(9, 31), [(4, '0.60'), (5, '1.10'), (2, '1.00')], None),
    ], start=1):
        wiersze = [
            Atrapa(produkt=produkt(p), masa_kg=D(m), cena_za_kg=cena(p), wartosc=(D(m) * cena(p)).quantize(D('0.01')))
            for p, m in pozycje
        ]
        sprzedaze.append(Atrapa(
            id=numer,
            data_czas=timezone.make_aware(datetime.combine(do, godzina)),
            sprzedawca=sprzedawca,
            rezerwacja_id=rezerwacja_id,
            pozycje=wiersze,
            suma=sum(w.wartosc for w in wiersze),
        ))
    return sprzedaze


def zestawienia(od, do):
    return Atrapa(
        sprzedaz=[
            Atrapa(produkt=produkt(p), masa_kg=D(m), wartosc=(D(m) * cena(p)).quantize(D('0.01')))
            for p, m in [(1, '842.50'), (8, '416.20'), (2, '233.00'), (4, '98.40')]
        ],
        ubytki=[Atrapa(produkt=produkt(4), masa_kg=D('14.20')), Atrapa(produkt=produkt(5), masa_kg=D('6.50'))],
        roznice=[w for w in (dostawa(do) or dostawa(timezone.localdate() - timedelta(days=1))).pozycje if w.roznica_kg],
        nieodebrane=Atrapa(liczba=4, wartosc=D('312.80')),
    )


def karta_klienta(klient_id):
    k = klient(klient_id)
    if k is None:
        return None
    dzis = timezone.localdate()
    wczoraj = dzis - timedelta(days=1)
    rezerwacje_klienta = [r for r in rezerwacje(dzis) + rezerwacje(wczoraj) if r.klient.uzytkownik_id == klient_id]
    pracownik = User(id=2, first_name='Jan', last_name='Nowak')
    oplaty = []
    rozliczenia = []
    if k.zaleglosc:
        oplaty = [Atrapa(rezerwacja_id=202, dzien_odbioru=wczoraj, oplata_za_nieodebranie=k.zaleglosc)]
        rozliczenia = [Atrapa(
            data_czas=timezone.make_aware(datetime.combine(wczoraj, time(9, 0))),
            rodzaj='obciazenie',
            kwota=k.zaleglosc,
            skuteczne=False,
            zarejestrowal=pracownik,
        )]
    return Atrapa(
        klient=k,
        rezerwacja_dzis=next((r for r in rezerwacje_klienta if r.dzien_odbioru == dzis and r.stan in ('zlozona', 'przygotowana')), None),
        rezerwacje=rezerwacje_klienta,
        oplaty=oplaty,
        rozliczenia=rozliczenia,
    )


def konta():
    dane = [
        (1, 'jnowak', 'Jan', 'Nowak', 'wlasciciel', True),
        (2, 'mkowal', 'Magda', 'Kowal', 'sprzedawca', True),
        (3, 'kbak', 'Kamil', 'Bąk', 'sprzedawca', True),
        (4, 'osik', 'Olga', 'Sikora', 'sprzedawca', False),
    ]
    wynik = [
        User(id=i, username=login, first_name=imie, last_name=nazwisko, email=f'{login}@warzywniak.example', is_active=aktywne)
        for i, login, imie, nazwisko, _, aktywne in dane
    ]
    for u, wiersz in zip(wynik, dane, strict=True):
        u.rola = wiersz[4]
    for k in klienci():
        k.uzytkownik.username = k.uzytkownik.email
        k.uzytkownik.rola = 'klient'
        wynik.append(k.uzytkownik)
    return wynik
