"""Dwa przekroje całego sklepu w tym samym układzie do wydruku na A4."""
import html
import subprocess


# Współrzędne w punktach. Konto i produkt zajmują całą szerokość diagramu,
# dzięki czemu każdy dokument łączy się z nimi osobną pionową linią.
SZEROKOSCI = (170, 160, 136, 140, 110, 120)
ENCJE = {
    # tabela: kolumna, wysokość, nazwa pojęcia, wybrane atrybuty dziedzinowe
    "auth_group": (1, 420, "Rola", "nazwa"),
    "auth_user_groups": (3, 420, "Przypisanie roli", ""),
    "auth_user": (None, 349, "Konto", "login"),
    "rozliczenie_zaleglosci": (0, 259, "Rozliczenie zaległości", "kwota, wynik"),
    "profil_klienta": (1, 259, "Profil klienta", "telefon"),
    "rezerwacja": (1, 178, "Rezerwacja", "dzień odbioru, stan"),
    "sprzedaz": (2, 178, "Sprzedaż", "chwila sprzedaży"),
    "dostawa": (3, 178, "Dostawa", "dzień przyjęcia"),
    "ubytek": (4, 178, "Ubytek", "ilość utracona"),
    "korekta_stanu": (5, 178, "Korekta stanu", "różnica, przyczyna"),
    "pozycja_rezerwacji": (1, 99, "Pozycja rezerwacji", "ilość zamówiona"),
    "pozycja_sprzedazy": (2, 99, "Pozycja sprzedaży", "ilość wydana, cena"),
    "pozycja_dostawy": (3, 99, "Pozycja dostawy", "ilość przyjęta"),
    "produkt": (None, 24, "Produkt", "nazwa, odmiana, jednostka"),
    "cena_produktu": (1, -47, "Cena produktu", "cena, data początku"),
    "plan_dostawy": (3, -47, "Plan dostawy", "dzień, ilość"),
}

# Podpis klucza obcego w języku sklepu. W modelu logicznym linia nosi
# rzeczywistą nazwę kolumny pobraną razem z licznością z metadanych MySQL.
OPISY = {
    ("profil_klienta", "uzytkownik_id"): "dane klienta",
    ("rozliczenie_zaleglosci", "zarejestrowal_id"): "rejestruje rozliczenie",
    ("rozliczenie_zaleglosci", "klient_id"): "dłużnik",
    ("rezerwacja", "klient_id"): "składa",
    ("sprzedaz", "sprzedawca_id"): "obsługuje",
    ("sprzedaz", "rezerwacja_id"): "odbiór",
    ("dostawa", "zarejestrowal_id"): "przyjmuje",
    ("ubytek", "zarejestrowal_id"): "rejestruje",
    ("korekta_stanu", "zarejestrowal_id"): "wpisuje różnicę",
    ("pozycja_rezerwacji", "rezerwacja_id"): "zawiera",
    ("pozycja_sprzedazy", "sprzedaz_id"): "zawiera",
    ("pozycja_dostawy", "dostawa_id"): "zawiera",
    ("pozycja_rezerwacji", "produkt_id"): "towar zamówiony",
    ("pozycja_sprzedazy", "produkt_id"): "towar wydany",
    ("pozycja_dostawy", "produkt_id"): "towar przyjęty",
    ("ubytek", "produkt_id"): "towar utracony",
    ("korekta_stanu", "produkt_id"): "towar przeliczony",
    ("cena_produktu", "produkt_id"): "historia cen",
    ("plan_dostawy", "produkt_id"): "planowana ilość",
}


def polozenie_x(kolumna):
    if kolumna is None:
        return sum(SZEROKOSCI) / 2
    return sum(SZEROKOSCI[:kolumna]) + SZEROKOSCI[kolumna] / 2


