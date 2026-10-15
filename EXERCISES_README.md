# Hvordan legge til egne øvelser

TouchPy støtter egendefinerte treningsfiler som kan legges til uten å bygge programmet på nytt.

## Innebygd øvelse: vanlige norske ord

Øvelsen `017_norwegian_common_words.txt` inneholder de 1 000 høyest rangerte
alfabetiske ordene i [FrequencyWords-listen for norsk (OpenSubtitles 2018)](https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/no/no_50k.txt).
Ordlisten er laget av hermitdave og innholdet er lisensiert under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Norsk tastaturstige

Øvelsene `018`–`033` gir en gradvis introduksjon til det norske tastaturet.
Bokstavøvelsene blander nye bokstaver med bokstavene fra tidligere trinn.
Bokstavene står samlet i varierende grupper på to, tre eller fire før et
mellomrom. Ordøvelsene bruker bare bokstaver som er introdusert til og med
trinnet.

Vanlige bokstaver kommer først, mens de sjeldne `q`, `w` og `z` introduseres
til slutt. Rekkefølgen er: hjemmeraden med `ø`, sammen med `e`, `i`, `r` og
`t`; deretter `n` og `m`; `u` og `y`; `o`, `p` og `å`; `æ`; `x` og `c`; `v`
og `b`; til slutt `q`, `w` og `z`. Det siste trinnet dekker hele alfabetet
og tar også i bruk komma, punktum og bindestrek.

## For brukere av .exe-filen

1. **Opprett en mappe** kalt `exercises` ved siden av `TouchPy.exe`:

   ```
   TouchPy/
   ├── TouchPy.exe
   └── exercises/          ← Opprett denne mappen
       ├── 018_min_tekst.txt
       └── 019_annen_tekst.txt
   ```

2. **Lag en .txt-fil** med følgende format:
   - **Valgfri første linje:** `Language: Norwegian` eller `Language: English` (velger tastaturoppsett).
   - **Neste linje (eller første hvis språk ikke er satt):** Tittel på øvelsen.
   - **Resten:** Selve teksten som skal skrives.

   **Eksempel 1 (Med språktagg):**

   ```
   Language: Norwegian
   Min egen øvelse
   Dette er teksten som eleven skal skrive.
   Den kan ha flere linjer.
   ```

   **Eksempel 2 (Uten språktagg - bruker standard engelsk):**

   ```
   My English Exercise
   This is the text to type.
   ```

3. **Start programmet** - dine øvelser vises automatisk i listen!

## Filnavn

- Bruk nummerering først for å kontrollere rekkefølgen: `018_`, `019_` osv.
- Filer sorteres alfabetisk etter filnavn
- Hvis du bruker samme nummer som en innebygd øvelse, overstyrer din fil den innebygde

## Tegnsett

- Bruk UTF-8 encoding (standard i Notepad/VS Code)
- Norske tegn (æ, ø, å) støttes fullt ut

## Tips

- Test øvelsen først i programmet før du deler den
- Hold tekstene kortere for bedre treningseffekt
- Bruk progressive øvelser som bygger på hverandre
- For litterære tekster: Bruk kun tekst som er fri for opphavsrett

## For utviklere (dev-modus)

I utviklermodus lastes øvelser fra:

1. `typing_trainer/exercises/` (innebygde øvelser)
2. `exercises/` i prosjektmappa (eksterne/test-øvelser)

Ekstern mappe prioriteres hvis samme filnavn brukes begge steder.
