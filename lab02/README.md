# Laborator 2: Recombee - înregistrare proprietăți

## Dataset

**Domeniu:** filme.
**Sursă:** [IMDB 5000 Movie Dataset (Kaggle)](https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset)
**Fișier:** `movie_metadata.csv` (5043 de intrări, 28 de coloane)

Fiecare rând descrie un film: titlu, regizor, actori, genuri, buget, încasări, scor IMDB etc.

## Proprietăți înregistrate în Recombee

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

Identificatorul unic al filmului (de ex. `movie_imdb_link`) nu este proprietate; va deveni `itemId` la încărcarea itemilor.

## Rulare

```
pip install recombee-api-client pandas
export RECOMBEE_PRIVATE_TOKEN="tokenul_tau"      
# Windows PowerShell: 
$env:RECOMBEE_PRIVATE_TOKEN="tokenul_tau"
python recombee_properties.py
```