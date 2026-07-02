---
type: benchmark
id: BENCH-D1-EXTREME-V1
title: "d1-rozumowanie-extreme-v1 — D1 ekstremalny (rozróżnienie ligi A)"
status: eval-only
parents: ["BENCH-T3", "BENCH-S3", "BENCH-D1-HARD-V1"]
author: Arkadiusz Słota
date: 2026-07-02
---

# d1-rozumowanie-extreme-v1 🇵🇱

> **6 ekstremalnych zadań** (poziom 11–13). Cel: **rozróżnić ligę A** — na `d1-rozumowanie-hard-v1`
> Slayer-27B i nemotron-4B uzyskały po 91% (sufit wrócił wyżej). Ten zestaw celuje w pułap najmocniejszych.

## Motywacja (z analizy D1-hard)
Brutalny zestaw ujawnił dwie ligi, ale **liga A (Slayer, nemotron) nadal na 91%** — nierozróżnialna.
Zgodnie z S3 (rotacja poprzeczki): gdy modele nasycą pasmo, podnosimy trudność. Ten zestaw = poziom 11+.

## Panel (zawężony — świadomie)
Testujemy tylko **ligę A + gemma** jako odniesienie. Qwen-1.7B (liga B) i bielik-1.5B (floor) **pominięte**
— na poziomie 7–10 były już na/pod podłogą, poziom 11+ nie da od nich sygnału (byłyby 0, brak informacji
wg S3). To celowa decyzja, nie luka.

## Czystość — zmierzona
`contamination_check.py` vs `seed_500_training_final`: **CZYSTY 0%** (span 0 tok).

## Ground-truth — zweryfikowany niezależnie
Każdy GT **potwierdzony programowo**: sprawdzenie spójności (L11-01 prostokąt), brute-force modeli
samoodniesienia (L11-02: jedyne k=4), symulacja Collatza (L12-01: 8 kroków), układ równań (L12-02:
27.5), brute-force permutacji (L13-01: 12), wyczerpanie hipotez winny=jedyny-kłamca (L13-02: B).
> Uwaga jakościowa: pierwotny L11-02 („3 zdania") miał **dwa** spójne modele (k=0 i k=1) — wykryte
> przy weryfikacji i **odrzucone**; zastąpione wariantem 5-zdaniowym o jednoznacznym rozwiązaniu (k=4).
> To ilustruje regułę: GT trudnych itemów sprawdzamy programowo, nie deklarujemy.

## Typy pułapek (meta-rozumowanie, nie tylko długi łańcuch)
- **nadmiarowe/sprzeczne dane** (L11-01) — wykryć niespójność, nie policzyć „coś";
- **samoodniesienie** (L11-02) — układ zdań o sobie samych, jednoznaczny model;
- **długi łańcuch warunkowy** (L12-01 Collatz) — deterministyczny, ale długi;
- **układ z wynikiem ułamkowym** (L12-02) — nie zaokrąglać do „ładnej" liczby;
- **kombinatoryka przez dopełnienie** (L13-01);
- **wyczerpująca analiza hipotez z meta-warunkiem** (L13-02 winny=jedyny kłamca).

## Schemat, ocena, pomiar
Jak w `d1-rozumowanie-v1`/`-hard-v1`. Itemy z odpowiedzią zamkniętą mają `klasy_odpowiedzi` (L13-02).

## Status / następne
v1, eval-only, audyt 0%, GT zweryfikowane. Cel przejazdu: czy rozróżnia Slayer vs nemotron (liga A).
Jeśli oba znów ~100% → poprzeczkę podnieść dalej; jeśli się rozjadą → mamy dyskryminację na szczycie.

## Powiązania
[[../d1-rozumowanie-hard-v1/README|d1-rozumowanie-hard-v1]] · [[../../docs/90-Ewaluacja/Analiza-D1-Hard-Sufit|analiza D1-hard]] · [[../../docs/25-Syntezy/S3-IRT-Taksonomia|S3]]
