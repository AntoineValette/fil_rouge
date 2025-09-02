from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, URIRef, Literal, Namespace, RDF, RDFS
import requests

# 1. Définir les endpoints
wikidata_endpoint = "https://query.wikidata.org/sparql"

# 2. La requête SPARQL pour récupérer les pays et leur code ISO3 depuis Wikidata
query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?country ?countryLabel ?iso3 ?iso2
WHERE {
  ?country wdt:P31/wdt:P279* wd:Q6256.
  ?country wdt:P298 ?iso3.
  ?country wdt:P297 ?iso2.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
ORDER BY ?countryLabel
"""

# 3. Exécuter la requête sur Wikidata
def get_countries():
    sparql = SPARQLWrapper(wikidata_endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print("COUNTRIES : results from SPARQL query OK")
    return results["results"]["bindings"]