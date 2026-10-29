# N05-50 v0.3 — 50 różnych benchmarków, nie wariantów

Autor metody i werdyktu: Mierniczy N-05. Zlecenie Arka z 2026-10-28 22:12:48Z, doprecyzowanie 2026-10-29 02:24:04Z: **50 różnych benchmarków**. Stan: dobór i źródła zdefiniowane przed pomiarami; nie odbiór danych, wykonawcy ani wyników modeli.

## 1. Jedno źródło listy i czyste przejście

- `tasks_50_v01.json` jest aktywnym rejestrem **N05-50-v0.3**: dokładnie 50 unikalnych `benchmark_id`, jeden główny protokół na benchmark. Nazwa pliku pozostaje stabilna dla odsyłaczy; wersję określa zawartość i pełny pin.
- `benchmark_sources_v03.json` wiąże te same identyfikatory z konkretnymi definicjami, członkami grup, datasetami, rewizjami i zaobserwowanymi deklaracjami licencji. To ledger źródeł, nie druga lista wyboru ani receipt danych.
- `results.schema.json` zachowuje układ wire-formatu `schema_version=1`, ale dopuszcza wyłącznie identyfikatory wykonania `N05-50-v0.3-panel200` i `N05-50-v0.3-fullB`. `inventory_commit` musi mieć pełne 40 hex. Przykład kontraktu pozostaje jawnie `contract_example`, nie pomiarem.
- Wydanie podaje pełny commit rejestru i SHA plików w osobnym `release_v03.json`; źródło rejestru nie odwołuje się cyklicznie do własnego SHA.

Stare 50 wierszy/36 etykiet family **nie realizowało nowego wymagania**. Historia v0.2, jej numeryczne konwencje i raporty pozostają w commitcie `396a4bc1` i wcześniejszych pinach. Nie konwertujemy starych wyników przez zmianę etykiety: T01–T50 mają nowy kontrakt, a T50 oznacza teraz ReCoRD, nie EQ-Bench. Nie ma aliasu przyjmującego pakiet v0.2 jako v0.3. Stary `openpl_sources_v01.json` zastępuje nowy ledger wszystkich źródeł.

## 2. Co uznajemy za odrębny benchmark

Liczymy nazwaną, źródłowo zidentyfikowaną kolekcję zadań, nie unikalną nazwę YAML. MC/regex/generacja, języki przekładu, liczby demonstracji, rundy i splity nie zwiększają licznika. ARC, ANLI i PoLEMo2 są liczone raz; rejestr jawnie wybiera główny protokół/zakres. MMLU, BLiMP, MATH i BBH są liczone po jednym, nie po jednym na podzadanie. GLUE/SuperGLUE nie są dopisywane ponad odrębne źródłowe datasety składowe.

QNLI nie jest dodatkowym źródłem obok SQuAD; MMLU-Pro/SR nie są dodatkami obok MMLU; MATH500/Minerva nie są dodatkami obok MATH. SWAG pominięto konserwatywnie wobec wspólnej puli kontekstów HellaSwag. Samo wspólne medium, np. Wikipedia lub artykuły RACE użyte przez CoQA, nie oznacza identycznej kuracji pytań; takie pokrycie jest nazwane, nie przedstawiane jako dowód statystycznej niezależności.

Oryginalne zlecenie nie narzucało 25PL/25EN. Dobór zachowuje rzeczywiste polskie źródła, lecz nie wypełnia parytetu wariantami. Dokładne liczebności, domeny i języki są w rejestrze. Pięćdziesiąt odrębnych kolekcji nie oznacza pięćdziesięciu niezależnych dowodów ani pięćdziesięciu wykonanych pomiarów.

Funkcjonalny kod wygenerowany przez model oraz benchmarki narzędziowe/agentowe nie są tu zastępowane atraptą graderów. HumanEval/MBPP wymagają osobnego zaakceptowanego sandboxu; agentowe eksperymenty Collective mają własny protokół. Nie liczymy tych brakujących ścieżek do wykonywalnej baterii.

## 3. Modele, środowiska i tożsamość wykonania

Porównanie dotyczy Slayer1B-1.06, dokładnego Bielik-1.5B-v3 oraz LFM2.5-1.2B-Base, bez zamieniania gated modelu na inną wersję lub instruct. Brak dostępu do Bielika jest `blocked_access`, nie zerem. Dostępne modele można przygotowywać i kalibrować niezależnie; nie dopisujemy później innego zestawu źródłowych ID do istniejącego sparowanego wyniku.

