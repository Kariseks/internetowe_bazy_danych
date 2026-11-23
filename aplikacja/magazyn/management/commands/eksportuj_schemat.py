"""Odtwórz DDL i diagramy z metadanych MySQL po migracji."""
import html
import re
import subprocess
from collections import defaultdict
from graphlib import TopologicalSorter
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor


# Podział wydruku na obszary. Do każdego dodawane są końce relacji obcych.
OBSZARY = {
    "rezerwacje": {"rezerwacja", "pozycja_rezerwacji", "sprzedaz", "pozycja_sprzedazy"},
    "magazyn": {"dostawa", "pozycja_dostawy", "ubytek", "korekta_stanu"},
    "asortyment": {"produkt", "cena_produktu", "plan_dostawy"},
    "rozliczenia": {"auth_user", "auth_group", "auth_user_groups", "profil_klienta", "rozliczenie_zaleglosci"},
}
NAZWY = {
    "auth_user": "Konto", "auth_group": "Rola", "auth_user_groups": "Przypisanie roli",
    "profil_klienta": "Profil klienta", "rozliczenie_zaleglosci": "Rozliczenie zaległości",
    "produkt": "Produkt", "cena_produktu": "Cena produktu", "plan_dostawy": "Plan dostawy",
    "rezerwacja": "Rezerwacja", "pozycja_rezerwacji": "Pozycja rezerwacji",
    "sprzedaz": "Sprzedaż", "pozycja_sprzedazy": "Pozycja sprzedaży", "dostawa": "Dostawa",
    "pozycja_dostawy": "Pozycja dostawy", "ubytek": "Ubytek", "korekta_stanu": "Korekta stanu",
}


def wczytaj(kursor):
    kolumny = defaultdict(list)
    kursor.execute("""
        SELECT table_name, column_name, column_type, is_nullable, extra
        FROM information_schema.columns WHERE table_schema = DATABASE()
        ORDER BY table_name, ordinal_position
    """)
    for tabela, pole, typ, null, extra in kursor:
        kolumny[tabela].append((pole, typ, null == "YES", "GENERATED" in extra.upper()))
    kursor.execute("""
        SELECT table_name, column_name, referenced_table_name, referenced_column_name
        FROM information_schema.key_column_usage
        WHERE table_schema = DATABASE() AND referenced_table_name IS NOT NULL
        ORDER BY table_name, column_name
    """)
    fk = {(tabela, pole): (cel, klucz) for tabela, pole, cel, klucz in kursor}
    kursor.execute("""
        SELECT table_name, index_name, column_name FROM information_schema.statistics
        WHERE table_schema = DATABASE() AND non_unique = 0
        ORDER BY table_name, index_name, seq_in_index
    """)
    klucze = defaultdict(lambda: defaultdict(list))
    for tabela, indeks, pole in kursor:
        klucze[tabela][indeks].append(pole)
    return kolumny, fk, klucze


def ddl(kursor, nazwy, fk, wersja):
    zaleznosci = {n: set() for n in nazwy}
    for (tabela, _), (cel, _) in fk.items():
        if cel != tabela:
            zaleznosci[tabela].add(cel)
    naglowek = (f"-- MySQL {wersja} • stan po migracjach Django\n"
                "-- Eksport definicji ze sklepu. Importować do osobnej, pustej bazy.\n"
                "-- Dane i liczniki rekordów pominięto.\nSET NAMES utf8mb4;\n")
    wynik = [naglowek]
    for tabela in TopologicalSorter({k: sorted(v) for k, v in zaleznosci.items()}).static_order():
        kursor.execute("SHOW CREATE TABLE " + connection.ops.quote_name(tabela))
        sql = kursor.fetchone()[1]
        # AUTO_INCREMENT za nawiasem zawiera kolejny numer w bieżącej bazie.
        wynik.append(re.sub(r"\bAUTO_INCREMENT=\d+\s+", "", sql) + ";\n")
    return "\n".join(wynik)


