---
type: antyteza
id: BENCH-AT1
title: "Benchmark spala się po ujawnieniu"
status: w-dyskusji
parents: ["BENCH-T2"]
author: Arkadiusz Słota
date: 2026-06-26
---

# AT1 — Wymiana niszczy to, co wymienia (steelman)

## Najmocniejsza wersja
Gdy team A przekazuje benchmark teamowi B, by ocenić modele B — zestaw **przestaje być tajny**.
B (świadomie lub nie) może go wciągnąć do treningu następnej iteracji. Po jednej rundzie benchmark
jest **spalony** = staje się danymi treningowymi drugiej strony. To ta sama „burned after exposure"
co przy każdym ujawnionym tajnym zestawie.

Koszty: budowa świeżych zestawów na każdą rundę jest **droga**; rotacja zżera zasoby obu teamów;
a zaufanie („obiecuję, że nie trenowałem") jest **niefalsyfikowalne** bez kontroli.

## Konsekwencja, jeśli prawdziwa
Blind exchange (T2) działa **raz**. Bez protokołu degeneruje się w zwykły publiczny benchmark,
który natychmiast się kontaminuje → przewaga znika.

## Powiązania
parent: [[../10-Tezy/T2-Wymiana-Blind|T2]] · rozstrzyga: [[../25-Syntezy/S1-Commitment-Protokol|S1]]
