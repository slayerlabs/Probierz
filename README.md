<p align="center">
  <img src="assets/flaga-pl.svg" alt="Flaga Polski" width="200">
</p>

# Probierz 🇵🇱

> **Kamień probierczy dla modeli** — bezlitosny test, który demaskuje, czy zdolność jest *prawdziwa*,
> czy zapamiętana (skażona). Rysa nie kłamie. Benchmarki **kontaminacyjnie czyste**, łamiące modele
> w skali dającej **mierzalny progres** — nie da się ich sfałszować.
>
> **Autor:** Arkadiusz Słota · **Lab:** SlayerLab 🇵🇱 · **Status:** know-how + runnable rdzeń · _Polska technologia, globalny zasięg_
> **Metoda pomiarowa:** [Dendrometria](../Optimal%20Design%20of%20Structures/Dendrometria/) (mierzymy, nie deklarujemy)

## Po co (dwie pieczenie na jednym ogniu)

Tworzymy dane treningowe **od zera** (`slayerlabs/datasets`, `academy/lab`, OpenPL, MicroModels).
Skutek: **wiemy dokładnie, co weszło do treningu** → możemy *udowodnić*, które dane NIE mogą trafić
do ewaluacji. To rozwiązuje największy nierozwiązany problem ewaluacji LLM — **kontaminację**
(MMLU i spółka są skażone). Robiąc dane, dostajemy czysty eval za darmo. Logiczne.

## Dwa ostrza (rdzeń metody)

### 1. Kontrola kontaminacji przez *provenance* (T1)
Każdy dataset ma etykietę: **trening-only** vs **eval-only**, które NIGDY się nie krzyżują
(`protokol/PROVENANCE-Manifest.md`). Nie ufamy deklaracji — **mierzymy** overlap n-gramowy
(`tools/contamination_check.py`, ten sam mechanizm n-gram co w `micro-models`: detektor dosłownej pamięci).

> **Dowód od pierwszego uruchomienia:** audyt `test_verification.jsonl` vs `seed_500` →
> **90% itemów skażonych** (mean overlap 0.84, 60% near-verbatim). Ten plik **nie jest** czystym
> held-out. Narzędzie złapało realny przeciek zanim ktokolwiek ogłosił benchmark.

### 2. Wymiana dwóch teamów — *blind exchange* (T2)
Sam-na-sobie **zawsze przeuczysz** swój benchmark (Goodhart → [M3](../ObsidianVault/Slayer/Repozytorium-Mechanizmow/)).
Drugi team buduje benchmarki, których **nigdy nie widziałeś**, Ty budujesz dla nich — wymieniacie się.
Nie da się ograć testu, którego nie znasz. To ten sam mechanizm co **ślepy audyt** (M4) i
ślepy re-review Xaviera: niezależny ewaluator = ground truth.

> ⚠️ **Pułapka:** benchmark **spala się po ujawnieniu** (staje się danymi drugiego teamu).
> Dlatego: **commitment scheme** (hash przed reveal), zestawy **jednorazowe**, rotacja —
> `protokol/PROTOKOL-Wymiany.md`.

## Bezlitosne ALE mierzalne (T3)

Za trudne = floor effect (wszyscy ~0, brak sygnału). Za łatwe = sufit. Rozwiązanie:
**gradient trudności** (dyskryminacja itemów, IRT-style) + **taksonomia awarii** — nie tylko
accuracy, ale *jak* model pęka (ciche błędy = najgorszy tryb, jak false-discard u Xaviera).

## Co mierzymy i jak to formalizujemy (konstrukt + model pomiaru)

Dwa ostrza (T1/T2) i T3 odpowiadają na pytanie „**jak testować uczciwie**". Osobna, logicznie
wcześniejsza warstwa odpowiada na pytanie „**co** mierzymy i **jak** to formalizujemy" — zgodnie z
metodą naukową **problem → model matematyczny → baseline → research → eval**.

- **Warstwa 1 — Konstrukt (problem):** definicja mierzalnej „zdolności językowej LLM" jako zbioru
  rozłącznych wymiarów (D1 rozumowanie, D2 semantyka, D3 składnia, D4 długi kontekst, D5 wierność
  instrukcji, D6 kalibracja niepewności). Każdy wymiar pozostaje w taksonomii tylko, jeśli spełnia
  empiryczny warunek obalenia (rozłączność + wariancja niesprowadzalna do czynnika wspólnego).
  Dokumenty: `C2`, `T4`, `T5`, `AT4`, `AT5`, `S4`.
- **Warstwa 2 — Model pomiaru (model matematyczny):** Item Response Theory (2PL/3PL) estymowany
  osobno per wymiar, na panelu ≥5 modeli, z przedziałami ufności (bootstrap). Zdolność $\theta^{(i)}$
  zamiast surowego pass-rate; item najbardziej informatywny przy $\theta \approx b$ (formalizacja
  „punktu dyskryminacji" z T3). Dokumenty: `T6`, `AT6`, `S5`.

Status: dialektyka domknięta (teza↔antyteza↔synteza z warunkiem obalenia); **dowód empiryczny =
faza baseline** (przejazd panelu modeli). Patrz `docs/90-Ewaluacja/Stan.md`.

## Mapa repo

```
Probierz/
├── README.md                        # ten plik — entrypoint
├── docs/
│   ├── 00-Cele/
│   │   ├── C1-Cel.md                # cel: uczciwość pomiaru (provenance, czystość)
│   │   └── C2-Konstrukt-Zdolnosci-Jezykowej.md  # cel: co mierzymy (konstrukt LLM)
│   ├── 10-Tezy/                     # T1 provenance · T2 wymiana · T3 bezlitosne-mierzalne
│   │                                # T4 dekompozycja-wymiarów · T5 rubryka-nie-proxy · T6 IRT
│   ├── 15-Antytezy/                 # AT1 spalanie · AT2 przeciek · AT3 floor-effect
│   │                                # AT4 czynnik-g · AT5 format-vs-zdolność · AT6 założenia-IRT
│   ├── 25-Syntezy/                  # S1 commitment · S2 audyt-overlap · S3 IRT+taksonomia
│   │                                # S4 taksonomia-wymiarów · S5 IRT-per-wymiar+panel
│   ├── 60-Reference/Slownik.md
│   └── 90-Ewaluacja/Stan.md         # żywy stan (zmierzone liczby + status warstw)
├── protokol/
│   ├── PROTOKOL-Wymiany.md          # commitment/reveal/rotacja (operacyjny rdzeń)
│   └── PROVENANCE-Manifest.md       # trening-only vs eval-only (mapa danych)
└── tools/
    └── contamination_check.py       # runnable: n-gramowy audyt przecieku (zweryfikowany)
```

## Kontrakt (żaden benchmark nie wychodzi bez tego)

1. **Manifest provenance** — udokumentowane źródło, etykieta trening/eval.
2. **Audyt kontaminacji PRZESZEDŁ** (`contamination_check.py` → 0% skażonych).
3. **Commitment przed wymianą** — hash opublikowany, zestaw jednorazowy.

Inaczej benchmark mierzy zapamiętywanie, nie zdolność — i jest bezwartościowy.
