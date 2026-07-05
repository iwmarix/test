---
name: breakdown
description: Tworzy pełny breakdown scenariusza — sceny, postacie, lokacje/światy, rekwizyty, efekty specjalne, piosenki. Użyj po zaimportowaniu scenariusza, przed budżetem i harmonogramem.
---

# Breakdown scenariusza

Cel: rozbić scenariusz na elementy produkcyjne. Pracuj na `projekty/<projekt>/scenariusz/scenariusz.txt` — przeczytaj CAŁY tekst, nie tylko nagłówki.

## Produkty (zapisz w `projekty/<projekt>/breakdown/`)

1. **`breakdown-scen.md`** — tabela wszystkich scen:
   | Nr | Lokacja | INT/EXT | Pora | Postacie | Kluczowe rekwizyty/elementy | Efekty / uwagi animacyjne |
   Po tabeli: sekcja "Sekwencje złożone" z omówieniem scen wymagających szczególnej uwagi (efekty, tłumy, piosenki, symulacje).
2. **`postacie.md`** — każda postać: opis z scenariusza, rola (główna/drugoplanowa/epizod), liczba scen, w których występuje, wymagania designu (dla animacji: warianty kształtu/koloru, rigi specjalne), potrzeby castingu głosowego.
3. **`lokacje.md`** — lokacje/światy: opis, liczba scen, wymagane assety tła, warianty oświetlenia (dzień/noc), skala trudności.
4. **`piosenki.md`** (jeśli są) — wstawki muzyczne: miejsce w scenariuszu, długość, wykonawcy, temat, konsekwencje produkcyjne.

## Metoda

- Sceny licz po nagłówkach `^\d+ +(EXT|INT)`. Postacie wykrywaj po liniach wersalikami przed dialogiem, ale weryfikuj czytając didaskalia (postacie nieme, np. pojazdy/przedmioty ożywione, nie mają dialogów wersalikami).
- Dla animacji w kolumnie "Efekty" odnotowuj: transformacje postaci, symulacje (papier, woda, tkaniny, śnieg), efekty świetlne, tłumy/multiplikacje, odbicia, teatr cieni, lewitacje, przejścia między światami.
- Na końcu podaj liczby zbiorcze: sceny, lokacje unikalne, postacie mówiące/nieme, piosenki, szacowany metraż (sceny dialogowe ~1 min/str., akcja wg opisu).
- Te liczby są wejściem do `/budzet` i `/harmonogram`.
