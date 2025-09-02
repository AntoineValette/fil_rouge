from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

def get_authors_IDs():
    """renvoie une liste des ID des auteurs dans GraphDB """

    # Endpoint
    GRAPHDB_ENDPOINT = "http://localhost:7200/repositories/Fil_Rouge_DB"

    query = """
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX : <http://www.semanticweb.org/guillaumeramirez/ontologies/2024/11/resaerchandstartups/>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX skos:<http://www.w3.org/2004/02/skos/core#>
    PREFIX foaf:<http://xmlns.com/foaf/0.1/>
    PREFIX dcterms: <http://purl.org/dc/terms/>
    
    select distinct ?person
    where{ 
        ?person a :Researcher
    }
    """

    # Configurer et exécuter la requête
    sparql = SPARQLWrapper(GRAPHDB_ENDPOINT)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    # Extraire les bindings
    bindings = results["results"]["bindings"]

    # Transformer les résultats en liste en extrayant la valeur du champ et coupant la chaine
    list_authors=[]
    for item in bindings:
        author = item["person"]["value"]
        author=author.split('/',-1)[-1]
        list_authors.append(author)

    return list_authors

if __name__ == "__main__":
    l=get_authors_IDs()
    print(l)