---
name: budzet
description: Tworzy budżet produkcji filmowej/animowanej w układzie zgodnym z kosztorysami PISF, wyprowadzony z breakdownu. Użyj po /breakdown, gdy potrzebny jest kosztorys do wniosku lub planowania.
---

# Budżet produkcji

Cel: kosztorys wyprowadzony z liczb z breakdownu (metraż, sceny, postacie, światy, piosenki). Wynik zapisz w `projekty/<projekt>/budzet/` jako `budzet.md` + `budzet.csv` (do importu w arkuszu).

## Zasady

1. **Najpierw tabela "Założenia"**: metraż filmu (min), technika (2D/3D/mieszana), stawki bazowe (koszt/min animacji wg złożoności, dniówki, wyceny piosenek). Każda stawka to jawne założenie `[do weryfikacji]` — użytkownik kalibruje. NIE podawaj kwot jako pewników.
2. **Kosztorys w układzie grup PISF** (produkcja animowana):
   - I. Prawa i scenariusz (opcja/zakup praw, scenariusz, konsultacje, tłumaczenia)
   - II. Development / projekty plastyczne (character design, projekty lokacji/światów, colorscript, bible projektu)
   - III. Preprodukcja (storyboard, animatik, layout, casting głosowy, nagrania dialogów referencyjnych)
   - IV. Produkcja animacji (modele/rigi lub setup 2D, tła, animacja właściwa wg min i kategorii złożoności, efekty, kompozycja, render)
   - V. Muzyka i dźwięk (kompozycja piosenek + podkład, nagrania wokalne, sound design, zgranie/mix)
   - VI. Postprodukcja (montaż, korekcja barwna, napisy, DCP/mastery, wersje językowe)
   - VII. Ekipa i koszty osobowe (reżyser, producent, kierownik produkcji — jeśli nie ujęci wyżej)
   - VIII. Koszty ogólne i rezerwa (ZAiKS/licencje, księgowość, ubezpieczenia, rezerwa 5–10%)
   - IX. Promocja i dystrybucja (jeśli wniosek tego wymaga)
3. **Animację wyceniaj od metrażu i złożoności**: podziel sceny z breakdownu na kategorie A (dialog, mało ruchu), B (standardowa akcja), C (sekwencje złożone: symulacje, tłumy, transformacje, teledyski) i przypisz różne stawki/min.
4. Piosenki licz osobno: kompozycja + tekst + aranż + nagranie + prawa, plus animacja teledysku w kategorii C.
5. Podaj strukturę finansowania tylko jeśli użytkownik poprosi (wkład własny, PISF — sprawdź aktualne progi w Programach Operacyjnych PISF na dany rok, koproducenci).

## Format CSV

`grupa;pozycja;jednostka;ilość;stawka;kwota;uwagi` — kwoty jako formuły ilość×stawka policzone, stawki `[do weryfikacji]` w uwagach.
