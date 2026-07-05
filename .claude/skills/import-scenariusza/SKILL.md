---
name: import-scenariusza
description: Wczytuje scenariusz z pliku .doc/.docx/.pdf, konwertuje do czystego tekstu UTF-8 i zakłada strukturę projektu. Użyj, gdy użytkownik podaje nowy scenariusz lub prosi o rozpoczęcie nowego projektu filmowego.
---

# Import scenariusza

Cel: przekształcić plik scenariusza w czysty tekst i założyć folder projektu.

## Kroki

1. Ustal ścieżkę pliku wejściowego (upload użytkownika lub plik w repo) i nazwę projektu (slug z tytułu, np. `wanda-i-jej-banda-2`).
2. Konwersja zależnie od formatu:
   - **.doc (binarny OLE2)**: `pip install olefile`, potem `python3 narzedzia/extract_doc.py wejscie.doc wyjscie.txt`. LibreOffice często nie radzi sobie z plikami z Maca (code page 10029) — skrypt czyta piece table i zachowuje polskie znaki.
   - **.docx**: `soffice --headless --convert-to txt:Text` lub python-docx.
   - **.pdf**: `pdftotext -layout`.
3. Załóż strukturę: `projekty/<slug>/{scenariusz,breakdown,budzet,harmonogram,vfx,koncepty}/`.
4. Zapisz do `projekty/<slug>/scenariusz/`: oryginał + `scenariusz.txt`.
5. Zweryfikuj jakość ekstrakcji: sprawdź polskie znaki, policz sceny (`grep -cE '^[0-9]+ +(EXT|INT)'`), wypisz nagłówki scen i listę postaci (linie wersalikami).
6. Podsumuj użytkownikowi: tytuł, autor, liczba scen, format (live-action / animacja), wykryte postacie — i zaproponuj `/breakdown` jako następny krok.

## Uwagi

- Wersaliki z polskimi znakami: używaj klasy `[A-ZĄĆĘŁŃÓŚŹŻ]` w grep.
- Jeśli scenariusz zawiera wstawki muzyczne ("WCHODZI TELEDYSK", piosenki) — odnotuj je, mają duży wpływ na budżet (kompozycja, nagranie, dodatkowa animacja).
