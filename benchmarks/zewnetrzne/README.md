# benchmarks/zewnetrzne — zestawy zewnętrzne (poza kontraktem Probierza)

> ⚠️ To **nie są benchmarki Probierza.** Są to publiczne zestawy cudzego autorstwa, których używamy do
> porównań z innymi pracami (np. polska oś wiedzy w kartach modeli). Nie spełniają kontraktu z
> głównego README: nie mają manifestu provenance po naszej stronie, nie przeszły audytu kontaminacji
> z wynikiem 0 % (dla publicznych tekstów z internetu nie da się tego zagwarantować) i nie są
> jednorazowe. Wynik na nich mówi, jak model wypada na znanym teście, a nie czy zdolność jest „czysta”.

Zasady dla tego katalogu:

1. **Danych nie kopiujemy.** Każdy zestaw jest pobierany z przypiętej rewizji źródła i sprawdzany po
   sha256 — każdy liczy na tych samych bajtach, a licencję i autorstwo trzyma źródło.
2. **Protokół jest jawny i jeden.** Skrypt w katalogu zestawu to dokładnie ten pomiar, który
   publikujemy; README podaje kalibrację (model, rewizja, oczekiwany wynik), żeby dało się sprawdzić zgodność.
3. **Kontaminacja jest opisana, nie wykluczona.** Jeśli znamy pytania, które trafiły do korpusu
   któregoś z naszych modeli, README zestawu to mówi.

| zestaw | co mierzy | źródło |
|---|---|---|
| [`arc-easy-pl/`](arc-easy-pl/) | ARC-Easy po polsku (2376 pytań wyboru, wiedza szkolna) | `Eurolingua/arcx` (+ kontrolnie `ddudek/ai2_arc_translated_pol`) |
| [`byte-ppl-w-pl/`](byte-ppl-w-pl/) | byte-PPL na 463 artykułach polskiej Wikipedii (kolumna W / byte-PPL PL na track.fabryka.ai) | `SlayerLab/fabryka-track-w-pl` |
