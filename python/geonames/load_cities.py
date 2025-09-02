from rdflib import Graph, URIRef, Literal, RDF
from rdflib.namespace import XSD, SKOS
import pandas as pd

from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def insert_cities(cities_file="../../places/cities.txt", city_batch_size=1000):
    """
    Lit le fichier des villes et insère les villes dans le graphe RDF par batch pour limiter l'utilisation mémoire.
    
    Chaque ville est insérée avec :
      - Son URI construit à partir du geonameid (ex. https://www.geonames.org/{geonameid})
      - Le lien vers son pays (basé sur le code ISO2)
      - Le nom officiel (SKOS.prefLabel)
      - Les coordonnées (Latitude et Longitude)
      - Les noms alternatifs regroupés dans un seul triplet (si présents)
    """
    cities_columns = [
        "geonameid", "name", "asciiname", "alternatenames", "latitude",
        "longitude", "feature_class", "feature_code", "country_code", "cc2",
        "admin1_code", "admin2_code", "admin3_code", "admin4_code", "population",
        "elevation", "dem", "timezone", "modification_date"
    ]
    cities_df = pd.read_csv(cities_file, delimiter="\t", names=cities_columns, encoding="utf-8")
    
    g = Graph()
    batch_count = 0
    
    for idx, row in cities_df.iterrows():
        geonameid = row["geonameid"]
        city_label = str(row["name"]).strip()
        country_code = str(row["country_code"]).strip()  # Code ISO2
        lat = row["latitude"]
        lon = row["longitude"]
        population = row['population']
        
        # Gestion des noms alternatifs
        alternatenames = str(row["alternatenames"]).strip() if pd.notna(row["alternatenames"]) else ""
        alternatenames_cleaned = (
            ", ".join([name.strip() for name in alternatenames.split(",") if name.strip()])
            if alternatenames else None
        )
        
        # URI de la ville basée sur le geonameid
        city_uri = URIRef(f"https://www.geonames.org/{geonameid}")
        g.add((city_uri, RDF.type, ONT.City))
        
        # Lien vers le pays
        country_uri = URIRef(f"https://www.geonames.org/countries/{country_code}")
        g.add((city_uri, ONT.inCountry, country_uri))
        
        # Ajout des propriétés de la ville
        g.add((city_uri, SKOS.prefLabel, Literal(city_label)))
        g.add((city_uri, ONT.Latitude, Literal(lat, datatype=XSD.float)))
        g.add((city_uri, ONT.Longitude, Literal(lon, datatype=XSD.float)))
        g.add((city_uri, ONT.population, Literal(population, datatype=XSD.integer)))
        
        # Ajout des noms alternatifs, regroupés en un seul literal (si présent)
        if alternatenames_cleaned:
            g.add((city_uri, ONT.Alternate, Literal(alternatenames_cleaned)))
        
        batch_count += 1
        
        # Insertion en batch
        if batch_count % city_batch_size == 0:
            insert_graph(g)
            print(f"Batch de {city_batch_size} villes inséré.")
            g = Graph()  # Réinitialisation du graph pour le prochain batch
    
    # Insertion du dernier batch (s'il reste des villes)
    if len(g) > 0:
        insert_graph(g)
        print(f"Le dernier batch de {len(g)} triplets a été inséré.")

if __name__ == "__main__":
    insert_cities()