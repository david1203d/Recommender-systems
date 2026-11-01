import os
import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# TODO 1: Configurare credentiale Recombee (la fel ca la Lab 02)
# Tokenul se citeste din variabila de mediu, ca sa nu ajunga in repository.
DB_NAME = 'sdr-movies-dev'
PRIVATE_TOKEN = os.environ.get('RECOMBEE_PRIVATE_TOKEN', 'tokenul_tau_privat')
REGION = Region.EU_WEST  # versiunile noi ale SDK-ului cer enum, nu text

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=REGION)

# TODO 2: Incarcarea aceluiasi dataset folosit la Lab 02
PATH_DATASET = 'movie_metadata.csv'

BATCH_SIZE = 100


def clean_text(value):
    """Curata un text (elimina spatiile, inclusiv cele nesecabile din titluri). Intoarce None daca lipseste."""
    if pd.isna(value):
        return None
    text = str(value).replace('\xa0', ' ').strip()
    return text if text else None


def prepare_dataset():
    """Citeste CSV-ul, extrage ID-ul unic si elimina duplicatele."""
    df = pd.read_csv(PATH_DATASET)
    print(f"Dataset citit: {len(df)} randuri.")

    # ID-ul unic: codul IMDB din link (ex.: tt0499549), nu link-ul intreg
    df['item_id'] = df['movie_imdb_link'].str.extract(r'(tt\d+)', expand=False)
    df = df.dropna(subset=['item_id'])

    # Acelasi film poate aparea de mai multe ori; pastram prima aparitie
    inainte = len(df)
    df = df.drop_duplicates(subset='item_id', keep='first')
    print(f"Au fost eliminate {inainte - len(df)} duplicate. Raman {len(df)} item-uri.")
    return df


def build_properties(row):
    """Construieste dictionarul de proprietati pentru un rand. Valorile lipsa (NaN) nu se trimit."""
    properties = {
        "movie_title": clean_text(row['movie_title']),
        "director_name": clean_text(row['director_name']),
        "title_year": None if pd.isna(row['title_year']) else int(row['title_year']),
        "duration": None if pd.isna(row['duration']) else int(row['duration']),
        "imdb_score": None if pd.isna(row['imdb_score']) else float(row['imdb_score']),
        "language": clean_text(row['language']),
        "country": clean_text(row['country']),
        "content_rating": clean_text(row['content_rating']),
    }
    return {k: v for k, v in properties.items() if v is not None}


def send_batch(requests):
    """Trimite un lot si verifica rezultatul fiecarui request din el. Intoarce numarul de erori."""
    raspunsuri = client.send(Batch(requests))
    erori = 0
    for cerere, raspuns in zip(requests, raspunsuri):
        if raspuns.get('code') not in (200, 201):
            erori += 1
            print(f"Eroare la item-ul {cerere.item_id}: {raspuns}")
    return erori


def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = prepare_dataset()
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []
    total_trimise = 0
    total_erori = 0

    for index, row in df.iterrows():
        # TODO 3: ID-ul unic al produsului (codul IMDB extras din movie_imdb_link)
        item_id = str(row['item_id'])

        # TODO 4: Maparea proprietatilor definite la Lab 02 cu valorile din randul curent
        properties = build_properties(row)

        # SetItemValues creeaza automat item-ul daca acesta nu exista
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) pentru eficienta
        if len(requests) == BATCH_SIZE:
            total_erori += send_batch(requests)
            total_trimise += len(requests)
            requests = []
            print(f"S-au trimis {total_trimise} item-uri...")

    # Trimitem si restul ramas (daca numarul total nu e multiplu de BATCH_SIZE)
    if requests:
        total_erori += send_batch(requests)
        total_trimise += len(requests)
        print(f"S-a trimis ultimul lot. Total: {total_trimise} item-uri.")

    if total_erori == 0:
        print("Toate item-urile au fost trimise cu succes!")
    else:
        print(f"Atentie: {total_erori} item-uri au avut erori (vezi mesajele de mai sus).")


if __name__ == "__main__":
    try:
        send_items()
    except APIException as e:
        print(f"Eroare API Recombee: {e}")