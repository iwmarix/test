# Personalizacja DCP — architektura systemu (ok. 200 kin)

Dokument koncepcyjny dla agenta/aplikacji automatyzującej przygotowanie ~200
spersonalizowanych kopii DCP filmu animowanego. Personalizacja dotyczy wyłącznie
ujęcia otwierającego (park + panorama miasta w tle). Wersja referencyjna: panorama
Warszawy.

Status: **propozycja architektury do akceptacji — przed implementacją**.

## Decyzje podjęte

- **2026-07-17 — DCP bez szyfrowania** (brak KDM). Konsekwencje: licencja easyDCP
  niepotrzebna; eksport przez Resolve Studio (natywnie) lub DCP-o-matic; upraszcza
  ingest w kinach i eliminuje cały wątek generowania/dystrybucji kluczy KDM.
- **2026-07-17 — personalizacja dotyczy DWÓCH ujęć** (nie jednego): otrzymano
  podglądy `WANDA1_panorama_1.mp4` (8,9 s) i `WANDA1_panorama_2.mp4` (13,5 s) —
  łącznie ~22,4 s / 538 klatek renderu AE na miasto. Kamera porusza się w obu
  ujęciach, przed panoramą są okluzje (drzewa, mgiełka, ptaki) — podmiana musi
  odbywać się na warstwie w projekcie AE, nie na gotowym wideo. Szczegóły:
  `analiza-ujec.md`.
- **2026-07-17 — wariant A: pełne DCP per kino** (kin będzie mniej niż 200).
  Konsekwencje: każde kino dostaje jedną samodzielną paczkę (najprostszy ingest);
  DCP-o-matic i podział na rolki niepotrzebne; trzeba zaplanować przestrzeń dyskową
  i czas enkodowania proporcjonalnie do finalnej liczby kin (~100–140 GB i ~1–2 h
  na kopię). Wariant B (OV+VF, §2) zostaje w dokumencie jako plan awaryjny, gdyby
  skala jednak urosła.

---

## 1. Czy to wykonalne przy użyciu Claude Code / Codex?

**Tak — cały kod da się wygenerować i utrzymywać w Claude Code.** Żaden element nie
wymaga technologii niedostępnej dla asystenta kodującego:

| Element | Technologia | Wykonalność |
|---|---|---|
| Orkiestrator + baza statusów | Python + SQLite | pełna |
| Import/eksport Excel | Python (openpyxl) | pełna |
| Generowanie panoram | Adobe Firefly Services / Photoshop API (Generative Fill z maską) | pełna, ale jakość wymaga człowieka w pętli |
| Panel akceptacyjny | lokalna aplikacja webowa (FastAPI + prosty frontend) | pełna |
| Render After Effects | ExtendScript (JSX) + `aerender` (CLI) | pełna |
| Podmiana w DaVinci Resolve | Resolve **Studio** Scripting API (Python) | pełna — wymaga wersji Studio |
| Eksport DCP | Resolve Studio (natywnie, nieszyfrowane SMPTE) lub DCP-o-matic CLI | pełna |
| Walidacja DCP | Clairmeta (open source QC) | pełna |

Warunki brzegowe (nie do obejścia kodem):
- **After Effects i DaVinci Resolve muszą działać lokalnie** na stacji z licencjami.
  Agent pisze skrypty, ale wykonanie odbywa się na Twojej maszynie.
- Zewnętrzne skryptowanie Resolve wymaga **DaVinci Resolve Studio** (wersja darmowa
  nie wystawia API dla zewnętrznych skryptów).
- Szyfrowane DCP + KDM wymagają licencji easyDCP; **nieszyfrowane SMPTE DCP**
  Resolve Studio i DCP-o-matic robią bez dodatkowych opłat. (Dystrybucja kinowa
  bywa robiona na nieszyfrowanych kopiach — do potwierdzenia z dystrybutorem.)

---

## 2. Kluczowa decyzja architektoniczna: pełne DCP vs OV + VF

