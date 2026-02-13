# Hvordan legge til egne øvelser

TouchPy støtter egendefinerte treningsfiler som kan legges til uten å bygge programmet på nytt.

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
   - **Første linje:** Tittel på øvelsen
   - **Resten:** Teksten som skal skrives

   **Eksempel** (`018_min_tekst.txt`):

   ```
   Min egen øvelse
   Dette er teksten som eleven skal skrive.
   Den kan ha flere linjer.
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
