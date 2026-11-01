# Laborator 2: Sistem de recomandare cu Recombee - înregistrare proprietăți

## Dataset

- **Domeniu:** filme
- **Sursă:** [IMDB 5000 Movie Dataset (Kaggle)](https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset)
- **Fișier:** `movie_metadata.csv`
- **Dimensiune:** 5043 de intrări (între 100 și 10K, conform cerinței), 28 de coloane

Fiecare rând descrie un film: titlu, regizor, actori, genuri, buget, încasări, scor IMDB etc.

## Proprietăți înregistrate în Recombee

Din cele 28 de coloane ale datasetului, am înregistrat 8 proprietăți în baza de date Recombee `sdr-movies-dev`:

| Proprietate | Tip Recombee | Descriere |
| --- | --- | --- |
| `movie_title` | string | Titlul filmului |
| `director_name` | string | Numele regizorului |
| `title_year` | int | Anul apariției |
| `duration` | int | Durata în minute |
| `imdb_score` | double | Scorul IMDB (0-10) |
| `language` | string | Limba filmului |
| `country` | string | Țara de producție |
| `content_rating` | string | Clasificarea de vârstă (PG-13, R etc.) |

Identificatorul unic al filmului (de exemplu `movie_imdb_link`) nu este înregistrat ca proprietate. Recombee îl gestionează nativ ca `itemId`, iar acesta va fi folosit la încărcarea itemilor, în laboratorul următor.

## Fișiere

- `recombee_properties.py` - scriptul care citește datasetul, definește proprietățile în Recombee și le listează pentru verificare
- `movie_metadata.csv` - datasetul folosit

## Rulare (Linux)

```
pip install recombee-api-client pandas
export RECOMBEE_PRIVATE_TOKEN="tokenul_tau"
python recombee_properties.py
```

Tokenul privat Recombee se citește din variabila de mediu `RECOMBEE_PRIVATE_TOKEN` și nu este salvat în cod.
