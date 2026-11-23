"""Rysuj przekroje klas z zarejestrowanych modeli Django (w środowisku aplikacji)."""

import os
import subprocess
import sys
from html import escape
from pathlib import Path

import django
from django.apps import apps

KATALOG = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KATALOG.parents[2] / "aplikacja"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


# Identyfikatory klas wybierają przypadek użycia, a pola i asocjacje pochodzą z ORM.
WIDOKI = {
    "klasy-modele-orm": (
        "auth.User", "konta.ProfilKlienta", "rezerwacje.Rezerwacja",
        "rezerwacje.PozycjaRezerwacji", "magazyn.Sprzedaz", "magazyn.Produkt",
        "rozliczenia.RozliczenieZaleglosci",
    ),
    "klasy-magazyn": (
        "magazyn.Produkt", "magazyn.CenaProduktu", "magazyn.PlanDostawy", "magazyn.Dostawa",
        "magazyn.PozycjaDostawy", "magazyn.Sprzedaz", "magazyn.PozycjaSprzedazy",
        "magazyn.Ubytek", "magazyn.KorektaStanu",
    ),
}


def renderuj(nazwa, etykiety):
    modele = [apps.get_model(etykieta) for etykieta in etykiety]
    kierunek = "LR" if nazwa == "klasy-magazyn" else "TB"
    fragmenty = [
        'digraph klasy {',
        f'graph [rankdir={kierunek}, bgcolor="white", nodesep=0.2, ranksep=0.55, pad=0.06];',
        'node [shape=plain, fontname="DejaVu Sans", fontsize=10];',
        'edge [fontname="DejaVu Sans", fontsize=9, color="#516E69", arrowhead=none];',
    ]
    for model in modele:
        meta = model._meta
        fragmenty.extend([
            f'{meta.object_name} [label=<<TABLE BORDER="1" CELLBORDER="0" '
            'CELLSPACING="0" CELLPADDING="4" BGCOLOR="#F8FBF9" COLOR="#99B3AF">',
            f'<TR><TD ALIGN="LEFT" BGCOLOR="#E1EFEC"><FONT POINT-SIZE="9">'
            f'{meta.app_label}</FONT><BR ALIGN="LEFT"/><B>{meta.object_name}</B></TD></TR>',
        ])
        for pole in meta.concrete_fields:
            if pole.is_relation or pole.primary_key or (meta.label == "auth.User" and pole.name not in {"username", "email"}):
                continue
            fragmenty.append(f'<TR><TD ALIGN="LEFT">{escape(pole.name)}'
                             f' : {escape(pole.get_internal_type())}</TD></TR>')
        fragmenty.append('</TABLE>>];')
        for pole in meta.concrete_fields:
            if pole.is_relation and pole.related_model in modele:
                rodzic = pole.related_model._meta.object_name
                liczba = "0..1" if pole.one_to_one else "*"
                fragmenty.append(f'{rodzic} -> {meta.object_name} [headlabel="{liczba}", '
                                 f'taillabel="{"0..1" if pole.null else "1"}", labeldistance=1.8];')
    fragmenty.append('}')
    subprocess.run(["dot", "-Tpdf", "-o", str(KATALOG / f"{nazwa}.pdf")],
                   input="\n".join(fragmenty), text=True, check=True)


if __name__ == "__main__":
    django.setup()
    for nazwa, etykiety in WIDOKI.items():
        renderuj(nazwa, etykiety)
