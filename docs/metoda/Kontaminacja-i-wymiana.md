---
type: metoda
id: BENCH-METODA-KONTAMINACJA
title: "Kontaminacja i ślepa wymiana benchmarków"
status: propozycja
author: Arkadiusz Słota
date: 2026-06-26
---

# Kontaminacja i ślepa wymiana benchmarków

Dokument dotyczy dwóch źródeł fałszywie wysokich wyników: kontaminacji (model widział benchmark w treningu, więc mierzymy zapamiętywanie, a nie zdolność) oraz dopasowania modelu do własnego testu przez team, który go zbudował. Wynika z niego, że benchmark może zostać wydany dopiero po audycie overlapu z danymi treningowymi, a ocena krzyżowa między teamami wymaga commitmentu i zestawów jednorazowych.

## Provenance: dane trening-only i eval-only

Największym problemem ewaluacji LLM jest kontaminacja. Publiczne benchmarki (MMLU, GSM8K) są masowo skażone scrapem.

Nasza przewaga polega na tym, że dane budujemy od zera (`slayerlabs/datasets`, `academy/lab`, OpenPL, MicroModels). Wiemy dokładnie, co weszło do treningu, więc możemy z góry wyznaczyć dane eval-only, które nigdy nie trafiają do treningu. Budując dane treningowe, dostajemy przy okazji czysty eval.

Mechanizm:
- **Manifest provenance** (`protokol/PROVENANCE-Manifest.md`): każdy dataset jest oznaczony jako `trening-only` albo `eval-only`, ze źródłem i datą.
- Granica trening↔eval jest twarda i udokumentowana, a nie dorozumiana.

## Ograniczenie: „od zera” nie wyklucza przecieku

Budowanie danych od zera daje kontrolę nad źródłem, ale nie nad podobieństwem semantycznym:
- **Parafraza** — item eval może być przeformułowaniem czegoś z treningu; overlap n-gramowy tego nie wykryje.
- **Wspólne źródła publiczne** — generując polskie dane „od zera”, i tak czerpiemy z tej samej dystrybucji języka.
- **Bliźniaki w danych** — `seed_500_v2` i `variants_all` to warianty tego samego materiału; etykieta `eval-only` na pochodnej daje fałszywe poczucie czystości.

Pomiar to potwierdził. `contamination_check.py` uruchomiony na `test_verification.jsonl` względem `seed_500_training_final.jsonl` wykazał **90% skażonych itemów** (średni overlap n-gramowy 0.84, 60% near-verbatim) — mimo że oba pliki są „nasze, od zera”. Bez audytu ten plik zostałby użyty jako test i zawyżyłby wyniki. Deklaracja provenance zawiodła, problem wykrył dopiero pomiar.

Wniosek: sama etykieta `eval-only` w manifeście jest hipotezą, a nie gwarancją. Każda para trening↔eval wymaga obowiązkowego audytu i deduplikacji. Provenance działa tylko razem z pomiarem.

## Audyt overlapu n-gramowego

Każda para trening↔eval przechodzi audyt `contamination_check.py` przed wydaniem benchmarku. Procedura:

1. **Frakcja n-gramów (n=13, jak w Llamie):** odsetek okien itemu pokrytych przez dane treningowe; frakcja powyżej progu oznacza item skażony.
2. **Any-match i najdłuższy wspólny span (domyślna, ostrzejsza reguła):** jakiekolwiek trafienie 13-gramu (lub długi wspólny span) flaguje item. Ta reguła łapie wtopione kopie (np. skopiowaną odpowiedź w oryginalnym prompcie), które sama frakcja przepuszcza. (Poprawka Xaviera.)
3. **Near-verbatim (frakcja ≈ 1.0):** dosłowne kopie całych itemów są usuwane bezwzględnie.
4. **Deduplikacja pochodnych:** warianty (`v2`, `variants_all`) traktujemy jako ten sam item; nie rozdzielamy train/eval po wariantach.
5. **Bramka:** benchmark wychodzi dopiero przy **0% skażonych** itemów (zarówno według frakcji, jak i spanu).

Dlaczego audyt jest konieczny: `test_verification` względem `seed_500` daje przy regule any-match (n=13) **100% skażonych** itemów, ze spanem do **217 tokenów**, czyli całe itemy skopiowane. (Wcześniejszy pomiar podawał 90% skażonych według frakcji — zob. sekcję wyżej.) Demonstracja wtopionej kopii: dosłowny fragment 20 tokenów otoczony paddingiem daje frakcję 0.04, więc stary próg by go przepuścił, ale span 19 tokenów go wychwytuje. Audyt trwa 0.5 s.

