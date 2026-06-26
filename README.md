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

## Mapa repo

```
Probierz/
├── README.md                        # ten plik — entrypoint
├── docs/
│   ├── 00-Cele/C1-Cel.md            # cel + kryteria sukcesu + falsyfikacja
│   ├── 10-Tezy/                     # T1 provenance · T2 wymiana · T3 bezlitosne-mierzalne
│   ├── 15-Antytezy/                 # AT1 spalanie · AT2 przeciek mimo "od zera" · AT3 floor-effect
│   ├── 25-Syntezy/                  # S1 commitment · S2 audyt-overlap · S3 IRT+taksonomia
│   ├── 60-Reference/Slownik.md
│   └── 90-Ewaluacja/Stan.md         # żywy stan (zmierzone liczby)
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
