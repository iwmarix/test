# Analiza ujęć do personalizacji panoramy

Materiał źródłowy: dwa podglądowe rendery MP4 dostarczone 2026-07-17
(`ujecia/WANDA1_panorama_1.mp4`, `ujecia/WANDA1_panorama_2.mp4`).
Klatki referencyjne: `ujecia/klatki/` (pomniejszone do 960 px).

## Parametry techniczne

| | Ujęcie 1 | Ujęcie 2 |
|---|---|---|
| Plik | WANDA1_panorama_1.mp4 | WANDA1_panorama_2.mp4 |
| Rozdzielczość | 1920×1080 (HEVC, yuv420p) | 1920×1080 (HEVC, yuv420p) |
| Klatkaż | 24 fps | 24 fps |
| Długość | 8,875 s (213 kl.) | 13,542 s (325 kl.) |
| Łącznie do renderu per miasto | | **~22,4 s (538 klatek)** |

Uwaga: to spłaszczone podglądy — do pipeline'u potrzebny jest warstwowy
projekt AE (patrz „Konsekwencje").

## Opis ujęć

**Ujęcie 1** — plan ogólny z poziomu parku: jezioro z liliami, kaczki, alejki,
ściana drzew; panorama miasta widoczna w **prześwicie między koronami drzew,
góra-środek kadru** (orientacyjnie x≈650–1400, y≈150–360 przy 1920×1080).
Kamera wykonuje powolną jazdę w głąb parku — w końcówce ujęcia kadr wchodzi
między drzewa i **panorama znika całkowicie** (ostatnie klatki z motion blur,
bez panoramy).

**Ujęcie 2** — długie ujęcie rozwijające się: start z lotu ptaka nad parkiem,
panorama miasta na horyzoncie **przez całą szerokość kadru**, nad koronami
drzew, z warstwą mgiełki/atmosfery u podstawy zabudowy. Kamera opada i jedzie
do przodu, kończąc na planie z poziomu ziemi: postacie (tata z dziećmi,
hulajnoga, piesek, fioletowy balonik, rower przy drzewie), a panorama nadal
widoczna w prześwicie za drzewami. Przez kadr przelatuje **klucz gęsi — część
ptaków przelatuje NA TLE panoramy** (przed nią).

Światło: ujęcie 1 — ciepłe, dzienne; ujęcie 2 — cieplejsze, „złota godzina",
różowe chmury. Panoramy per miasto muszą znieść oba gradingi.

## Konsekwencje dla pipeline'u

1. **Kamera się porusza w obu ujęciach** (jazda, opadanie, paralaksa) —
   panoramy NIE da się podmienić jako statycznej łatki na wideo. Podmiana musi
   nastąpić **wewnątrz kompozycji AE**: plansza (plate) panoramy podpięta pod
   ruch kamery kompozycji. To potwierdza przyjętą architekturę (szablon AE +
   slot na stałej ścieżce) i **wyklucza drogę „inpainting na gotowym wideo"**.
2. **Okluzje przed panoramą**: korony drzew (oba ujęcia), mgiełka/atmosfera
   u podstawy miasta, ptaki lecące przed panoramą, balonik przy lewej krawędzi
   (uj. 2). Kolejność warstw w AE musi być: niebo → **plansza panoramy** →
   mgiełka → drzewa/park → ptaki/postacie. **Wymaga warstwowego projektu AE
   ze studia** — dostarczone MP4 są spłaszczone; bez projektu warstwowego
   doszłaby kosztowna rotoskopia ptaków i krawędzi drzew.
3. **Jedna plansza panoramy na miasto obsłuży oba ujęcia** — miasto jest
   odległe, więc zmiana wysokości kamery minimalnie zmienia jego perspektywę;
   w obu ujęciach panorama funkcjonuje jako daleki plan. Plansza musi być
   **szersza niż kadr** (rekomendacja: ≥3000 px szerokości, z pasem zapasu
   dołem pod linię drzew), bo ruch kamery przesuwa widoczny wycinek.
4. **Neutralna plansza + grading w kompozycji**: różnice światła między
   ujęciami (dzień vs złota godzina) powinna załatwiać korekcja koloru nałożona
   na warstwę panoramy w każdej kompozycji, nie osobne plansze per ujęcie.
   Generujemy **jedną neutralną panoramę na miasto**, kompozycje ją barwią.
5. **Panel akceptacyjny**: podgląd zatwierdzanej panoramy trzeba pokazywać
   **w kontekście obu ujęć** (mockup klatki z uj. 1 i uj. 2), nie jako goły
   obraz — o akceptowalności decyduje wygląd w kadrze, za drzewami i mgiełką.
6. **Wolumen renderu AE**: 2 kompozycje / ~538 klatek na miasto (zamiast 1
   ujęcia) — czas renderu AE ×2 względem pierwotnego szacunku; bez wpływu na
   czas enkodowania DCP (fragment i tak wchodzi w całość filmu).
7. **Znikanie panoramy w końcówce uj. 1** to zaleta: naturalna granica cięcia
   fragmentu do podmiany w Resolve (koniec fragmentu w miejscu, gdzie panoramy
   już nie widać — szew niewidoczny).

## Do potwierdzenia ze studiem

- [x] ~~Czy istnieje warstwowy projekt AE obu ujęć z panoramą jako osobną
      warstwą/precompem?~~ **POTWIERDZONE 2026-07-17**: kompozycje AE
      z panoramą za drzewami jako osobną warstwą istnieją (autor: Maciek).
      Warunek konieczny pipeline'u spełniony — bez rotoskopii.
- [ ] Rozdzielczość i przestrzeń barwna finalnego mastera (podglądy są
      1920×1080; DCP flat to 1998×1080 — co jest źródłem?)
- [ ] Czy odbicie panoramy pojawia się w wodzie jeziora w którymkolwiek
      ujęciu w pełnej jakości (w podglądach niewidoczne, ale do weryfikacji
      na projekcie warstwowym)?
- [ ] Timecode'y obu ujęć w masterze filmu (do konformu w Resolve).

## Stan prac (2026-07-17)

**Wstrzymane na kilka dni** — studio przygotowuje wzorcową maskę i plik AE;
trwają testy, czy podkładanie panoramy dobrze wygląda w ruchu. Implementacja
(Faza 1) ruszy po otrzymaniu materiałów.

### Na co patrzeć przy testach ruchu (typowe miejsca „pękania" podmiany)

- **Paralaksa na krawędziach** — czy panorama przesuwa się odrobinę wolniej
  niż korony drzew (miasto jest dalej); jeśli plansza jest przypięta na
  sztywno do drzew, ruch zdradzi podmianę.
- **Dryf skali w uj. 2** — przy opadaniu kamery miasto nie powinno zauważalnie
  rosnąć/maleć (jest daleko); jeśli rośnie, plansza wisi za blisko kamery
  w przestrzeni 3D kompozycji.
- **Mgiełka u podstawy zabudowy** — czy leży NAD warstwą panoramy i czy
  zlewa się z nią tak samo w całym przebiegu ujęcia.
- **Ptaki i balonik** — czy zawsze renderują się przed panoramą (kolejność
  warstw stała w czasie).
- **Sklejka z gradingiem** — podgląd obu ujęć z tą samą planszą: dzień
  (uj. 1) i złota godzina (uj. 2); plansza neutralna powinna znieść oba.
- **Końcówka uj. 1** — moment znikania panoramy za drzewami: żadnych
  prześwitów planszy między liśćmi przy motion blur.

## Do pozyskania od Maćka (specyfikacja warstwy panoramy)

- [ ] Wymiary planszy panoramy w px i jej pozycja/skala w obu kompozycjach
      (czy jedna warstwa/precomp jest współdzielona przez oba ujęcia?).
- [ ] Eksport obecnej planszy Warszawy jako PNG w pełnej rozdzielczości —
      posłuży jako wzorzec formatu (rozmiar, linia horyzontu, strefa krycia
      drzewami) i referencja stylu dla generowania pozostałych miast.
- [ ] Czy warstwa panoramy ma stałą interpretację koloru (sRGB/ACES?) —
      żeby wygenerowane plansze wpinały się bez przesunięć barwnych.
- [ ] Zgoda na drobną modyfikację projektu: przepięcie źródła warstwy na
      stały plik `work/current_panorama.png` (slot pipeline'u).
