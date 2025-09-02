from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_city_mapping():
    """renvoie  un dataframe avec les uri des villes, leur libellées, l'uri du pays correspondant, et le code pays """

    # Endpoint
    GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/guillaumeramirez/ontologies/2024/11/resaerchandstartups/>
    
    SELECT DISTINCT ?city ?label ?country ?code3 ?code2
    WHERE {
    ?city a wd:Q515. 
    ?city skos:prefLabel ?label.
    ?city wdt:P17 ?country.
    ?country :code_iso2 ?code2.
    ?country :code_iso3 ?code3.
    }
    ORDER BY ?label
    """

    # Configurer et exécuter la requête
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Extraire les bindings
    bindings = results["results"]["bindings"]

    # Transformer les résultats en DataFrame en extrayant la valeur de chaque champ
    df = pd.DataFrame({
    "city": [item["city"]["value"] for item in bindings],
    "label": [item["label"]["value"] for item in bindings],
    "country": [item["country"]["value"] for item in bindings],
    "code3": [item["code3"]["value"] for item in bindings],
    "code2": [item["code2"]["value"] for item in bindings]
    })

    # Il manque New York (qui doit être NYC dans le df) donc on le rajoute manuellement
    new_row = {'city': 'https://www.wikidata.org/wiki/Q60', 'label': 'New York', 'country': 'wd:Q60', 'code': 'USA'}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    return df

def get_city_by_label_and_code3(df, label, code):
    """filtre le dataframe df pour trouver l'uri d'une ville à partir de son nom et du code pays"""
    filtered_df = df[(df['label'].str.lower() == label.lower()) & (df['code3'] == code)]
    if not filtered_df.empty:
        return filtered_df.iloc[0]['city']
    else:
        return None

def get_city_by_label_and_code2(df, label, code):
    """filtre le dataframe df pour trouver l'uri d'une ville à partir de son nom et du code pays"""
    filtered_df = df[(df['label'].str.lower() == label.lower()) & (df['code2'] == code)]
    if not filtered_df.empty:
        return filtered_df.iloc[0]['city']
    else:
        return None



if __name__ == "__main__":
    cities=get_city_mapping()

    """
    city_uri = get_city_by_label_and_code3(cities, "Paris", "FRA")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(cities, "Los Angeles", "USA")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(cities, "palo alto", "USA")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(cities, "new york", "USA")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(cities, "hong kong", "CHN")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(cities, "amsterdam", "NLD")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code3(get_city_mapping(), "montréal", "CAN")
    print("City URI:", city_uri)
    """

    city_uri = get_city_by_label_and_code2(cities, "Paris", "FR")
    print("City URI:", city_uri)

    city_uri = get_city_by_label_and_code2(cities, "Los Angeles", "US")
    print("City URI:", city_uri)
