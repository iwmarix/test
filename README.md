# Asystent Produkcji Filmowej

Repozytorium-asystent do zarządzania produkcją filmów i animacji z pomocą Claude Code: planowanie, breakdowny, budżety, harmonogramy oraz prewizualizacje i koncepty z użyciem narzędzi AI (Adobe/Firefly, Figma).

## Jak korzystać

Otwórz sesję Claude Code w tym repozytorium i używaj komend:

| Komenda | Co robi |
|---------|---------|
| `/import-scenariusza` | wczytuje scenariusz (.doc/.docx/.pdf), konwertuje do tekstu, zakłada projekt |
| `/breakdown` | pełny breakdown: sceny, postacie, lokacje/światy, piosenki, sekwencje złożone |
| `/budzet` | kosztorys w układzie PISF wyprowadzony z breakdownu |
| `/harmonogram` | plan produkcji z kamieniami milowymi (Gantt) |
| `/koncept-art` | moodboardy, projekty postaci, briefy VFX, prewizualizacje z narzędzi AI |

Można też pisać naturalnie, np. „przygotuj listę pytań do studia animacji o wycenę sceny Origamków" — zasady pracy asystenta opisuje `CLAUDE.md`.

## Struktura

```
narzedzia/            skrypty (ekstrakcja tekstu ze starych .doc itd.)
projekty/<projekt>/   scenariusz / breakdown / budzet / harmonogram / vfx / koncepty
.claude/skills/       definicje komend asystenta
```

## Projekty

- **wanda-i-jej-banda-2** — „Wanda i jej banda 2: W przedszkolu" (Mojca Tirš), film animowany, 30 scen + 3 teledyski. Gotowy pełny breakdown, briefy efektów E1–E10, szkielety budżetu i harmonogramu.