Zanim powstanie kod, trzeba rozstrzygnąć jedną rzecz, bo zmienia ona skalę
przedsięwzięcia o rząd wielkości.

### Wariant A — 200 pełnych DCP (tak jak w opisie)
- Rozmiar: film ~75–90 min @ 150–250 Mb/s ≈ **85–140 GB na kopię → 17–28 TB łącznie**.
- Czas enkodowania JPEG 2000: ~1–2 h na kopię na mocnej stacji → **250–400 h maszynowych**
  (10–17 dni ciągłej pracy jednej maszyny).
- Zaleta: każde kino dostaje jedną, samodzielną paczkę — zero ryzyka przy ingeście.

### Wariant B — 1× OV + 200× VF (rekomendowany do rozważenia)
Standard DCI przewiduje **OV (Original Version)** + **VF (Version File)** — paczkę
uzupełniającą, która podmienia tylko wybraną rolkę (reel). Skoro zmienia się
wyłącznie ujęcie otwierające:
- master dzielimy na rolki tak, by ujęcie otwierające było **osobną rolką**;
- każde kino dostaje ten sam OV + swój VF (**~1–3 GB** zamiast ~100 GB);
- łączny wolumen: ~100 GB + ~0,5 TB; enkodowanie VF: minuty zamiast godzin.

Ryzyka wariantu B: część kin słabiej radzi sobie z ingestem OV+VF (wymaga wgrania
dwóch paczek i wyboru wersji z VF); Resolve nie autoruje OV/VF — trzeba użyć
**DCP-o-matic** (obsługuje VF) lub easyDCP. Wymaga testu ingestu w 2–3 kinach
przed decyzją.

**Rozstrzygnięcie (2026-07-17): wariant A** — kin będzie mniej niż 200, więc
prostota ingestu wygrywa z oszczędnością wolumenu. Moduł `dcp_builder` i tak
projektujemy z wymiennym backendem (Resolve-full jako jedyny implementowany;
DCP-o-matic-VF opisany jako plan awaryjny na wypadek wzrostu skali).

---

## 3. Architektura rozwiązania

```
                    ┌──────────────────────────────┐
                    │   Panel WWW (localhost)      │
                    │   FastAPI + prosty frontend  │
                    │   - dashboard statusów       │
                    │   - akceptacja kadrów        │
                    └───────────┬──────────────────┘
                                │
┌───────────────┐   ┌───────────▼──────────────────┐   ┌────────────────┐
│ kina.xlsx     │──▶│   ORKIESTRATOR (Python)      │◀──│ referencje     │
│ (import)      │   │   - maszyna stanów           │   │ panoram (JPG)  │
│ kina.xlsx     │◀──│   - kolejka zadań            │   └────────────────┘
│ (status, eksport)  │   - SQLite: stan procesu    │
└───────────────┘   └──┬──────┬──────┬──────┬──────┘
                       │      │      │      │
             ┌─────────▼─┐ ┌──▼───┐ ┌▼─────────┐ ┌▼──────────────┐
             │ panorama_ │ │ ae_  │ │ resolve_ │ │ dcp_builder   │
             │ gen       │ │ render│ │ conform │ │ + walidacja   │
             │ (Firefly/ │ │(aerender│(Resolve │ │ (Clairmeta)   │
             │  PS API)  │ │ + JSX)│ │ Py API) │ │               │
             └───────────┘ └──────┘ └──────────┘ └───────────────┘
```

Zasady:
1. **Źródłem prawdy jest SQLite**, nie Excel. Excel to format importu (lista kin)
   i eksportu (raport statusów). Dzięki temu proces jest wznawialny i odporny na
   równoczesną edycję arkusza.
2. **Każdy etap to idempotentny krok maszyny stanów**: ma zdefiniowane wejście,
   wyjście (plik o deterministycznej ścieżce) i status. Restart = pominięcie kroków,
   których artefakt istnieje i przeszedł walidację (checksum w bazie).
3. **AE i Resolve pracują sekwencyjnie na jednej stacji** (kolejka). Skalowanie =
   dołożenie drugiej stacji roboczej, nie wątków.