EN: `6d2abda4fd171e68a8789330c4149e37c1ca0bda`. PL: `21d0ea9cf4fd6153dfff4d84d6ad0aab5488f302`. Dwa odrębne venv/procesy. Ledger przypina dokładne bajty deklaracji z kanonicznych checkoutów i lokalną definicję `tasks/llmzszl.yaml`. Nie normalizujemy hashów w trakcie biegu. Kod callbacków, cały wheel harnessu, zależności i zasoby metryk są częścią odrębnego związanego runtime, nie dowodem wynikającym z samych SHA YAML.

Panel: float32, eval/inference, batch1, max_length4096, bez automatycznego BOS/chat-template. Zachowujemy odebraną semantykę numerycznego komponentu82; nowy pin musi jawnie przyjąć v0.3 i zachować weryfikowany cały komponent/import provenance. Raportujemy rzeczywiste wersje, urządzenie i ustawienia backendu, bez cichego przełączania precyzji po pomiarze tempa. Seedy harnessu `(python,numpy,torch,fewshot)=(0,1234,1234,1234)`; seed selekcji 20261028 jest inną osią.

Cały komponent modelu jest sprawdzany przed importem, z jawnym pochodzeniem modułów; `execution.json` zachowuje manifest i faktyczne `lm.provenance`. Deklarowany model/weights SHA musi zgadzać się z weryfikowanymi wejściami, bez ponownego czytania wag tylko dla metadanych. Odbiór tekstowych ścieżek82 z raportu N26 `ec1f5f63` nie jest kalibracją1B/GPU ani akceptacją nowego całego producenta.

## 4. Jednostka, panel200 i grupy

Jednostką jest oryginalny dokument po źródłowym `process_docs`, nie arbitralny wiersz requests lub token. Złożona tożsamość zachowuje `benchmark_id`, źródłowego członka/task i jego rzeczywisty identyfikator albo hash kanonicznego oryginalnego dokumentu. Nie używamy indeksu pętli jako rzekomego source_id. Równość i parowanie sprawdzamy po jawnych ID/treści, nie po samym n ani kolejności listy.

Dla benchmarku wybieramy `min(200,N_eligible)` przed modelami według SHA256 `20261028|benchmark_id|member_task|source_id`, z deterministycznym tie-breakiem kanonicznych bajtów. `N_eligible` jest ustalone po wymaganych wyłączeniach supportu i zatwierdzonych wyłączeniach kontaminacji; raport zawiera również pierwotną liczebność i przyczyny wyłączeń. Wszystkie porównywane modele mają ten sam wybrany zbiór ID. Digest parowania obejmuje kanonicznie posortowane złożone ID, bez zmiany źródłowej kolejności wykonania; kanoniczny JSON UTF-8 ma sort_keys, ensure_ascii=False, separators(',',':'), bez końcowego LF, jak prymitywy producenta.

**200 dotyczy całego benchmarku, nie każdego członka grupy.** BLiMP ma 67, MMLU57, MATH7, BBH27 źródłowych członków. Każdy otrzymuje najpierw `min(2,N_i)` dokumentów. Pozostałe sloty przydzielamy dostępnym członkom po największym deficycie `budget*source_weight - allocated`, remis po nazwie tasku, nigdy ponad jego populację. Jeżeli wymagany członek jest pusty albo minimalny przydział nie mieści się w budżecie, jest jawny błąd, nie usunięcie podzadania.

Wagi pozostają źródłowe: BLiMP równo po członkach; MMLU/MATH/BBH proporcjonalnie do zamrożonych kwalifikujących populacji członków. Po źródłowym scoringu ponownie składamy ich metryki z tymi STAŁYMI wagami, nie z przypadkowych liczebności próby. Manifest zapisuje wszystkie `N_i`, przydziały, wagi i ID. Warianty/inne członki nie produkują dodatkowych głównych wierszy wyników.

WikiText-2 jest wyjątkiem: pełny źródłowy strumień testowy, prawidłowo ważone `byte_perplexity`, nie średnia perplexity dokumentów ani konwersja Glint `tp^(N/B)`. Porównanie pozostaje opisowe. Starej krzywej historycznej nie przepisujemy na tę nową miarę.

