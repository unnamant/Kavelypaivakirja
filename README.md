# Kävelypäiväkirja

Sovelluksen tämän hetkinen tilanne:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy poistamaan tilinsä ja sillä tehdyt ilmoitukset.
- Käyttäjä pystyy lisäämään sovellukseen päivityksiä kävelyistään: matkan pituus, kaupunki ja reitin/päivityksen nimi sekä kuvaamaan kävelyään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään päivityksiä.
- Käyttäjä näkee sovellukseen lisätyt päivitykset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät päivitykset.
- Käyttäjä pystyy etsimään kävely-päivityksiä hakusanalla, joka etsii hakusanaa otsikosta ja kuvauksesta(description). Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä päivityksiä.
- Käyttäjä pystyy liittämään kuvia päivitykseen.
- Käyttäjä pystyy kommentoimaan toisten käyttäjien (ja omaan) päivitykseen.
- Käyttäjä pystyy valitsemaan eri luokkia päivitykselleen: sää, kävelyn onnistuminen ja kävelyn tyyli.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tietokohteet.
- Sovelluksessa on CSFR-tokenit.
- Sovelluksessa pystyy tekemään rivinvaihtoja kuvaukseen.
- Salasanassa vaaditaan 8 merkkiä, ja tunnuksen tulee olla alle 20 merkkiä
  
 ## Sovelluksen asennus ja käyttöohjeet:
 
Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
```
```
$ sqlite3 database.db < init.sql
```
Käynnistä sovellus komennolla:
```
$ flask run
```