def karta(tabela, kolumny, indeksy, fk, skrot):
    kolor = "#44626a" if skrot else "#184e43"
    pola = []
    for pole, typ, pusty, wyliczany in kolumny:
        pk = pole in indeksy["PRIMARY"]
        if skrot and not pk:
            continue
        etykiety = []
        if pk:
            etykiety.append("PK")
        if (tabela, pole) in fk:
            etykiety.append("FK")
        if not pk and [pole] in indeksy.values():
            etykiety.append("UQ")
        if wyliczany:
            etykiety.append("ƒ")
        pola.append(
            f'<TR><TD ALIGN="LEFT"><FONT COLOR="#47645d">{"/".join(etykiety) or "&#160;"}</FONT></TD>'
            f'<TD ALIGN="LEFT">{html.escape(pole)}</TD><TD ALIGN="LEFT">'
            f'<FONT COLOR="#41525d">{html.escape(typ)}{" ?" if pusty else ""}</FONT></TD></TR>'
        )
    for nazwa, pola_indeksu in indeksy.items():
        if not skrot and nazwa != "PRIMARY" and len(pola_indeksu) > 1:
            pola.append('<TR><TD ALIGN="LEFT"><FONT COLOR="#47645d">UQ</FONT></TD>'
                        f'<TD ALIGN="LEFT" COLSPAN="2">{html.escape(", ".join(pola_indeksu))}</TD></TR>')
    return (f'<<TABLE BORDER="1" COLOR="#a9beb6" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4" BGCOLOR="#fafcfa">'
            f'<TR><TD ALIGN="LEFT" BGCOLOR="{kolor}" COLSPAN="3"><FONT COLOR="white">'
            f'<B>{html.escape(tabela)}</B></FONT></TD></TR>' + "".join(pola) + "</TABLE>>")


def diagram(plik, obszar, kolumny, fk, klucze, orientacja, koncept=False):
    relacje = [(t, p, cel, klucz) for (t, p), (cel, klucz) in fk.items() if t in obszar]
    tabele = obszar | {cel for _, _, cel, _ in relacje}
    dot = [f'digraph G {{ graph [charset="UTF-8", rankdir={orientacja}, margin=0, pad=0.07, '
           'nodesep=0.22, ranksep=0.5, splines=polyline, bgcolor="white"];',
           'node [shape=plain, fontname="DejaVu Sans", fontsize=10];',
           'edge [dir=both, arrowsize=0.75, penwidth=1.2, color="#527077"];']
    for tabela in sorted(tabele):
        if koncept:
            dot.append(f'"{tabela}" [label="{NAZWY[tabela]}", shape=box, style="rounded,filled", '
                       'fillcolor="#eef5f0", color="#779d92", margin="0.14,0.10"];')
        else:
            label = karta(tabela, kolumny[tabela], klucze[tabela], fk, tabela not in obszar)
            dot.append(f'"{tabela}" [label={label}];')
    for tabela, pole, cel, _ in relacje:
        unikalny = [pole] in klucze[tabela].values()
        pusty = next(c[2] for c in kolumny[tabela] if c[0] == pole)
        dot.append(f'"{cel}" -> "{tabela}" [arrowtail={"teeodot" if pusty else "teetee"}, '
                   f'arrowhead={"teeodot" if unikalny else "crowodot"}];')
    dot.append("}")
    subprocess.run(["dot", "-Tpdf", "-o", str(plik)], input="\n".join(dot), text=True, check=True)


class Command(BaseCommand):
    help = "Eksportuje DDL wszystkich tabel i wektorowe ERD sklepu z aktualnej bazy MySQL."

    def add_arguments(self, parser):
        parser.add_argument("--katalog", type=Path, default=settings.BASE_DIR.parent,
                            help="Katalog główny artefaktów (domyślnie katalog projektu).")

    def handle(self, *args, **options):
        if connection.vendor != "mysql":
            raise CommandError("Eksport DDL wymaga połączenia z bazą MySQL.")
        migracje = MigrationExecutor(connection)
        if migracje.migration_plan(migracje.loader.graph.leaf_nodes()):
            raise CommandError("Przed wykonaniem eksportu zastosuj migracje (manage.py migrate).")
        repo = options["katalog"]
        katalog_bazy = repo / "baza"
        katalog_rys = repo / "dokumentacja" / "rysunki" / "diagramy"
        katalog_bazy.mkdir(parents=True, exist_ok=True)
        katalog_rys.mkdir(parents=True, exist_ok=True)
        with connection.cursor() as kursor:
            kursor.execute("SELECT VERSION()")
            wersja = kursor.fetchone()[0]
            kolumny, fk, klucze = wczytaj(kursor)
            domena = set.union(*OBSZARY.values())
            brak = domena - kolumny.keys()
            if brak:
                raise CommandError("Brakuje tabel: " + ", ".join(sorted(brak)))
            sql = ddl(kursor, kolumny, fk, wersja)
        for nazwa, obszar in OBSZARY.items():
            orientacja = "LR" if nazwa == "magazyn" else "TB"
            diagram(katalog_rys / f"erd-{nazwa}.pdf", obszar, kolumny, fk, klucze, orientacja)
        diagram(katalog_rys / "erd-konceptualny.pdf", domena, kolumny, fk, klucze, "LR", koncept=True)
        (katalog_bazy / "schema.sql").write_text(sql, encoding="utf-8")
        self.stdout.write(f"MySQL {wersja} • {len(kolumny)} tabel • {len(fk)} kluczy obcych")
