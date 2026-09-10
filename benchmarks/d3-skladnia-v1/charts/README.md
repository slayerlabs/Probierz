# d3-skladnia — wykresy na liczbach (dowód że benchmark działa)

Wszystkie liczby są **zmierzone**, reprodukowalne z bajtów (`tools/run_forced_choice.py` na zdekontaminowanym held-oucie). To Stage-1 = **baseline opisowy** na 30 parach; werdykt realnego modelu wymaga produkcyjnego seeda (≥85 rdzenia) + wytrenowanych checkpointów.

## 01_baseline_gradient.png — sygnał rośnie z rzędem n-gramu
Accuracy baseline n-gram na parach minimalnych: order-1 **0.40** → order-4 **0.667** (chance = 0.50).
Im więcej bajtów kontekstu widzi metoda, tym lepiej łapie morfoskładnię — czyli **benchmark ma sygnał, nie szum**. CI szerokie (n=30), dlatego to baseline opisowy, nie werdykt — dokładnie jak mówi pre-reg (moc na werdykt: N_core ≥ 85).

## 02_per_rodzina_o4.png — gdzie siedzi kompetencja
Accuracy baseline (order-4) per rodzina zjawiska: **rząd przypadka 0.40** (czerwony) vs zgoda przym.-rzecz. 0.875, aspekt 0.80, rodzaj przeszły 0.71.
Wniosek: sąsiedzką zgodę/aspekt baseline łapie „za darmo” z lokalnej statystyki — **rząd przypadka to oś dyskryminująca**, tam realny model MUSI pobić baseline, żeby udowodnić że umie polski, a nie tylko statystykę bajtów.

## 03_floor_bpb.png — podłoga BPB (interpretowalność)
Podłoga n-gramowa bits-per-byte na held-oucie: unigram 5.09 → order-4 **2.78** (hard floor). Linia czerwona = toy-model (trenowany na 2 zdaniach) = **5.31 bpb**.
Toy-model jest POWYŻEJ unigrama (5.31 > 5.09) → **nie pobił nawet najprostszej podłogi = „nauczył się nic”**. To pokazuje, że BPB + floor mówią prawdę: bez podłogi „5.31” wyglądałoby jak „coś”, z podłogą widać że to poniżej ściany.

Źródła liczb: panel n-gram `wyniki-ngram-o1..o4.json`; floor zmierzony na held-oucie (order-0..4, add-0.05); toy-model = realny przebieg fast_pl.
