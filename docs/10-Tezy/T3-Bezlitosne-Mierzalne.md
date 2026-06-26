---
type: teza
id: BENCH-T3
title: "Bezlitosne, ale mierzalny progres"
status: w-dyskusji
parents: ["BENCH-C1"]
author: Arkadiusz Słota
date: 2026-06-26
---

# T3 — Łam modele, ale zostaw sygnał

## Teza
Benchmark ma **łamać** modele (znajdować realne braki), ale jeśli jest *za* trudny — wszyscy
dostają ~0% (**floor effect**), brak sygnału, brak progresu. Za łatwy → sufit. Cel: **bezlitosny
w punkcie dyskryminacji**, gdzie różnice między modelami są największe.

## Mechanizm
- **Gradient trudności** — itemy od „trudne" do „prawie niemożliwe", nie jedna ściana (IRT: dyskryminacja > trudność).
- **Taksonomia awarii** — nie tylko accuracy, lecz *jak* model pęka: halucynacja, błędny plan,
  ciche pominięcie (najgorszy tryb — niewidoczny bez audytu, jak false-discard u Xaviera).
- **Skala progresu** — benchmark żyje: gdy modele go nasycą, podnosimy poprzeczkę (rotacja itemów).

## Dlaczego „mierzalny"
Wynik ma rozróżniać (rozrzut > szum) i pokazywać *gdzie* model się łamie — to mapa do poprawy,
nie tylko ocena. Dendrometria: mierzymy realny sygnał, nie deklarujemy trudności.

## Powiązania
parent: [[BENCH-C1]] · synteza: [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · kontra: [[../15-Antytezy/AT3-Floor-Effect|AT3]]
