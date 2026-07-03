---
type: decyzja
id: BENCH-DEC2
title: "Decyzja — po kalibracji zestawów fokus na samym Slayerze"
status: przyjeta
parents: ["BENCH-DEC1", "BENCH-S3"]
author: Arkadiusz Słota
date: 2026-07-02
---

# DEC2 — Panel spełnił rolę; przedmiotem testu staje się Slayer

## Kontekst
Panel 5 modeli (bielik 1.5B → Slayer 27B) był używany do **kalibracji zestawów**: ustalenia gradientu
trudności i sprawdzenia, że itemy dyskryminują. Ten cel jest osiągnięty:
- **Gradient działa:** D1 łatwy (2–6 kroków) → brutalny (7–10) → ekstremalny (11–13) rozkłada modele.
- **Zestawy dyskryminują:** ujawniły dwie ligi rozumowania; liga B (gemma) spada z trudnością, liga A
  (Slayer, nemotron) trzyma się dłużej.
- **Sufit i floor zmierzone:** wiemy, gdzie itemy tracą informację (S3).

## Decyzja
Od teraz **przedmiotem testu jest sam Slayer v49** — próbujemy go ze wszystkich stron. Panel słabych
modeli **nie jest już rutynowo odpalany** (względy efektywności: jeden model = brak żonglowania VRAM/LM
Studio, tylko proxy Slayera; szybsza iteracja).

## Uzasadnienie
- Cel projektu (Probierz) to **charakterystyka zdolności modelu docelowego** (Slayer), nie ranking
  cudzych modeli. Panel był środkiem (kalibracja), nie celem.
- Efektywność: przejazd 5 modeli × zestaw to godziny i zarządzanie VRAM; sam Slayer to minuty.
- Wynik na słabszych modelach jest już przewidywalny (floor/liga B) — niska wartość informacyjna (S3).

## Zastrzeżenie metodologiczne (kiedy WRACAMY do modelu odniesienia)
Rezygnacja z panelu ma jeden koszt: **przy pojedynczym modelu nie da się odróżnić „item za trudny/wadliwy"
od „Slayer tego nie umie".** Dlatego reguła:
- **Gdy Slayer oblewa item** i chcemy wiedzieć, czy to słabość Slayera czy wada itemu → uruchom **jeden
  model odniesienia** (nemotron-4B, liga A) na tym itemie. Jeśli odniesienie zdaje, a Slayer nie → realna
  słabość Slayera. Jeśli obaj oblewają → podejrzenie wadliwego itemu (do audytu GT).
- Test rozłączności wymiarów (C2/S4) **nadal wymaga panelu** — gdy do niego wrócimy (D3–D6), panel
  trzeba przywrócić. DEC2 dotyczy fazy **charakterystyki Slayera**, nie fazy dowodzenia konstruktu.

## Konsekwencje operacyjne
- Nowe zestawy przejeżdżamy domyślnie **tylko Slayerem** (`wyniki-slayer-v49.json`).
- Model odniesienia (nemotron) odpalamy **selektywnie**, przy podejrzanych failach.
- GT każdego trudnego itemu **weryfikujemy programowo** przed przejazdem (bez panelu to jedyna ochrona
  przed wadliwą rubryką).

## Powiązania
parent: [[D-DEC1-Kolejnosc-Wymiary-Vs-Panel|DEC1]] · [[../25-Syntezy/S3-IRT-Taksonomia|S3]] · [[../90-Ewaluacja/Analiza-D1-Hard-Sufit|analiza D1-hard]] · [[../90-Ewaluacja/Stan|Stan]]
