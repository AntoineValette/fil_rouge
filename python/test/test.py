import requests
import json
import pandas as pd
from pandas import json_normalize

USER_KEY = {"user_key":"aa316dfa75128c027b7582c104293ddb"}

QUERY = {
    "field_ids": [
        "identifier",
        "location_identifiers",
        "short_description"
    ],
    "limit": 1000,
    "query": [
    {
        "type": "predicate",
        "field_id": "location_identifiers",
        "operator_id": "includes",
        "values": [
            "4ce61f42-f6c4-e7ec-798d-44813b58856b" #UUID FOR LOS ANGELES
        ]
    },
    {
        "type": "predicate",
        "field_id": "facet_ids",
        "operator_id": "includes",
        "values": [
            "company"
        ]
    }
    ]
}


def get_company_count(query: dict) -> str:
    """
    Effectue une requête POST vers l'API Crunchbase et renvoie le texte brut de la réponse.
    """
    response = requests.post(
        "https://api.crunchbase.com/api/v4/searches/organizations",
        params=USER_KEY,
        json=query
    )
    if response.status_code != 200:
        raise Exception(f"Erreur API {response.status_code}: {response.text}")
    return response.text


def extract_urls(query: dict) -> pd.DataFrame:
    """
    Effectue une requête POST vers l'API Crunchbase, normalise le JSON et retourne un DataFrame.
    """
    response = requests.post(
        "https://api.crunchbase.com/api/v4/searches/organizations",
        params=USER_KEY,
        json=query
    )
    if response.status_code != 200:
        raise Exception(f"Erreur API {response.status_code}: {response.text}")

    data = response.json()
    entities = data.get('entities', [])
    # Normalisation des données pour obtenir un DataFrame exploitable
    df = json_normalize(entities)
    return df


if __name__ == "__main__":
    # Affiche la réponse brute (texte) pour le compte des entreprises
    print(get_company_count(QUERY))

    # Extraction et affichage des données sous forme de DataFrame
    df = extract_urls(QUERY)
    print(df.head())