Granica metody: n-gramy wykrywają dosłowność, a nie parafrazę czy podobieństwo semantyczne, więc zastrzeżenie z poprzedniej sekcji jest częściowo zasadne. Następnym krokiem jest overlap embeddingowy (sentence-transformers) jako druga warstwa — analogicznie do relewancji E5 w Dendrometrii.

## Ślepa wymiana zestawów

Benchmark zbudowany i oceniany przez ten sam team podlega prawu Goodharta: nieświadomie dopasowujemy model do własnego testu (podobnie jak cyrkularność E3 w Dendrometrii, gdzie proxy staje się wynikiem).

Rozwiązaniem jest drugi, niezależny team. On buduje benchmarki, których nigdy nie widzieliśmy, a my budujemy benchmarki dla niego. Wymieniamy się gotowymi zestawami. Testu, którego się nie zna, nie można ograć, więc wynik jest niezależnym ground truth, a nie autowalidacją.

Mechanizm:
- Team A i Team B trenują niezależnie; każdy zna tylko swoje dane treningowe.
- Benchmarki są krzyżowe: A ocenia modele B i odwrotnie.
- Wymiana odbywa się według `protokol/PROTOKOL-Wymiany.md` (commitment i jednorazowe ujawnienie).

Jest to uogólnienie metody M4 („AI-first-pass + human-ground-truth”): niezależną weryfikacją jest tu drugi team zamiast człowieka. Odpowiada też ślepemu re-review Xaviera, w którym ewaluator nie ma dostępu do „kluczy”.

## Benchmark spala się po ujawnieniu

Gdy team A przekazuje benchmark teamowi B, by ocenić modele B, zestaw przestaje być tajny. B, świadomie lub nie, może go wciągnąć do treningu następnej iteracji. Po jednej rundzie benchmark jest spalony, czyli staje się danymi treningowymi drugiej strony — to ten sam efekt „burned after exposure”, który dotyczy każdego ujawnionego tajnego zestawu.

Koszty: budowa świeżych zestawów na każdą rundę jest droga, rotacja zużywa zasoby obu teamów, a zaufanie („obiecuję, że nie trenowałem”) jest niefalsyfikowalne bez kontroli.

Bez protokołu ślepa wymiana działa tylko raz i degeneruje się w zwykły publiczny benchmark, który natychmiast ulega kontaminacji, a przewaga znika.

## Commitment przed ujawnieniem

Ślepa wymiana działa, jeśli benchmark jest jednorazowy i chroniony schematem commitment — nie polegamy na obietnicy „nie trenowałem”. Skrót protokołu (pełna wersja w `protokol/PROTOKOL-Wymiany.md`):

1. **Commit:** team A publikuje hash zestawu (SHA-256) i datę, zanim go ujawni. Treść pozostaje tajna.
2. **Jednorazowe ujawnienie:** A ujawnia zestaw tylko do jednej ewaluacji modeli B; B przeprowadza ewaluację i zwraca wyniki oraz odpowiedzi modelu.
3. **Spalony po użyciu:** ujawniony zestaw jest oznaczany w manifeście jako `spalony` i nigdy więcej nie służy jako eval (może jawnie trafić do treningu).
4. **Rotacja:** A utrzymuje pulę itemów; każda runda losuje świeży podzbiór, reszta pozostaje tajna.
5. **Audyt następnej iteracji:** przed kolejną rundą uruchamiamy `contamination_check.py` dla modelu B względem spalonych zestawów (sprawdzamy, czy B je wchłonął — jest to dopuszczalne, o ile nie trafiły do aktywnego evalu).

Dlaczego to działa:
- Hash dowodzi, że A nie podmienił zestawu pod wynik (ochrona przed Goodhartem po stronie autora).
- Jednorazowość sprawia, że spalenie jest zaplanowane, a nie przypadkowe; przewaga nie znika, tylko rotuje.
- Koszt rotacji jest realny, ale stanowi cenę niezależnego ground truth (podobnie jak koszt ślepego audytu w metodzie M4).

## Powiązane

[[BENCH-C1]] · [[../../protokol/PROTOKOL-Wymiany|protokół wymiany]] · [[../../protokol/PROVENANCE-Manifest|manifest provenance]] · [[../../tools/contamination_check.py|narzędzie]]