4. **Panel akceptacyjny to jedyny krok manualny w torze** — reszta jedzie sama.

### Statusy (maszyna stanów)

```
PENDING → PANORAMA_GENERATED → AWAITING_APPROVAL → (REJECTED → PANORAMA_GENERATED …)
        → APPROVED → AE_RENDERING → AE_DONE → RESOLVE_CONFORMED
        → DCP_ENCODING → DCP_VALIDATED → DONE
любой krok → ERROR (z logiem i możliwością retry od tego kroku)
```

---

## 4. Co w pełni automatyczne, a co manualne

| Etap | Tryb |
|---|---|
| Import listy kin z Excela | automat |
| Generowanie panoram (Generative Fill z maską + referencją) | automat, **ale**: |
| Akceptacja kadru | **manualna — świadomie** (jakość AI niegwarantowana; podpisujesz się pod każdym miastem) |
| Ręczna podmiana kadru po korekcie w Photoshopie | manualna, panel przyjmuje upload |
| Render AE | automat |
| Konform w Resolve + render mastera fragmentu / pełnego | automat |
| Enkodowanie i nazewnictwo DCP | automat |
| Walidacja DCP (Clairmeta: struktura, hashe, zgodność SMPTE) | automat |
| QC wyrywkowe (obejrzenie kilku DCP na projektorze/playerze) | manualne, próbka 5–10% |
| Zapis statusów do arkusza | automat |

---

## 5. Integracje — jak połączyć poszczególne elementy

### Excel ⇄ system
- `openpyxl`: import kolumn (nr, kino, miasto, ścieżka referencji), eksport statusów
  do kopii arkusza `kina_status.xlsx` (nigdy nie nadpisujemy oryginału).

### Generowanie panoram
- **Maska stała** (przygotowana raz w Photoshopie — obszar nieba/panoramy za linią drzew).
- Adobe Firefly Services / Photoshop API: Generative Fill na obszarze maski,
  z promptem opisującym miasto + obrazem referencyjnym; parametry stałe dla
  wszystkich miast (spójna stylistyka i światło).
- Zapis: `output/01_panoramy/{nr}_{miasto}/v{n}.png` — wersjonowanie podejść.
- Fallback: grafik robi kadr ręcznie i wgrywa go przez panel (ten sam slot).

### Panel akceptacyjny
- Lokalna aplikacja webowa (FastAPI + HTMX/React): siatka miast, podgląd
  bazowy-vs-wygenerowany (suwak porównawczy), przyciski
  Akceptuj / Odrzuć+regeneruj / Wgraj własny / Zatwierdź finalnie.
- Zatwierdzenie przenosi plik do `output/02_zatwierdzone/{nr}_{miasto}.png`
  i odblokowuje kolejkę AE.

### After Effects
- Projekt-szablon `.aep` z kompozycją, w której warstwa panoramy wskazuje na
  **stałą ścieżkę** `work/current_panorama.png`.
- Sterowanie: skrypt Python kopiuje zatwierdzony PNG pod stałą ścieżkę, po czym
  uruchamia `aerender -project szablon.aep -comp "OPENING" -output ...`.
  (Podmiana pliku pod stałą ścieżką eliminuje potrzebę grzebania w projekcie;
  ExtendScript/JSX potrzebny tylko, jeśli trzeba coś więcej niż relink.)
- Output: master fragmentu w formacie bezstratnym/near-lossless
  (ProRes 4444 lub sekwencja TIFF 16-bit), **w przestrzeni barwnej zgodnej
  z masterem filmu**.

### DaVinci Resolve
- Resolve **Studio** + Scripting API (Python, `DaVinciResolveScript`).
- Ten sam trik ze stałą ścieżką: projekt wzorcowy ma na timeline fragment
  podlinkowany do `work/current_fragment.mov`. Skrypt podmienia plik na dysku →
  Resolve widzi nową zawartość bez chirurgii na timeline (API do podmiany klipów
  jest krucha — unikamy jej).
