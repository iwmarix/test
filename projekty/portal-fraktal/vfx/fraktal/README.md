# Portal fraktalny — scena Mandelbulber 2

Wzór na sufit/portal, wzorowany na referencji: koncentryczne, organiczne
warstwice z bąblami, szklisty materiał, zimna tonacja.

## Pliki

| Plik | Co to |
|---|---|
| `portal_v01.fract` | scena Mandelbulbera — **czysty tekst, wersjonuje się w git** |
| `render.sh` | render podglądu / finału / sweepów / animacji |
| `render/portal_v01_podglad.png` | aktualny stan wzoru (1280×720) |

## Jak renderować

```bash
./render.sh podglad                    # 960x540 PNG, ~30 s na 4 rdzeniach
./render.sh final                      # 1920x1080 EXR
GPU=-g ./render.sh final               # to samo na GPU (OpenCL), dużo szybciej
./render.sh sweep fov 1.0 1.25 1.5     # seria wariantów jednego parametru
./render.sh anim 0 96                  # sekwencja klatek animacji keyframe
```

Wymaga Mandelbulbera 2 (`mandelbulber2` w PATH). Pobranie: https://mandelbulber.com

## Jak działa ta scena — trzy rzeczy, które robią ten wzór

**1. Fraktal ścięty do płaskiej płyty.**
```
limits_enabled true;
limit_min -200 -200 -0.015;
limit_max  200  200  0.015;
```
Bez tego Kaliset rozrasta się w bryłę i czyta się jak krajobraz. Przycięcie do
płyty grubości 0,03 daje płaski wzór oglądany od przodu.

**2. Kamera prostopadle do płyty.** `camera 0.02 -0.06 5.2`, `target 0.02 -0.06 0`.
Patrzenie wzdłuż osi Z zamienia krajobraz w mandalę.

**3. Warstwice to paleta, nie geometria.**
Zagnieżdżone pasy powstają z mapowania palety kolorów na liczbę iteracji.
Ustawienie `mat1_use_colors_from_palette=0` **kasuje cały wzór** i zostaje płaski
dysk — sprawdzone. Kolor studzi się przez `saturation`, `main_light_colour`
i grade w kompozycji, nie przez wyłączenie palety.

## Parametry do kręcenia

| Parametr | Co zmienia | Zakres |
|---|---|---|
| `fov` | ile pierścieni w kadrze | 0.8–1.6 |
| `camera` / `target` (Z) | zagęszczenie wzoru | 3–8 |
| `fractal1_IFS_scale` | charakter struktury | 1.8–3.4 |
| `fractal1_transf_constant_julia_c` | kształt centrum; `0 Y 0` zachowuje symetrię lewo-prawo | Y: −1…1 |
| `saturation` | nasycenie | 0.2–0.6 |
| `main_light_colour` | temperatura światła | hex 16-bit |
| `DE_factor` | jakość vs czas (mniej = lepiej/wolniej) | 0.05–0.2 |

Sweep dowolnego z nich: `./render.sh sweep <klucz> <wartości...>`

## Stan: czego jeszcze brakuje do referencji

- [ ] **Symetria lustrzana** — referencja jest symetryczna lewo-prawo, ta scena
      jeszcze nie. Kierunek: `julia_c` z zerem w X + kamera dokładnie na osi.
- [ ] **Charakter labiryntowy** — referencja ma bardziej kanciaste, rozgałęzione
      pasy; tu są gładsze, falowe. Do sweepu: `IFS_direction_*`, `IFS_scale`.
- [ ] **Refrakcja lasu** — w referencji przez wzór prześwituje las. W Mandelbulberze
      robi się to przez `textured_background true` + `file_background <plate>`.
      Potrzebna klatka lasu.
- [ ] **Wtopienie w plate** — mgła, snop światła, aberracja, ziarno. To robota
      w kompozycji (AE), nie w Mandelbulberze.

## Uwaga o wersji

Scena rozwijana na Mandelbulberze **2.20**. Nowsze wersje czytają ją bez problemu,
ale parametry dodane po 2.20 nie zadziałają wstecz.
