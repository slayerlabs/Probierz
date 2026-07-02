---
type: teza
id: BENCH-T5
title: "Każdy wymiar mierzalny zadaniem z falsyfikowalną rubryką, nie proxy"
status: w-dyskusji
parents: ["BENCH-C2"]
author: Arkadiusz Słota
date: 2026-07-02
---

# T5 — Rubryka pass/fail, nie miara zastępcza

## Teza
Wymiar konstruktu (T4) mierzymy **zadaniem z jawną, falsyfikowalną rubryką**: deterministycznym
kryterium rozstrzygającym pass/fail dla danej odpowiedzi w sposób powtarzalny. **Odrzucamy miary
zastępcze (proxy)**, które korelują ze zdolnością, lecz nie mierzą jej bezpośrednio:

- **perplexity / log-loss** — mierzy dopasowanie rozkładu do korpusu, nie poprawność rozumowania;
  model o niższej perplexity może częściej generować pewne, lecz nieprawdziwe odpowiedzi (halucynacje).
- **podobieństwo embeddingowe do wzorca** — premiuje podobieństwo powierzchniowe; przepuszcza
  odpowiedzi poprawne stylistycznie, lecz błędne merytorycznie.
- **sam wybór A/B/C/D (multiple choice bez uzasadnienia)** — podatny na zgadywanie i skróty formatu;
  mierzy eliminację dystraktorów, nie zdolność generatywną.

## Uzasadnienie
Celem Probierza (C1) jest pomiar **zdolności, nie artefaktu**. Proxy powiela problem kontaminacji po
stronie metryki: dostarcza wielkość skorelowaną ze zdolnością, więc **formalnie** przypomina pomiar,
lecz optymalizacja pod nią (Goodhart) rozdziela wartość metryki od zdolności rzeczywistej. Rubryka
pass/fail jest **bezpośrednia**: definiuje, co poprawne rozwiązanie musi zawierać lub wykonać, i to
podlega weryfikacji.

## Wymogi rubryki (warunek dopuszczenia itemu)
Rubryka jest dopuszczalna wyłącznie, gdy spełnia wszystkie:
1. **Falsyfikowalność** — istnieje obserwowalna odpowiedź, która ją **oblewa** (jeśli każda odpowiedź
   przechodzi, rubryka nie mierzy niczego).
2. **Determinizm dla grader-a** — dwóch niezależnych graderów (człowiek lub LLM-sędzia) przypisuje ten
   sam pass/fail; docelowo mierzona **zgodność między-graderami** (np. Cohen κ).
3. **Odporność na format** — pass zależy od treści lub zachowania, nie od przypadkowego formatowania
   (w przeciwnym razie pomiar rejestruje format — patrz AT5).
4. **Powiązanie z taksonomią awarii (S3)** — fail klasyfikowany: `halucynacja` / `błędny-plan` /
   `ciche-pominięcie` / `format` / `pętla`. Wynik = pass-rate **oraz** rozkład trybów awarii.

## Relacja do istniejącego benchmarku
`csharp-solid-v1` realizuje już ten wzorzec (`kryterium_pass` + `tryb_awarii` w schemacie itemu). T5
**uogólnia** go z pojedynczego benchmarku do reguły obowiązującej wszystkie wymiary konstruktu.

## Dowód / falsyfikacja
T5 jest normą projektową weryfikowaną operacyjnie: jeśli dla wymiaru D_i **nie można** skonstruować
rubryki spełniającej cztery wymogi (np. „naturalność stylu" bywa nierozstrzygalna deterministycznie),
to albo wymiar jest źle zdefiniowany (powrót do T4/S4), albo należy mierzyć go porównawczo (ranking
par, nie pass/fail). **Obalenie T5:** jeśli rubryki pass/fail systematycznie dają niższą zgodność
między-graderami niż proxy (κ rubryki < κ proxy), to proxy są rzetelniejsze i teza upada.

## Powiązania
parent: [[../00-Cele/C2-Konstrukt-Zdolnosci-Jezykowej|C2]] · siostra: [[T4-Dekompozycja-Wymiarow|T4]] · kontra: [[../15-Antytezy/AT5-Format-Nie-Zdolnosc|AT5]] · taksonomia awarii: [[../25-Syntezy/S3-IRT-Taksonomia|S3]]
