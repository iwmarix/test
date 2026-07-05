---
name: koncept-art
description: Tworzy concept art, moodboardy, briefy VFX i prewizualizacje z użyciem narzędzi AI (Adobe/Firefly MCP i inne). Użyj gdy potrzebne są materiały wizualne — projekty postaci, światów, shot listy efektów, animatiki.
---

# Koncept art i efekty z narzędziami AI

Cel: materiały wizualne do developmentu i preprodukcji. Wyniki zapisuj w `projekty/<projekt>/koncepty/` (obrazy + `README.md` z opisem, promptami i wersjami) oraz briefy w `projekty/<projekt>/vfx/`.

## Dostępne narzędzia (sprawdź ToolSearch przed użyciem)

- **Adobe (MCP `Adobe_for_creativity`)**: edycja obrazów (usuwanie tła, generative expand/fill, selekcje po promptach, kolory, blur, ziarno, wektoryzacja), `animate_design` (animacja projektu), `video_render`/`video_render_frame`, wyszukiwanie assetów stockowych, Firefly boards (moodboardy: `create_firefly_board`, `boards_add_items_to_board`).
- **Figma (MCP `Figma`)**: diagramy (np. mapa światów, struktura sekwencji), plansze prezentacyjne.
- Do generowania obrazów od zera — jeśli w sesji brak generatora, przygotuj gotowe prompty (PL + EN) do użycia w Firefly/Midjourney i zapisz je w `koncepty/prompty.md`.

## Workflow

1. **Moodboard**: na podstawie breakdownu zbierz kierunki wizualne per świat/lokacja (paleta, faktury, referencje). Utwórz Firefly board lub plik markdown z opisami i promptami.
2. **Projekty postaci**: dla każdej postaci z `postacie.md` — brief designu (sylwetka, paleta, materiał/faktura, warianty i transformacje wymagane przez scenariusz) + prompty generacyjne.
3. **Briefy VFX/animacji specjalnej**: dla scen kategorii C z breakdownu — opis efektu, referencje, proponowana technika (symulacja/2D FX/kompozycja), szacunek trudności (S/M/L/XL).
4. **Prewizualizacja/animatik**: sekwencje obrazów → animacja (Adobe `animate_design`/`video_render`) lub eksport plansz do Adobe Express.

## Zasady

- Materiały AI = referencja/prewizualizacja, NIE finalne assety. Oznaczaj pliki `koncept-ai-*`.
- Zachowuj prompty i parametry przy każdym obrazie — powtarzalność ma znaczenie.
- Styl dla produkcji dziecięcych: sprawdź w breakdownie grupę docelową i utrzymuj spójny, bezpieczny ton.
- Prawa: materiały generowane AI we wnioskach PISF i materiałach promocyjnych oznaczaj zgodnie z wymogami instytucji `[do weryfikacji z prawnikiem produkcji]`.
