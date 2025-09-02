from rdflib import Graph, URIRef, Literal, Namespace, RDF

from python.util.insert_graph import insert_graph
from python.wikidata.countries_query import get_countries
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS


def load_countries():
    #Créer un graphe RDF et y ajouter les résultats
    g = Graph()

    for country in get_countries():
        # Récupérer les valeurs
        iso3_value = country["iso3"]["value"]
        iso2_value = country["iso2"]["value"]
        label_value = country["countryLabel"]["value"]
        country_uri = URIRef(country["country"]["value"])


        # Ajout des triples au graphe :
        g.add((country_uri, RDF.type, WD.Q6256))
        g.add((country_uri, ONT.code_iso3, Literal(iso3_value)))
        g.add((country_uri, ONT.code_iso2, Literal(iso2_value)))
        g.add((country_uri, SKOS.prefLabel, Literal(label_value)))

    insert_graph(g)
    print("[COUNTRIES] local graph added to graphDB")

if __name__ == "__main__":
    load_countries()

