from rdflib import Graph, URIRef, Literal, Namespace, RDF

from python.util.insert_graph import insert_graph
from python.wikidata.cities_query import get_cities
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def load_cities():
    #Créer un graphe RDF et y ajouter les résultats
    g = Graph()

    for city in get_cities():
        # Récupérer les valeurs
        label_city = city["labelEn"]["value"]

        city_uri = URIRef(city["city"]["value"])
        country_uri=URIRef(city["country"]["value"])

        # Ajout des triples au graphe :
        g.add((city_uri, RDF.type, WD.Q515)) #est de type city  https://www.wikidata.org/wiki/Q515
        g.add((city_uri, WDT.P17, country_uri)) #aPourPays   https://www.wikidata.org/wiki/Property:P17
        g.add((city_uri, SKOS.prefLabel, Literal(label_city)))

    insert_graph(g)
    print("[CITIES] local graph added to graphDB")

if __name__ == "__main__":
    load_cities()
