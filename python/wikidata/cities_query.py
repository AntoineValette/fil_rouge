from SPARQLWrapper import SPARQLWrapper, JSON

# 1. Définir les endpoints
wikidata_endpoint = "https://query.wikidata.org/sparql"

# 2. La requête SPARQL pour récupérer les villes et l'uri du pays
query = """
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT distinct ?city ?labelEn ?country
WHERE {
  ?city wdt:P31/wdt:P279* wd:Q515.  # This finds instances of wd:Q515 or any subclass of wd:Q515.
  ?city wdt:P17 ?country.
  ?city rdfs:label ?labelEn.
  FILTER(LANG(?labelEn) = "en").
}
ORDER BY ?labelEn
"""

# 3. Exécuter la requête sur Wikidata
def get_cities():
    sparql = SPARQLWrapper(wikidata_endpoint)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print("CITIES : results from SPARQL query OK")
    return results["results"]["bindings"]