def etykieta(tytul, opis, pas):
    if pas:
        def porty(prefiks):
            return "".join(f'<TD PORT="{prefiks}{i}" WIDTH="{szerokosc}" HEIGHT="1"></TD>'
                           for i, szerokosc in enumerate(SZEROKOSCI))

        return (f'<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0" CELLPADDING="0" BGCOLOR="#184e43">'
                f'<TR>{porty("k")}</TR><TR><TD COLSPAN="6" HEIGHT="22">'
                f'<FONT COLOR="white"><B>{tytul}</B>  ·  {opis}</FONT></TD></TR>'
                f'<TR>{porty("d")}</TR></TABLE>>')
    return (f'<<TABLE BORDER="1" COLOR="#779d92" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" BGCOLOR="#f1f6f3">'
            f'<TR><TD><B>{tytul}</B></TD></TR><TR><TD><FONT POINT-SIZE="11">{opis}</FONT></TD></TR></TABLE>>')


def koniec(tabela, drugi):
    kolumna, y, *_ = ENCJE[tabela]
    kolumna2, y2, *_ = ENCJE[drugi]
    if tabela in ("auth_user", "produkt"):
        return f'{tabela}:{"k" if y2 > y else "d"}{kolumna2}:{"n" if y2 > y else "s"}'
    if y == y2:
        return f'{tabela}:{"e" if kolumna2 > kolumna else "w"}'
    return f'{tabela}:{"n" if y2 > y else "s"}'


def rysuj(plik, kolumny, fk, klucze, koncept=False):
    dot = ['digraph G { graph [margin=0, pad=0.03, splines=line, outputorder=edgesfirst, bgcolor="white"];',
           'node [shape=plain, fontname="DejaVu Sans", fontsize=12];',
           'edge [dir=both, arrowsize=0.70, penwidth=1.15, color="#45655c", '
           'fontname="DejaVu Sans", fontsize=11, fontcolor="#243f37"];']
    for tabela, (x, y, nazwa, opis) in ENCJE.items():
        if koncept and tabela == "auth_user_groups":
            continue
        if not koncept:
            nazwa = tabela
            opis = "PK " + ", ".join(klucze[tabela]["PRIMARY"])
        label = etykieta(html.escape(nazwa), html.escape(opis), tabela in ("auth_user", "produkt"))
        dot.append(f'{tabela} [pos="{polozenie_x(x)},{y}!", label={label}];')

    def linia(rodzic, dziecko, podpis, poczatek, koniec_linii):
        dot.append(f'{koniec(rodzic, dziecko)} -> {koniec(dziecko, rodzic)} '
                   f'[arrowtail={poczatek}, arrowhead={koniec_linii}];')
        xr, yr, *_ = ENCJE[rodzic]
        xd, yd, *_ = ENCJE[dziecko]
        if yr == yd:
            x = (polozenie_x(xr) + polozenie_x(xd)) / 2
            y = yr if dziecko == "auth_user_groups" else yr + 28
        else:
            x = polozenie_x(xr if dziecko in ("auth_user", "produkt") else xd)
            y = (yr + yd) / 2
        dot.append(f'opis_{rodzic}_{dziecko} [pos="{x},{y}!", '
                   f'label="{podpis}", fontsize=11.5, fontcolor="#243f37", style=filled, fillcolor="white"];')

    for (tabela, pole), (cel, _) in sorted(fk.items()):
        if tabela not in ENCJE or (koncept and tabela == "auth_user_groups"):
            continue
        pusty = next(puste for nazwa, _, puste, _ in kolumny[tabela] if nazwa == pole)
        jedna = [pole] in klucze[tabela].values()
        liczba_dzieci = "teeodot" if jedna else "crowodot"
        if koncept and (tabela, pole) in (("pozycja_rezerwacji", "rezerwacja_id"),
                                         ("pozycja_sprzedazy", "sprzedaz_id")):
            liczba_dzieci = "crowtee"
        linia(cel, tabela, OPISY[tabela, pole] if koncept else pole,
              "teeodot" if pusty else "teetee", liczba_dzieci)
    if koncept:
        linia("auth_group", "auth_user", "rola konta", "teetee", "crowodot")
    dot.append("}")
    subprocess.run(["neato", "-n2", "-Tpdf", "-o", str(plik)],
                   input="\n".join(dot), text=True, check=True)
