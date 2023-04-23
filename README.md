# Tsoha opetussovellus
## Aihe
Tarkoituksena on tehdä esimerkkiaiheen mukainen opetussovellus.

Siis sovelluksen täytyy...
* mahdollistaa opettaijien ja oppilaiden sisäänkirjautuminen
* luoda kursseja
* luoda kurssimateriaaleja
* luoda automaattisesti tarkistettavia harjoituksia
* tehdä harjoituksia
* muodostaa yhteenveto ja tilastoja käyttäjän kursseista
* antaa mahdollisuus luoda ja muokata kurssimateriaaleja

---
## Nykyinen tilanne


Sovellukseen pystyy nyt kirjautumaan sisälle ja opettajat pystyvät luomaan kursseja sekä katsomaan olemassa olevia kursseja.
Kursseille voi luoda lukuja ja luvuille voi luoda tehtäviä.

---

## Sovelluksen kokeileminen
Sovellusta voidaan testata ajamalla app.py -tiedosto src -kansiossa flaskilla.
Sovellus tarvitsee python-paketit, jotka on määritelty requirements.txt-tiedostossa. 
Ympäristömuuttujien DATABASE_URL ja SECRET_KEY täytyy olla määriteltyjä. Tarvitaan vielä tietokanta, jonka taulut on alustettu schema.sql -tiedoston avulla.