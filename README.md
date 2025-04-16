# Kävelypäiväkirja

Sovelluksen tämän hetkinen tilanne:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään sovellukseen päivityksiä kävelyistään: matkan pituus, kaupunki ja reitin/päivityksen nimi sekä kuvaamaan kävelyään. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään päivityksiä.
- Käyttäjä näkee sovellukseen lisätyt päivitykset. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät päivitykset.
- Käyttäjä pystyy etsimään kävely-päivityksiä hakusanalla, joka etsii hakusanaa otsikosta ja kuvauksesta(description). Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä päivityksiä.
- Käyttäjä pystyy liittämään kuvia päivitykseen.
- Käyttäjä pystyy kommentoimaan toisten käyttäjien (ja omaan) päivitykseen.
- Käyttäjä pystyy valitsemaan eri luokkia päivitykselleem: sää, kävelyn onnistuminen ja kävelyn tyyli.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät tietokohteet.
  
Käyttöohjeet:
- python -m venv venv
- pip install flask

- git clone https://github.com/unnamant/Kavelypaivakirja
- cd Kavelypaivakirja
- flask run