- Skrypt: otwiera projekt → weryfikuje relink → dodaje job do Render Queue
  z presetem DCP (lub presetem mastera dla toru DCP-o-matic) → renderuje →
  odczytuje status joba.
- Audio: nietknięte — podmieniamy wyłącznie wideo fragmentu, ścieżka dźwiękowa
  leży na osobnych trackach wzorcowego mastera.

### DCP
- **Backend A (pełne DCP):** Resolve Studio, format DCP (SMPTE, nieszyfrowane),
  2K flat/scope 24 fps zgodnie z masterem, XYZ z zarządzaniem barwą Resolve.
- **Backend B (OV+VF):** Resolve renderuje master fragmentu → `dcpomatic2_create`
  / `dcpomatic2_cli` buduje VF względem OV.
- Nazewnictwo wg **DCNC (Digital Cinema Naming Convention)**, np.:
  `WandaIJejBanda2_FTR-{nr}_F_PL-XX_51_2K_{STUDIO}_{YYYYMMDD}_{FAC}_SMPTE_OV`
  (człon `{nr}`/miasto w polu wersji terytorialnej lub ContentVersion — do
  ustalenia z dystrybutorem, DCNC ma sztywne pola).
- Po enkodzie: **Clairmeta** — walidacja struktury, hashów i zgodności SMPTE;
  wynik zapisany w bazie; dopiero wtedy status `DONE`.

---

## 6. Forma aplikacji: desktop vs web vs skrypty

**Rekomendacja: zestaw skryptów Python + lokalny panel webowy (localhost).**

- Desktop (Electron/Qt) — zbędny narzut; nie daje nic ponad panel w przeglądarce.
- Web „prawdziwie" hostowany — odpada: AE/Resolve i tak działają na konkretnej stacji.
- Skrypty + FastAPI na localhost: najmniej kodu, panel dostępny też z drugiego
  komputera w sieci studia (akceptacja kadrów przez reżysera/producenta bez
  siadania przy stacji renderującej).

---

## 7. Ograniczenia automatyzacji AE i Resolve

**After Effects**
- `aerender` działa bez otwierania GUI, ale wymaga zainstalowanego, zalicencjonowanego
  AE na tej maszynie; równoległość ograniczona (praktycznie 1 render naraz na stację).
- ExtendScript jest wiekowy (ES3), debugowanie uciążliwe — dlatego minimalizujemy
  jego rolę (relink przez stałą ścieżkę zamiast skryptowej podmiany warstw).
- Brak headless na serwerze bez licencji; render farmy AE to osobny temat (nie
  potrzebny przy fragmencie ~kilkudziesięciu sekund).

**DaVinci Resolve**
- Zewnętrzne API **tylko w Studio**.
- API jest oficjalne, ale słabo udokumentowane; operacje edycyjne na timeline
  (podmiana klipu, trim) bywają zawodne między wersjami → stąd wzorzec
  „stała ścieżka + relink", który omija najbardziej kruchy fragment API.
- Resolve nie autoruje OV/VF ani szyfrowanych DCP (bez easyDCP).
- Jedna instancja Resolve na maszynę; kolejkujemy sekwencyjnie.

**Wspólne**
- Zarządzanie barwą to najłatwiejsze miejsce na niewidoczny na podglądzie,
  a widoczny na ekranie kinowym błąd: fragment z AE musi być w identycznej
  przestrzeni co master (test A/B na sklejce w pilotażu obowiązkowy).

---

## 8. Zabezpieczenie procesu przy 200 kopiach

1. **SQLite jako źródło prawdy** + statusy per krok, nie per kino — wznowienie
   dokładnie od miejsca awarii.
2. **Idempotencja**: krok najpierw sprawdza, czy jego artefakt istnieje i ma
   zgodny checksum (SHA-256 w bazie) — jeśli tak, pomija pracę.
3. **Deterministyczne ścieżki i nazwy** — żadnych nazw „z ręki".
4. **Walidacja na każdym szwie**: PNG (wymiary, tryb koloru) → render AE (długość
   w klatkach, fps, hash) → render Resolve (długość, fps) → DCP (Clairmeta).
