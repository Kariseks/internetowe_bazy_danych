# Internetowe bazy danych — projekt

Dokumentacja i (później) aplikacja na przedmiot **Internetowe bazy danych**.

## Struktura

```
├── dokumentacja/          ← LaTeX (główna praca na razie)
│   ├── main.tex
│   ├── rozdzialy/         ← etapy wg wytycznych
│   └── figury/
├── materialy/             ← PDF-y prowadzącego (wytyczne)
├── PLAN.md                ← postępy i następne kroki
└── README.md
```

## Kompilacja dokumentacji

```bash
cd dokumentacja
latexmk -pdf -interaction=nonstopmode main.tex
# wynik: main.pdf
latexmk -c   # sprzątanie plików pomocniczych
```

Rysunki wrzucaj do `dokumentacja/figury/` i wstawiaj przez `\figura{plik.png}{podpis}`.

## Etapy (z wytycznych)

1. Przygotowanie i uzasadnienie / analiza
2. Faza projektowa
3. Implementacja i walidacja
4. Wdrożenie
5. Prezentacja i zaliczenie
