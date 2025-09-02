import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

def sparql_to_dict(sparql_query):
    """
    Exécute une requête SPARQL sur l'endpoint spécifié et renvoie un dictionnaire
    contenant les résultats.

    :param sparql_query: La requête SPARQL à exécuter (chaîne de caractères).
    :return: Un dictionnaire avec deux clés : "columns" et "rows".
    """
    GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(sparql_query)
    sparql.setReturnFormat(JSON)

    # Exécute la requête et récupère le résultat en JSON
    results = sparql.query().convert()

    # Récupère la liste des variables (colonnes) de la réponse
    columns = results['head']['vars']
    rows = []

    # Parcours chaque binding et construit un dictionnaire pour chaque ligne
    for result in results['results']['bindings']:
        row = {}
        for col in columns:
            # Pour chaque variable, récupère la valeur si elle existe
            row[col] = result.get(col, {}).get('value', None)
        rows.append(row)

    # Retourne un dictionnaire contenant les colonnes et les lignes
    return {"columns": columns, "rows": rows}


# Exemple d'utilisation
if __name__ == "__main__":
    query = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX : <http://www.semanticweb.org/fil_rouge_AntoineValette_GuillaumeRamirez/>

    SELECT DISTINCT ?org ?name WHERE {
      ?org a :Organization .
      ?org skos:prefLabel ?name .
    } LIMIT 10
    """
    result_dict = sparql_to_dict(query)
    print(result_dict)