5. **Log per kino** (`logs/{nr}_{miasto}.log`) + log zbiorczy; błąd nie zatrzymuje
   kolejki, tylko oznacza rekord `ERROR` i jedzie dalej.
6. **Dry-run** i limit `--only 1,2,3` do testów na podzbiorze.
7. **Miejsce na dysku sprawdzane przed enkodem** (patrz szacunki w §2).
8. **Kopia arkusza, nigdy edycja oryginału**; eksport raportu CSV po każdej sesji.
9. **QC wyrywkowe**: 5–10% gotowych DCP obejrzane na playerze/projektorze.

---

## 9. Struktura folderów roboczych, nazewnictwo, format arkusza

```
dcp-personalizacja/
  input/
    kina.xlsx                  # arkusz wejściowy
    base/
      kadr_bazowy.psd/png      # ujęcie referencyjne (Warszawa)
      maska_panoramy.png       # stała maska obszaru podmiany
    referencje/
      {nr:03d}_{miasto}.jpg    # referencja panoramy per miasto
    ae/szablon_opening.aep
    resolve/projekt_wzorcowy.drp
  work/
    current_panorama.png       # slot podmiany dla AE
    current_fragment.mov       # slot podmiany dla Resolve
    state.sqlite               # baza statusów
  output/
    01_panoramy/{nr:03d}_{miasto}/v{n}.png
    02_zatwierdzone/{nr:03d}_{miasto}.png
    03_render_ae/{nr:03d}_{miasto}.mov
    04_dcp/{nr:03d}_{miasto}/{nazwa_DCNC}/
  logs/
    {nr:03d}_{miasto}.log
    pipeline.log
  raporty/
    kina_status.xlsx           # eksport statusów (kopia arkusza + kolumny statusowe)
```

**Arkusz wejściowy `kina.xlsx`** (jeden wiersz = jedno kino):

