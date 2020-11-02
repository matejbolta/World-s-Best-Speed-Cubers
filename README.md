Elite Speedsolvers Analysis
=========================
Projektna naloga pri predmetu Programiranje 1 na Fakulteti za matematiko in fiziko.

Analiziral bom podatke s spletne strani [World Cube Association](https://www.worldcubeassociation.org/). Tam se nahajajo podatki z vseh tekmovanj, ki so bila izvedena v okviru WCA zveze.

Podatki s shranjeni v datotekah `333.csv` in `multi.csv`.

Datoteka `333.csv` vsebuje podatke prvih 10000 tekmovalcev v disciplini 3x3x3 Cube, razvrščenih po povprečju (average).
Za vsakega tekmovalca imamo podatek o:
* ranku,
* imenu tekmovalca,
* rezultatu (povprečju),
* narodnosti,
* tekmovanju,
* letu doseženega razultata,
* wca id-ju,
* spolu,
* številu preteklih tekmovanj tekmovalca,
* velikosti tekmovanja (s tem doseženim rezultatom).

Datoteka `multi.csv` vsebuje podatke prvih 2000 tekmovalcev v disciplini Multiple Blindfolded.
Za vsakega tekmovalca imamo enake podatke, kot pri datoteki `333.csv`, poleg tega pa še:
* rezultat je razbit na rezultat, točke rezultata in čas rezulata
* dodano je 333 povprečje tekmovalca in njegov svetovni rank v tej (osnovni) disciplini

Moje delovne hipoteze:
* Katere države so najboljše v klasični 3x3x3 disciplini?
* Kako "izkušenost tekmovalca", ter število preteklih tekmovanj vpliva na njegov rank?
* Ali so vsi najboljši časi že stari, ali se vrh lestvice stalno spreminja (vpliv leta doseženega rezulatata na rank)?
* Kakšna je slovenska zasedba v svetovnem merilu?
* Vpliv spola na rankiranje?
* Vpliv velikosti tekmovanja na rankiranje?
* Kako 3x3x3 rezultat vpliva na ostale discipline (konkretno 3x3x3 Multi-Blind)?