# Elite Speedsolvers Analysis
##### Projektna naloga pri predmetu Programiranje 1 na Fakulteti za matematiko in fiziko. Vključuje zajem podatkov in njihovo analizo.

***

## Zajem podatkov

Podatki so zajeti s spletne strani [World Cube Association](https://www.worldcubeassociation.org/). Tam se nahajajo informacije vseh tekmovanj, ki so bila izvedena v okviru zveze WCA. 

Zajem izvaja skripta `skripta.py`.  

V repozitoriju najdemo podatke v mapi `data/`. Shranjeni so v dveh oblikah, `.json` in `.csv`, vsebina obeh datotek pa je enaka.  

Datoteka `333.csv` vsebuje podatke prvih 10000 tekmovalcev v disciplini 3x3x3 Cube, razvrščenih po povprečju (average). Za vsakega tekmovalca imamo sledeče podatke:
* Podatki o tekmovalcu:
  * WCA ID,
  * ime,
  * narodnost,
  * spol,
  * izkušenost (število preteklih tekmovanj).
* Podatki o tekmovalčevem dosežku:
  * rezultat (povprečje),
  * tekmovanje,
  * leto doseženega rezultata,
  * velikost tekmovanja (z doseženim rezultatom).

Datoteka `multi.csv` vsebuje podatke prvih 2000 tekmovalcev v disciplini Multiple Blindfolded.
Za vsakega tekmovalca imamo enake podatke kot pri datoteki `333.csv`, poleg tega pa še:
* rezultat je razbit na rezultat, točke rezultata in čas rezultata;
* dodano je tekmovalčevo povprečje 3x3x3 in njegova svetovna uvrstitev v tej osnovni disciplini.

***

## Analiza podatkov

Analiza se nahaja v datoteki `analiza_podatkov.ipynb`.

Cilj analize je odgovoriti na naslednja vprašanja:
* Kako "izkušenost tekmovalca" (tj. število preteklih tekmovanj) vpliva na njegovo uvrstitev?
  * Al so izkušenejši tekmovalci vedno boljši?
* Kako se rezultati spreminjajo, ko se sprehajamo od boljših proti slabšim tekmovalcem?
  * Ali stroga elita močno odstopa od ostalih?
* Kdaj so bili doseženi najboljši rezultati?
  * Ali so tisti izpred nekaj let še aktualni?
  * Kako tukaj vidimo razliko med disciplinama?
* Kakšna je razporeditev najboljših tekmovalcev po spolu?
  * Ali so ženske enakovredne moškim?
* Kako velikost tekmovanja vpliva na rezultate?
  * Ali lokalno tekmovanje pomeni manjši pritisk za tekmovalce?
* Katere države dosegajo največ najboljših rezultatov?
  * Ali obstajajo velesile?
  * Kje se nahajamo Slovenci?
* Ali obstaja povezava med dobrimi tekmovalci v Multiple Blindfolded in njihovim 3x3x3 povprečjem?