| kolumna | przykład | uwagi |
|---|---|---|
| `nr` | 001 | numeracja trzycyfrowa, stała |
| `kino` | Kino Muza | nazwa kina |
| `miasto` | Poznań | klucz personalizacji |
| `miasto_slug` | poznan | ASCII, do nazw plików (generowane automatycznie, edytowalne) |
| `referencja` | referencje/001_poznan.jpg | ścieżka względna |
| `uwagi` | — | np. wskazówki do panoramy („z Ostrowem Tumskim") |

Kolumny statusowe (tylko w eksporcie `kina_status.xlsx`): `status`, `wersja_kadru`,
`data_akceptacji`, `dcp_nazwa`, `dcp_hash_ok`, `blad`.

**Nazewnictwo plików pośrednich:** zawsze `{nr:03d}_{miasto_slug}` — sortowalne,
jednoznaczne, bez polskich znaków. Kilka kin w tym samym mieście = ten sam kadr,
ale osobne nry i osobne DCP (albo świadoma deduplikacja — flaga w arkuszu).

---

## 10. Plan MVP — pilotaż na 3 kinach / 3 miastach

**Faza 0 — decyzje i przygotowanie assetów (bez kodu)**
- Wybór 3 miast testowych o różnej trudności (np. Kraków — rozpoznawalna panorama,
  Rzeszów — średnia, mała miejscowość bez charakterystycznej panoramy).
- Przygotowanie: maska panoramy, szablon AE ze slotem na stałej ścieżce,
  projekt wzorcowy Resolve, 3 referencje.
- Decyzje: ~~szyfrowanie DCP~~ (rozstrzygnięte: bez szyfrowania), SMPTE 2K 24 fps
  (potwierdzić z masterem), wstępnie wariant A vs B z §2.

**Faza 1 — kręgosłup danych**
- Moduły: `excel_io`, `state` (SQLite, maszyna stanów), CLI `pipeline status/run`.
- Test: import 3 kin, statusy, wznawianie.

**Faza 2 — panoramy + panel**
- `panorama_gen` (Firefly/PS API) + panel akceptacyjny (lista, porównanie, akcje).
- Test: 3 miasta × kilka wersji, akceptacja, ręczna podmiana.

**Faza 3 — After Effects**
- `ae_render`: slot + `aerender` + walidacja outputu.
- Test: 3 zatwierdzone kadry → 3 fragmenty; kontrola barwna względem mastera.

**Faza 4 — Resolve + DCP**
- `resolve_conform` + `dcp_builder` (backend A) + `qc` (Clairmeta).
- Test: 3 pełne DCP, walidacja, **ingest w prawdziwym kinie / na serwerze kinowym**.
- (Wariant rozstrzygnięty na A — próba OV+VF tylko, gdyby skala urosła.)

**Faza 5 — przebieg zbiorczy**
- Pełny run 3 kin bez dotykania czegokolwiek poza panelem akceptacji.
- Pomiar czasów per etap → ekstrapolacja na 200 kin → plan sprzętowy
  (czy 1 stacja wystarczy, czy potrzebne 2–3).

**Faza 6 — skalowanie do 200**
- Import pełnego arkusza, praca falami (np. po 20 kin), QC wyrywkowe, raport.

---

## 11. Struktura repozytorium narzędzia i lista modułów

```
dcp-personalizer/
  README.md
  pyproject.toml
  config.yaml                # ścieżki, preset DCP, parametry generowania
  src/dcp_personalizer/
    cli.py                   # wejście: run / status / retry / export-report
    state.py                 # SQLite + maszyna stanów + checksumy
    excel_io.py              # import kina.xlsx, eksport kina_status.xlsx
    panorama_gen.py          # Firefly/Photoshop API, wersjonowanie kadrów
    approval/
      server.py              # FastAPI: panel akceptacyjny
      templates/             # widoki (lista, porównanie, upload)
    ae_render.py             # slot + aerender + walidacja
    resolve_conform.py       # Resolve Scripting API: relink, render queue
    dcp_builder.py           # backend A (Resolve) / backend B (dcp-o-matic VF)
    qc.py                    # Clairmeta + kontrole długości/fps/hash
    naming.py                # DCNC + slugi + ścieżki deterministyczne
    logging_setup.py
  scripts/
    ae/relink_and_check.jsx  # awaryjny ExtendScript (gdy relink slotem nie wystarczy)
    resolve/preset_notes.md  # dokumentacja presetu renderu/DCP
  tests/
    test_state.py test_naming.py test_excel_io.py  # logika bez AE/Resolve
```

Zależności zewnętrzne: Python 3.11+, `openpyxl`, `fastapi`, `uvicorn`, `pillow`,
`clairmeta`; na stacji: After Effects, DaVinci Resolve **Studio**, opcjonalnie
DCP-o-matic (CLI); dostęp do Adobe Firefly Services (klucz API).

---

## 12. Główne ryzyka techniczne (skrót)

1. **Jakość i spójność panoram AI** — światło/perspektywa/stylistyka bazowego kadru;
   mniejsze miasta bez ikonicznej panoramy. Mitygacja: stała maska, stałe parametry,
   człowiek w pętli, fallback ręczny. Osobno: **prawa do referencji** panoram.
2. **Zarządzanie barwą na szwie** AE→Resolve→XYZ — test sklejki w pilotażu.
3. **Wolumen i czas** pełnych DCP (~100–140 GB i ~1–2 h enkodowania na kopię) —
   po decyzji na wariant A trzeba policzyć dyski i harmonogram enkodowania dla
   finalnej liczby kin; przy dużej liczbie ratunkiem jest druga stacja lub
   powrót do wariantu OV+VF.
4. **Kruchość API Resolve** przy edycji timeline — omijana wzorcem stałej ścieżki.
5. **Zgodność ingestu w kinach** (SMPTE vs Interop, OV+VF) — test na prawdziwym
   serwerze kinowym w fazie 4, przed skalowaniem.
6. **Licencje**: Resolve Studio (wymagane), Firefly Services (koszty generowania
   ~200+ obrazów z iteracjami). easyDCP zbędny — DCP bez szyfrowania (decyzja).