`fullB` jest osobnym pełnym odczytem wybranych tutaj primary-protocols, bez limitu200 i bez zwiększania licznika benchmarków. Zachowuje źródłowe samplery/strumienie fewshot oraz wymaga osobnego odebranego source-protocol/runtime receipt: kontekst, precyzja, kolejność, demo ID i rzeczywiste self-exclusion muszą być znane przed biegiem. Nie przenosi automatycznie hash-banku ani przydziału panelu. Nie jest dawną replikacją23 definicji OpenPL i nie daje automatycznej porównywalności z zewnętrzną tabelą pełnych wyników.


## 5. Demonstracje, kontekst i brak cichych zmian

Liczba demonstracji jest jawna w rejestrze. Dla pul danych panel używa rozłącznego banku wymaganej wielkości wybranego hashem `20261028|benchmark_id|member_task|support|source_id`; źródłowy split jest zachowany, a fallback jest nazwany. Gdy źródło ma stałe próbki fewshot w definicji, np. BBH, zachowujemy te próbki i ich kolejność zamiast dorzucać bank z testu. Dopasowane pytanie demonstracyjne jest wyłączone z puli punktowanej. Stałe źródłowe preambuły nie są usuwane ani udawane jako dodatkowe benchmarki.

Przy każdym scored ID zapisujemy num_fewshot, rzeczywiste demo ID/pochodzenie, actual_shots, removed_demo_ids, hash kontekstu i rozmiary tokenów. Rezerwa generacji pochodzi z tasku, domyślnie256; IFEval jawnie1280. Jeśli prompt+rezerwa nie mieści się w4096, usuwamy opcjonalne demonstracje od końca. Nie tniemy pytania/opcji/referencji, nie wybieramy nowego łatwiejszego dokumentu po wyniku. Brak miejsca bez demonstracji jest jawnym błędem i nie może zostać nazwany ukończonym panelem200.

Tekst generacji ma source-HFLM skip_special_tokens=True, rawEOS osobnoFalse; until stosuje źródłową kolejność i kolejne split bez globalnego earliest/strip. Oryginalne filtry zadania są wykonywane po tym tekście. NQ/TriviaQA używają rzeczywistego filtra `remove_whitespace`; nie wymyślamy `none`. Nowy MultiBLiMP zachowuje osobny jawny parowy scoring ze źródłowym prefiksem spacji, bez przenoszenia go na inne benchmarki lub usuwania niepasujących tokenów po cichu.

## 6. Metryki i porównania

Każdy benchmark ma JEDNĄ z góry wskazaną główną metrykę/filtr/jednostkę/kierunek, identyczne dla stanów ok i braków. Wszystkie oryginalne metryki pomocnicze pozostają w prywatnych artefaktach. Surowe miary zachowują skalę: nie mnożymy całego lm-eval przez100. CoLA MCC może być ujemne; TruthfulQA MC2 to masa prawdopodobieństwa, nie MC1; PSC to matching, nie generatywne streszczanie; KLEJ-NER to klasyfikacja zdania, nie span-F1. Nie ma średniej z50 nieporównywalnych jednostek ani chance-normalized rankingu po fakcie.

Baseline referencyjny: Slayer kontra każdy dostępny, dokładnie wskazany model obcy, per benchmark. Dla par wymagane te same źródłowe ID/targety, benchmark/member weights, data/protocol i odebrany runtime; samo równe n/digest lub zgodny kształt tablic nie wystarcza. Przy n_scored mniejszym od ustalonej próby nie udajemy pełnych200.

Na sparowanych per-item wynikach: opisowy paired-bootstrap CI95, 10000 replik/seed20261028; w grupach resampling wewnątrz członków z zachowanymi wagami. Nieaddytywne F1/MCC i ważone miary przeliczamy źródłową agregacją, nie średnią z już zagregowanych liczb. Dwustronny paired permutation/swap10000 z +1 correction; Holm alpha0.05 dla maksymalnie98 z góry zadeklarowanych kontrastów (49 poza opisowym Wiki ×2 referencje). Brakujące/nieporównywalne kontrasty są jawnie withheld, nie sukcesem ani zerowym p; nie wybieramy korzystniejszej rodziny po obejrzeniu wyników. Małe próby w niektórych członkach ograniczają rozdzielczość; CI opisowy nie gwarantuje mocy ani równoważności.

