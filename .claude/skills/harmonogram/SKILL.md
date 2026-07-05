---
name: harmonogram
description: Tworzy harmonogram produkcji filmu/animacji z podziałem na etapy i kamienie milowe, wyprowadzony z breakdownu. Użyj po /breakdown, równolegle lub po /budzet.
---

# Harmonogram produkcji

Cel: realny plan czasowy z kamieniami milowymi. Wynik: `projekty/<projekt>/harmonogram/harmonogram.md` (+ opcjonalnie wykres Gantta w Mermaid).

## Zasady

1. Wyprowadzaj czasy z liczb breakdownu: metraż animacji, liczba assetów (postacie × warianty, lokacje/światy), liczba piosenek. Tempo produkcji animacji podawaj jako jawne założenie (np. sekund animacji/tydzień/animator `[do weryfikacji]`) i pokaż wyliczenie.
2. **Etapy dla animacji** (typowa kolejność, częściowo równoległe):
   - Development: finalny scenariusz, projekty plastyczne, colorscript
   - Preprodukcja: storyboard → animatik (lock), casting i nagranie dialogów (w animacji dialogi nagrywa się PRZED animacją), demo piosenek
   - Produkcja assetów: postacie (modele/rigi/turnaroundy), lokacje, rekwizyty
   - Animacja: shoty wg sekwencji, od najtrudniejszych (kategoria C) — one niosą największe ryzyko
   - Efekty, kompozycja, render
   - Dźwięk: finalne nagrania piosenek, sound design, zgranie
   - Postprodukcja: montaż online, korekcja, mastery
3. Dla live-action zamiast tego: okres zdjęciowy z planem dni zdjęciowych (grupuj sceny po lokacjach, nie po kolejności fabularnej).
4. Każdy etap: czas trwania, zależności, kamień milowy (co jest "gotowe"), ryzyka.
5. Mermaid Gantt: sekcje = etapy, użyj dat względnych od startu podanego przez użytkownika (jeśli brak — oznacz T0 i pytaj tylko wtedy, gdy data jest niezbędna).
