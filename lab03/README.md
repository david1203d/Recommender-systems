# Laborator 3: Sistem de recomandare cu Recombee - trimitere items

În acest laborator am populat catalogul din Recombee (baza `sdr-movies-dev`) cu filmele din datasetul folosit la Laboratorul 2. Proprietățile (coloanele catalogului) fuseseră definite deja la Laboratorul 2.

## Dataset

- **Domeniu:** filme
- **Sursă:** [IMDB 5000 Movie Dataset (Kaggle)](https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset)
- **Fișier:** `movie_metadata.csv` (5043 de rânduri în fișierul original)

## Pregătirea datelor

- **ID-ul unic (`itemId`):** codul IMDB al filmului (de exemplu `tt0499549`), extras din coloana `movie_imdb_link` cu o expresie regulată. Linkul întreg nu a fost folosit, pentru că conține și parametri inutili (`?ref_=...`).
- **Duplicate:** același film apărea de mai multe ori în fișier. După extragerea ID-ului au fost eliminate 124 de rânduri duplicate (se păstrează prima apariție), rămânând **4919 filme unice**.
- **Valori lipsă:** dacă un film nu are valoare pentru o proprietate (de exemplu `content_rating`), proprietatea respectivă nu se trimite pentru acel film.
- **Curățare text:** titlurile conțineau spații nesecabile la final (de exemplu `Avatar `), care au fost eliminate.

## Proprietăți trimise

| Proprietate | Tip Recombee | Coloana din CSV |
| --- | --- | --- |
| `movie_title` | string | `movie_title` |
| `director_name` | string | `director_name` |
| `title_year` | int | `title_year` |
| `duration` | int | `duration` |
| `imdb_score` | double | `imdb_score` |
| `language` | string | `language` |
| `country` | string | `country` |
| `content_rating` | string | `content_rating` |

## Trimiterea item-urilor

Scriptul `recombee_items.py` creează câte un request `SetItemValues` pentru fiecare film (cu `cascade_create=True`, deci item-ul se creează dacă nu există) și le trimite în **loturi de 100** folosind `Batch`, în loc de un request HTTP pentru fiecare film. Răspunsul fiecărui request din lot este verificat, iar erorile sunt afișate.

## Rulare (Linux)

export RECOMBEE_PRIVATE_TOKEN="tokenul_tau"
python recombee_items.py


Tokenul privat Recombee se citește din variabila de mediu `RECOMBEE_PRIVATE_TOKEN` și nu este salvat în cod.

## Rezultat

Datele au fost încărcate cu succes în Recombee: în *Admin UI* → *Catalog* → *Items* apar cele 4919 de filme, cu proprietățile completate.