Werdykt better/worse wymaga prawidłowego kierunku, spełnionego z góry kryterium p_Holm i niezależnie odebranego rekordu z actor/artifact SHA. Inconclusive oznacza brak wykazanego kierunku w tym badaniu, nie remis lub dowód równoważności. Renderer nie liczy statystyki i nie nadaje accepted.

## 7. Dane, licencje i zasoby przed pierwszym odczytem modeli

Każdy benchmark wskazuje zaobserwowane deklaracje licencji i pełną rewizję karty w rejestrze; dokładne źródła są w ledgerze. SHA repo Hub nie jest dowodem byte-readback zewnętrznych plików dataset scriptu. Każdy run wymaga osobnych raw-file SHA/rozmiarów, procesu transformacji, cech/splitów i source_id. Nie uruchamiamy Hub dataset builders/TRC: źródłowy Task dostaje zatwierdzone lokalne dane. Preprocessing nie może tworzyć nieprzypiętego cache wewnątrz zaakceptowanej paczki ani gubić późniejszych pól JSON.

Tag NC, other lub brak tagu nie jest automatycznym zezwoleniem. N04 kwalifikuje konkretny cel wewnętrznej ewaluacji i możliwość eksportu samych agregatów; to nie trening ani redystrybucja pytań. Do rozstrzygnięcia bramki dane nie są dopuszczone. Jeśli użycie jest niedozwolone, pozycję zastępujemy przed pomiarami nowym jawnym pinem, nadal zachowując50 odrębnych źródeł. Nie wypełniamy braków syntetycznym wynikiem.

Dla każdego nowego źródła obowiązuje przywiązany do rewizji skan kontaminacji wobec naszych wsadów. LLMzSzŁ ma zgłoszone pokrycie treningowe: wymaga zgodności rewizji/ID z audytem; nie przenosimy automatycznie dawnych liczników. Czyste wyłączenia stosuje się do TEGO SAMEGO panelu wszystkich modeli. Pełny wynik z pokryciem może być tylko odrębnie oznaczoną diagnostyką, nie niejawnie czystym primary.

Wszystkie metryki, NLTK i tokenizery są przypięte/cachowane przed importami. IFEval wymaga langdetect/immutabledict i read-only punkt_tab przez NLTK_DATA; brak zasobu ma zatrzymać przed importem, nie pobrać w biegu. SQuAD2 wymaga przejrzanego, przypiętego lokalnego modułu evaluate squad_v2. Sieć i tokeny HF wyłączone w wykonaniu; cache zadeklarowany w rodzicu i przekazany do potomka.

## 8. Rozdzielenie odbiorów i ukończenia

N05 prowadzi dobór/protokół i werdykt, N03 producenta/materializację, N02 modele/runtime, N26 niezależną poprawność, N04 kod/dane/egress, N14 zasoby i transport. Żaden odczyt źródeł, test z syntetyczną odpowiedzią, gotowy renderer lub receipt CPU nie jest wynikiem jakości modeli.

Przed właściwym biegiem: nowy pin producenta obsługujący grupy, legacy Task SQuAD2, lokalny YAML i nowy rejestr; manifest całego komponentu, pełne40hex, faktyczne lm.provenance; źródłowe/raw/processed/freeze manifests; wszystkie niezależne bramki. Żadnych strażników po dawnym T50/EQ lub dawnych T01–T05 zamiast bieżącego benchmark_id/kind.

Na uprawnionym hoście wymagany rzeczywisty pilot checkpointów: logity/LL oraz reprezentatywna GENERACJA i koszt fan-out wyborów. Tempo LL/natywnego HFLM nie jest wyceną generacji Slayera z pełnym prefiksem w każdym kroku. Ustawień/metody nie stroimy na quality z main; pilot nie jest ukończoną50. START/operator/zegar i rezerwa finansowa należą do osobnego uzgodnionego handoffu; większa karta nie podnosi limitu kontekstu ani nie przenosi GREEN A100 na B300.

`ok` wymaga rzeczywistego pomiaru, n_scored>0 i kompletu digestów. not_run/blocked_access/blocked_runtime/blocked_security/unsupported/failed/skipped zachowują value=null/ci95=null. Prawdziwe0 nie jest brakiem. Osiągnięcie50 identyfikatorów w tym rejestrze jest końcem DOBORU, nie dowodem50 ukończonych benchmarków na modelu.
