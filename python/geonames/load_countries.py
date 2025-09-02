from rdflib import Graph, URIRef, Literal, RDF
from rdflib.namespace import SKOS
import pandas as pd

from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def insert_countries(countries_file="../../places/countries.txt"):
    """
    Lit le fichier des pays et insère tous les pays dans le graphe RDF.
    Pour chaque pays, on utilise le code ISO2 pour construire l'URI.
    """
    # Lecture du fichier des pays
    countries_df = pd.read_csv(countries_file, delimiter="\t", encoding="utf-8")
    
    g = Graph()
    
    for idx, row in countries_df.iterrows():
        iso2 = str(row["ISO"]).strip()
        iso3 = str(row["ISO3"]).strip()
        country_label = str(row["Country"]).strip()
        
        # Construction de l'URI pour le pays (renvoie vers la page GeoNames)
        country_uri = URIRef(f"https://www.geonames.org/countries/{iso2}")
        
        g.add((country_uri, RDF.type, ONT.Country))
        g.add((country_uri, ONT.code_iso3, Literal(iso3)))
        g.add((country_uri, ONT.code_iso2, Literal(iso2)))
        g.add((country_uri, SKOS.prefLabel, Literal(country_label)))
    
    # Insertion du graphe dans la base RDF
    insert_graph(g)
    print("Tous les pays ont été insérés avec succès.")

if __name__ == "__main__":
    insert_countries()
