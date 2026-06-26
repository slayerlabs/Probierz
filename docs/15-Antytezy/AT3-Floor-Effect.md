---
type: antyteza
id: BENCH-AT3
title: "Bezlitosny = brak sygnału (floor effect)"
status: w-dyskusji
parents: ["BENCH-T3"]
author: Arkadiusz Słota
date: 2026-06-26
---

# AT3 — „Łam modele" zabija pomiar (steelman)

## Najmocniejsza wersja
Jeśli benchmark jest *naprawdę* bezlitosny, wszystkie modele dostają ~0% → **zero dyskryminacji**,
nie wiesz który lepszy, nie ma progresu (floor effect). „Łamanie modeli" i „mierzalny progres" są
w napięciu.

Gorzej: **kalibracja trudności jest cyrkularna** — żeby wiedzieć, że item „dyskryminuje", musisz go
odpalić na modelach, które dopiero chcesz ocenić. IRT wymaga **wielu modeli × wielu odpowiedzi**;
przy małej próbce (jak N=5 u Xaviera) oszacowanie trudności ma gigantyczną wariancję.

## Konsekwencja, jeśli prawdziwa
„Bezlitosne ale mierzalne" (T3) to slogan bez procedury. Bez kalibracji dostajesz albo ścianę
(0% wszędzie), albo arbitralny dobór itemów pod z góry założony wynik.

## Powiązania
parent: [[../10-Tezy/T3-Bezlitosne-Mierzalne|T3]] · rozstrzyga: [[../25-Syntezy/S3-IRT-Taksonomia|S3]]
