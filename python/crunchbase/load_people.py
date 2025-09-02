from rdflib import Graph, URIRef, Namespace, RDF, FOAF
import pandas as pd

from python.geonames.mapping import create_mapping_from_graphdb, match_country, match_city, build_city_dicts, build_country_dict
from python.crunchbase.orga_people_functions.geography_functions import add_region, add_linkedin
from python.crunchbase.orga_people_functions.people_functions import add_role, add_name
from python.util.insert_graph import insert_graph
from python.util.Namespaces import ONT, WD, WDT, RDFS, SKOS

def load_people(file_path: str):
    base_ppl = "https://www.crunchbase.com/people/"
    base_orga = "https://www.crunchbase.com/organization/"

    chunk_size = 1000  # nombre de lignes par chunk
    chunk_nb = 0

    mapping=create_mapping_from_graphdb("iso3") #dataframe pour trouver URI d'une ville à partir de son nom et du code pays
    country_dict = build_country_dict(mapping, "iso3")
    official_dict, alternate_dict = build_city_dicts(mapping)

    # Lecture du CSV par chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Créer un nouveau graphe pour chaque chunk
        g = Graph()

        for index, row in chunk.iterrows():
            # URI de la personne basée sur son UUID
            person_uri = URIRef(base_ppl + row['uuid'])
            g.add((person_uri, RDF.type, ONT.Person))

            # Linkedin de la personne
            linkedin_uri=add_linkedin(person_uri,row['linkedin_url'], g )

            # URI de l'organisation basée sur son UUID
            orga_uri = URIRef(base_orga + str(row['featured_job_organization_uuid']))
            g.add((person_uri, ONT.worksFor, orga_uri))

            # ajout nom et prénom
            add_name(person_uri,  row['first_name'], row['last_name'], g)

            #ajout du role (sous classe de worksFor si possible)
            add_role(person_uri, row['featured_job_title'], orga_uri, g)

            # ajout de la region (dataproperty)
            add_region(person_uri, row['region'], g)

            # ajout du pays (classe)
            country = match_country(country_dict, row['country_code'])
            if country:
                country_uri = URIRef(country)
                g.add((person_uri, ONT.inCountry, country_uri))

            # ajout de la ville (classe)
            city = match_city(official_dict, alternate_dict, row['city'], country)
            if city:
                city = URIRef(city)
                g.add((person_uri, ONT.inCity, city))

            #print(f"Person added to local graph: {person_uri} --- {linkedin_uri}")

        # Insérer le graphe du chunk dans GraphDB
        insert_graph(g)
        print(f"[PEOPLE] local graph of chunck {chunk_nb} added to GraphDB")
        chunk_nb += 1

    print("[PEOPLE] all chunks of organization added to GraphDB")

if __name__ == "__main__":
    load_people("../../crunchbase/people.csv")