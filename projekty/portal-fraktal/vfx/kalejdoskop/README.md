# Portal kalejdoskopowy — fraktalne pogięcie obrazu

Skrypt: `narzedzia/portal_kalejdoskop.py`

Nie renderuje geometrii fraktalnej. Gnie **współrzędne obrazu** tą samą
matematyką co Kaliset (składanie `abs` + obrót + skala) i pogiętymi
współrzędnymi próbkuje zdjęcie. Efekt: komórki wypełnione odbitym lustrzanie
lasem, obrysowane szklistymi krawędziami.

## Użycie

```bash
# z własnym zdjęciem (zalecane)
python3 narzedzia/portal_kalejdoskop.py --plate las.jpg -W 1920 -H 1080 --out portal.png

# bez zdjęcia — zastępczy las proceduralny
python3 narzedzia/portal_kalejdoskop.py --out portal.png
```

Render 1280×720 trwa ~1 s, więc sweepy parametrów są darmowe.

## Parametry

| Flaga | Co robi | Zakres |
|---|---|---|
| `--iter` | liczba złożeń — więcej = drobniejszy wzór | 5–12 |
| `--scale` | skala po złożeniu — steruje wielkością komórek | 1.1–2.0 |
| `--rot` | obrót między złożeniami — zmienia symetrię | 0.1–1.0 |
| `--inwersja` | inwersja sferyczna; 0 = wyłączona (mniej „tunelowo") | 0–0.5 |
| `--texskala` | ile źródła widać w komórce — **małe = las nieczytelny** | 0.3–1.5 |
| `--pasy` | gęstość warstwic na szkle | 6–16 |
| `--szklo` | siła szklanych krawędzi i specularu | 0.5–2.0 |
| `--zoom` | kadrowanie | 0.6–1.3 |
| `--winieta` | przyciemnienie brzegów | 0–0.5 |

Ustawienia użyte do `portal_kalejdoskop_v1.png`:
`--iter 7 --scale 1.30 --rot 0.20 --inwersja 0 --texskala 0.7 --pasy 9 --zoom 0.95 --szklo 1.35 --winieta 0.30`

## Stan

Trafione: charakter komórek, symetria lustrzana, szkliste obrysy, zimna tonacja.

Do poprawy:
- wzór jest równomierny na całym kadrze; referencja ma **wyraźny portal w centrum**
  wygasający ku krawędziom — do zrobienia przez maskę radialną mieszającą wzór z plate'em
- las w komórkach rozpoznawalny słabo — poprawi się od razu po podaniu
  `--plate` z prawdziwym zdjęciem zamiast źródła proceduralnego
